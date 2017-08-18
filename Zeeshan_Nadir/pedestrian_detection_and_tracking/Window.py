import numpy as np
import cv2
import trackingUtilities as track
import imageProcUtilities as utils
from matplotlib import pyplot as plt
class Window:
    #totalPedestriansSoFar = 0
    def __init__(self, box, scaleFac, detectionRate, maxSpeed, frame, frame_HSV, frame_gray, feature_params):

        # Kalman Filter
        self.kalman = cv2.KalmanFilter(4, 2)
        self.kalman.measurementMatrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0]], np.float32)
        self.kalman.transitionMatrix = np.array([[1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1]], np.float32)
        self.kalman.processNoiseCov = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], np.float32) * 0.03
        self.kalman.measurementNoiseCov = np.array([[1, 0], [0, 1]], np.float32) * 0.0003

        # Initialize the KALMAN Filter
        self.kalman.__setattr__('statePost', np.array(([[box[0]], [box[1]], [0], [0] ] ), dtype=np.float32))

        # Initialize the width and height of the bouding box
        self.w = box[2]
        self.h = box[3]
        # Maximum speed of each window object (in units of pixels per frame)
        self.maxSpeed = maxSpeed
        # Detection rate in units of frames per detection
        self.detectionRate = detectionRate
        # Counter for pedestrian detection in current window
        self.counter = 0

        # Camshift object
        # reduce the size of the box by scale factor
        w = self.w * scaleFac
        h = self.h * scaleFac

        self.measurement = None

        (tl, br) = track.get_corners((self.kalman.statePost[0], self.kalman.statePost[1], w, h),
                                     frame_HSV.shape[1], frame_HSV.shape[0])
        roi = frame_HSV[tl[1]:br[1], tl[0]:br[0],:]
        self.roiHist = cv2.calcHist([roi], [0, 1], None, [8, 8], [0, 180, 0, 255])
        self.appearanceHist = self.roiHist.flatten()
        self.roiHist = cv2.normalize(self.roiHist, self.roiHist, 0, 255, cv2.NORM_MINMAX)
        self.termination = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

        # Total pedestrians so far
        #Window.totalPedestriansSoFar += 1
        #self.id = Window.totalPedestriansSoFar
        # Select the color for the window
        self.color = (int(np.random.random_integers(0, 2)*127),
                      int(np.random.random_integers(0, 2)*127),
                      int(np.random.random_integers(0, 2)*127))

        #(self.id, self.color) = self.matchCurrentWindowWithPastPeds(listOfDeletedPeds, corrThreshForOldWins)

        # Indicate to delete the window
        self.markForDel = False
        # Keep track of the motion of this window
        self.isWindowMoving = True
        # Times without a motion measurement and corresponding threshold
        self.ctrWithoutMotion = 0
        # Maximum no. of predictions without getting a detection
        self.ctrWithoutMotionThresh = 35

        self.measurementType = None

        # KLT properties
        self.tracks = []
        self.countAfterLastDetection = 0
        self.detectCtrThresh = 30
        self.track_len = 1
        self.totalPtsThresh = 3
        self.pixelThreshForPurgingPts = 2
        self.totalPts = 0
        self.initializeCrnrPts(box, scaleFac, frame, frame_gray, feature_params)

    def matchCurrentWindowWithPastPeds(self, listOfDeteledPeds, corrThreshForOldWins):
        Window.totalPedestriansSoFar +=1
        self.id = Window.totalPedestriansSoFar
        # Select the color for the window
        self.color = (int(np.random.random_integers(0,255)),
                      int(np.random.random_integers(0,255)),
                      int(np.random.random_integers(0,255)))
        for i, oldWins in enumerate(listOfDeteledPeds):
            corr = cv2.compareHist(self.appearanceHist, oldWins[2], cv2.HISTCMP_CORREL)
            if corr > corrThreshForOldWins:
                self.id = oldWins[0]
                self.color = oldWins[1]
                Window.totalPedestriansSoFar -= 1
                break
        return (self.id, self.color)


    def initializeCrnrPts(self, box, scaleFac, frame, frame_gray, feature_params):
        mask = np.zeros_like(frame_gray)
        tl_x, tl_y = np.int32((box[0] - scaleFac * box[2] / 2, box[1] - scaleFac * box[3] / 2))
        br_x, br_y = np.int32((box[0] + scaleFac * box[2] / 2, box[1] + scaleFac * box[3] / 2))
        cv2.rectangle(mask, (tl_x, tl_y), (br_x, br_y), 255, -1)
        pts = cv2.goodFeaturesToTrack(frame_gray, mask=mask, **feature_params)

        if pts is not None:
            for x, y in np.float32(pts).reshape(-1, 2):
                self.tracks.append([(x, y)])
                #cv2.circle(frame, (x, y), 2, self.color, -1)
        self.totalPts = len(self.tracks)

    def trackCrnrPts(self, frame, scaleFac, prev_gray, frame_gray, lk_params):
        if self.countAfterLastDetection < self.detectCtrThresh and self.totalPts > self.totalPtsThresh:
            p0 = np.float32([tr[-1] for tr in self.tracks]).reshape(-1, 1, 2)
            p1, st, err = cv2.calcOpticalFlowPyrLK(prev_gray, frame_gray, p0, None, **lk_params)
            p0r, st, err = cv2.calcOpticalFlowPyrLK(frame_gray, prev_gray, p1, None, **lk_params)
            d = abs(p0 - p0r).reshape(-1, 2).max(-1)
            good = d < self.pixelThreshForPurgingPts

            for i, j in enumerate(good):
                if p1[i,0,0] < self.kalman.statePost[0] - scaleFac* self.w/2 or \
                                p1[i, 0, 0] > self.kalman.statePost[0] + scaleFac * self.w / 2 or \
                                p1[i, 0, 1] < self.kalman.statePost[1] - scaleFac * self.h / 2 or \
                                p1[i, 0, 1] > self.kalman.statePost[1] + scaleFac * self.h / 2:
                    good[i]=False

            new_tracks = []
            for tr, (x, y), good_flag in zip(self.tracks, p1.reshape(-1, 2), good):
                if not good_flag:
                    continue
                tr.append((x, y))
                if len(tr) > self.track_len:
                    del tr[0]
                new_tracks.append(tr)
                cv2.circle(frame, (x, y), 2, self.color, -1)
            self.tracks = new_tracks

            d = np.zeros((2), dtype=np.float32)
            for tr in self.tracks:
                d[0] = d[0] + tr[0][0]
                d[1] = d[1] + tr[0][1]
            self.totalPts = len(self.tracks)
            if self.totalPts < self.totalPtsThresh:
                return None
            else:
                d[0] = d[0] / self.totalPts
                d[1] = d[1] / self.totalPts
                cv2.polylines(frame, [np.int32(tr) for tr in self.tracks], False, self.color)
                measurement = np.array([[d[0]], [d[1]]], dtype = np.float32)
                return measurement
        else:
            return None

    def predict(self):
        self.counter+=1
        self.kalman.predict()
        self.countAfterLastDetection = self.countAfterLastDetection + 1
        self.measurement = None


    def setMeasurement(self, box):
        measurement = np.array([[box[0]], [box[1]], [box[2]], [box[3]]], dtype=np.float32)
        self.measurement = measurement


    def correct_with_new_motion(self, measurement):
        self.w = int(measurement[2])
        self.h = int(measurement[3])
        self.isWindowMoving = True
        self.ctrWithoutMotion = 0
        self.kalman.correct(measurement[0:2])


    def correct(self, pixelMovThresh, frame_HSV, corrThresh, scaleFac, overlapThresh,
                winW, winH, frame, hog, detectScaleUp, overlapWeightage, prev_gray, frame_gray, lk_params,
                feature_params, frame_width, frame_height, win_padding):
        if self.measurement is not None:
            self.correct_with_new_motion(self.measurement)
            self.initializeCrnrPts(self.measurement, scaleFac, frame, frame_gray, feature_params)
            self.measurementType = 0
            self.countAfterLastDetection = 0
        elif self.counter % self.detectionRate == 0:
            measurement = self.detectPedestrianInCurrentWindow(winW, winH, frame, frame_HSV, scaleFac, pixelMovThresh, corrThresh, overlapThresh,
                                                               overlapWeightage, hog, detectScaleUp, frame_width, frame_height)
            if measurement is not None:
                self.correct_with_new_motion(measurement)
                self.countAfterLastDetection = 0
                self.measurementType = 1
                self.initializeCrnrPts(measurement, scaleFac, frame, frame_gray, feature_params)
            else:
                measurement = self.trackCrnrPts(frame, scaleFac, prev_gray, frame_gray, lk_params)
                if measurement is not None:
                    self.kalman.correct(measurement)
                    self.measurementType = 1
                else:
                    self.ctrWithoutMotion = self.ctrWithoutMotion + 1
                    self.isWindowMoving = False
                    self.measurementType = 2
        else:
            measurement = self.trackCrnrPts(frame, scaleFac, prev_gray, frame_gray, lk_params)
            if measurement is not None:
                self.kalman.correct(measurement)
                self.measurementType = 1
            else:
                # self.correct_with_color(pixelMovThresh, frame_HSV, corrThresh, scaleCam)
                self.ctrWithoutMotion = self.ctrWithoutMotion + 1
                self.isWindowMoving = False
                self.measurementType = 2

        self.clipSpeed()
        self.purgeAllKalmanWindowsForDeletion(self, frame_width, frame_height, win_padding)
    def detectPedestrianInCurrentWindow(self, winW, winH, frame, frame_HSV, scaleFac, pixelMovThresh, corrThresh, overlapThresh,
                                        overlapWeightage, hog, detectScaleUp, frame_width, frame_height):
        measurement = None
        Kbox = [self.kalman.statePost[0], self.kalman.statePost[1],  self.w, self.h]
        boxes = track.detectPedestrian(Kbox, winW, winH, frame, hog, detectScaleUp, frame_width, frame_height)
        list_of_hist = list()

        for i, box in enumerate(boxes):
            box_frame_1 = frame_HSV[int(box[1] - scaleFac * box[3] / 2):int(box[1] + scaleFac * box[3] / 2),
                          int(box[0] - scaleFac * box[2] / 2):int(box[0] + scaleFac * box[2] / 2), :]
            hist_1 = cv2.calcHist([box_frame_1], [0, 1], None, [8, 8], [0, 180, 0, 255])
            hist_1 = cv2.normalize(hist_1, hist_1).flatten()
            list_of_hist.append(hist_1)

        if len(boxes)>=1:
            match = np.zeros((len(boxes)), dtype = np.float32)
            for i, box in enumerate(boxes):
                overlap = utils.giveOverLap(box, Kbox)
                corr = cv2.compareHist(list_of_hist[i], self.appearanceHist, cv2.HISTCMP_CORREL)
                if overlap > overlapThresh and corr > corrThresh and \
                            (abs(self.kalman.statePost[0] - box[0]) < pixelMovThresh) and \
                            (abs(self.kalman.statePost[1] - box[1]) < pixelMovThresh):
                    match[i] = overlapWeightage * overlap + (1-overlapWeightage) * corr
            j = match.argmax()
            if match[j] > 0:
                measurement = np.array([[box[0]], [box[1]], [box[2]], [box[3]]], dtype=np.float32)
        return measurement

    def purgeAllKalmanWindowsForDeletion(self, frame_width, frame_height, win_padding):
        cx = self.kalman.statePost[0]
        cy = self.kalman.statePost[1]
        if track.centerOutsideFrame(cx, cy, frame_width, frame_height, win_padding):
            self.markForDel = True
        elif self.ctrWithoutMotion > self.ctrWithoutMotionThresh:
            self.markForDel = True

    def resetMotion(self):
        self.isWindowMoving = False

    def clipSpeed(self):
        if self.kalman.statePost[2] < -self.maxSpeed:
            self.kalman.statePost[2] = -self.maxSpeed
        if self.kalman.statePost[3] < -self.maxSpeed:
            self.kalman.statePost[3] = -self.maxSpeed

        if self.kalman.statePost[2] > self.maxSpeed:
            self.kalman.statePost[2] = self.maxSpeed
        if self.kalman.statePost[3] > self.maxSpeed:
            self.kalman.statePost[3] = self.maxSpeed

    def __del__(self):
        print('Pedestrian at location ', (self.kalman.statePost[0], self.kalman.statePost[1]), ' deleted!!')
        print("Counter without motion = ", self.ctrWithoutMotion)
