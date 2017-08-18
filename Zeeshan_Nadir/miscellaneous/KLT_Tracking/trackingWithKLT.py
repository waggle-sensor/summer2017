import numpy as np
import cv2
import trackingUtilities as track
import imageProcUtilities as utils
import matplotlib.pyplot as plt

# KLT Parameters
lk_params = dict(winSize=(15, 15),
                 maxLevel=2,
                 criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

feature_params = dict(maxCorners=100,
                      qualityLevel=0.001,
                      minDistance=3,
                      blockSize=5)

class App:
    def __init__(self, video_src):
        self.track_len = 50
        self.detect_interval = 5
        self.tracks = []
        self.cam = cv2.VideoCapture(video_src)
        self.frame_idx = 0

    def run(self):
        # create background subtraction object
        fgbg = cv2.createBackgroundSubtractorMOG2()
        # Kernels for morphological operations
        kSize = 3
        kernelO = np.ones((kSize, kSize), np.uint8)
        kernelC = np.ones((kSize, kSize), np.uint8)
        counter = 0
        # Video Writer object
        #out = cv2.VideoWriter("C:\\Users\\Zeeshan Nadir\\Documents\\Argonne\\ped_tracking_with_detection_3\\data\\KLT.avi", -1, 30, (800, 450))
        while True:
            ret, frame = self.cam.read()
            if not ret:
                break
            frame = utils.resize(frame, 800)
            counter += 1
            print("Counter = ", counter)
            if counter ==500:
                break
            # ------------------------------------------- background subtraction ------------------------------------
            fgmask = fgbg.apply(frame)
            ret, fgmask = cv2.threshold(fgmask, 0, 255, 0)
            opening = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernelO, iterations=2)
            sure_fg = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernelC, iterations=2)
            (_, contours, _) = cv2.findContours(sure_fg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            list_of_new_boxes = track.giveContours(contours, frame.shape[0]*frame.shape[1], frame.shape[1], frame.shape[0], -1, 10,
                                                   0.0005, 0.20)
            # --------------------------------------------------------------------------------------------------------

            self.frame_idx += 1
            if self.frame_idx < 30:
                continue

            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            vis = frame.copy()

            if len(self.tracks) > 0:
                img0, img1 = self.prev_gray, frame_gray
                p0 = np.float32([tr[-1] for tr in self.tracks]).reshape(-1, 1, 2)
                p1, st, err = cv2.calcOpticalFlowPyrLK(img0, img1, p0, None, **lk_params)
                p0r, st, err = cv2.calcOpticalFlowPyrLK(img1, img0, p1, None, **lk_params)
                d = abs(p0-p0r).reshape(-1, 2).max(-1)
                good = (d < 1) * (d > 0.001)
                new_tracks = []
                for tr, (x, y), good_flag in zip(self.tracks, p1.reshape(-1, 2), good):
                    if not good_flag:
                        continue
                    tr.append((x, y))
                    if len(tr) > self.track_len:
                        del tr[0]
                    new_tracks.append(tr)
                    cv2.circle(vis, (x, y), 2, (0, 255, 0), -1)
                self.tracks = new_tracks
                cv2.polylines(vis, [np.int32(tr) for tr in self.tracks], False, (0, 255, 0))
                #draw_str(vis, (20, 20), 'track count: %d' % len(self.tracks))

            if self.frame_idx % self.detect_interval == 0:
                mask = np.zeros_like(frame_gray)
                for box in list_of_new_boxes:
                    tl_x, tl_y = np.int32((box[0]-box[2]/2, box[1]-box[3]/2))
                    br_x, br_y = np.int32((box[0]+box[2]/2, box[1]+box[3]/2))
                    cv2.rectangle(mask,(tl_x, tl_y), (br_x, br_y), 255, -1)
                for x, y in [np.int32(tr[-1]) for tr in self.tracks]:
                    cv2.circle(mask, (x, y), 5, 0, -1)
                p = cv2.goodFeaturesToTrack(frame_gray, mask = mask, **feature_params)
                if p is not None:
                    for x, y in np.float32(p).reshape(-1, 2):
                        self.tracks.append([(x, y)])

            print(len(self.tracks))
            self.prev_gray = frame_gray
            cv2.imshow('lk_track', vis)
            cv2.imshow('sure_fg', sure_fg)
            #out.write(vis)


            ch = cv2.waitKey(25)
            if ch == 27:
                break
        #out.release()
def main():
    import sys
    print(__doc__)
    App("C:\\Users\\Zeeshan Nadir\\Documents\\Argonne\\Pedestrian_Detection_Tracking\\data\\towncenter.avi").run()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()