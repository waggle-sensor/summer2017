import numpy as np
import cv2
import trackingUtilities as track
import matplotlib.pyplot as plt

class Window:
    def __init__(self, box, scaleFac, frame_HSV):

        # Kalman Filter
        self.kalman = cv2.KalmanFilter(8, 4)
        self.kalman.transitionMatrix = np.array([ [1, 0, 0, 0, 1, 0, 0, 0],[0, 1, 0, 0, 0, 1, 0, 0],
                                                  [0, 0, 1, 0, 0, 0, 1, 0],[0, 0, 0, 1, 0, 0, 0, 1],
                                                  [0, 0, 0, 0, 1, 0, 0, 0],[0, 0, 0, 0, 0, 1, 0, 0],
                                                  [0, 0, 0, 0, 0, 0, 1, 0],[0, 0, 0, 0, 0, 0, 0,1]], np.float32)

        self.kalman.measurementMatrix = np.array([[1, 0, 0, 0, 0, 0, 0, 0],[0, 1, 0, 0, 0, 0, 0, 0],
                                                  [0, 0, 1, 0, 0, 0, 0, 0],[0, 0, 0, 1, 0, 0, 0, 0]], np.float32)

        self.kalman.processNoiseCov = np.eye((8), dtype=np.float32) * 0.0003


        self.kalman.measurementNoiseCov = np.eye((4), dtype=np.float32) * 0.0003


        # Initialize the KALMAN Filter
        self.kalman.__setattr__('statePost', np.array(([ [box[0]], [box[1]], [box[2]], [box[3]], [0], [0], [0], [0] ] ), dtype=np.float32))

        # Camshift object
        # reduce the size of the box by scale factor
        w = box[2] * scaleFac
        h = box[3] * scaleFac
        (tl, br) = track.get_corners((self.kalman.statePost[0], self.kalman.statePost[1], w, h),
                                     frame_HSV.shape[1], frame_HSV.shape[0])
        roi = frame_HSV[tl[1]:br[1], tl[0]:br[0],:]
        self.roiHist = cv2.calcHist([roi], [0, 1], None, [16, 16], [0, 255, 0, 255])
        self.roiHist = cv2.normalize(self.roiHist, self.roiHist, 0, 255, cv2.NORM_MINMAX)
        self.termination = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

        # Select the color for the window
        self.color = (int(np.random.random_integers(0,1)*255),
                      int(np.random.random_integers(0,1)*255),
                      int(np.random.random_integers(0,1)*255))

        # Indicate to delte the window
        self.markForDel = False

        # Keep track of the motion of this window
        self.isWindowMoving = True

        # Scale factor for CAMShift
        self.scaleFac = scaleFac

        # Scale factor for widening of ped detection window
        self.widenPedDetectWin = 1.20

        # Times without a motion measurement and corresponding threshold
        self.ctrWithoutMotion = 0
        self.ctrWithoutMotionThresh = 30

    def predict(self):
        self.ctrWithoutMotion = self.ctrWithoutMotion + 1
        self.kalman.predict()


    def correct_with_new_motion(self, measurement):
        self.isWindowMoving = True
        self.ctrWithoutMotion = 0
        self.kalman.correct(measurement)

    def correct_with_high_precision(self, measurement):
        self.isWindowMoving = True
        self.ctrWithoutMotion = 0
        oldMeasurementNoiseCov = self.kalman.measurementNoiseCov
        self.kalman.measurementNoiseCov = oldMeasurementNoiseCov * 0.001
        self.kalman.correct(measurement)
        self.kalman.measurementNoiseCov = oldMeasurementNoiseCov

    def correct_with_color (self, pixelMovThresh, frame_HSV):
        frame_width = frame_HSV.shape[1]
        frame_height = frame_HSV.shape[0]
        w = self.kalman.statePost[2]
        h = self.kalman.statePost[3]

        backProj = cv2.calcBackProject([frame_HSV], [0, 1], self.roiHist, [0, 255, 0, 255], 1)
        mask = np.zeros_like(backProj, dtype = np.uint8)
        (tl, br) = track.get_corners((self.kalman.statePost[0], self.kalman.statePost[1], w*(1+self.scaleFac), h*(1+self.scaleFac)),
                               frame_width, frame_height)
        tl = list(tl)
        br = list(br)
        if br[0]-tl[0] <= 0 or br[1]-tl[1] <= 0:
            self.markForDel = True
        else:
            if track.centerOutsideFrame (tl[0], tl[1], frame_width, frame_height):
                roiBox = (0,0,frame_HSV.shape[1], frame_height)
            elif track.centerOutsideFrame (br[0], br[1], frame_width, frame_height):
                roiBox = (0, 0, frame_width, frame_height)
            else:
                roiBox = (tl[0],tl[1],br[0]-tl[0],br[1]-tl[1])

            mask[roiBox[1]:roiBox[1]+roiBox[3], roiBox[0]:roiBox[0]+roiBox[2]] = 255
            backProj = backProj * mask

            (r, roiBox) = cv2.CamShift(backProj, roiBox, self.termination)

            pts = np.int0(cv2.boxPoints(r))
            x, y, w, h = cv2.boundingRect(pts)
            cx = x + w/2
            cy = y + h/2

            # Kalman Filter Measurement
            if abs(cx - self.kalman.statePost[0]) <= pixelMovThresh and abs(cy - self.kalman.statePost[1]) <= pixelMovThresh:
                measurement = np.array([[cx], [cy], [self.kalman.statePost[2]], [self.kalman.statePost[3]]], dtype=np.float32)
                self.kalman.correct(measurement)

        self.ctrWithoutMotion = self.ctrWithoutMotion + 1
        self.isWindowMoving = False

    def resetMotion(self):
        self.isWindowMoving = False

    def __del__(self):
        print('Pedestrian at location ', (self.kalman.statePost[0], self.kalman.statePost[1]), ' deleted!!')
        print("Counter without motion = ", self.ctrWithoutMotion)