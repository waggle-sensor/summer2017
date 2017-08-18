#importing modules

import numpy as np
import cv2
import imageProcUtilities as utils
import matplotlib.pyplot as plt

def get_corners(box, frame_width, frame_height):
    # This function accepts a box in the format of (x,y,w,h) and returns tl and br points
    # It also makes sure everything is inside the given frame width and height
    tl = np.int0((box[0] - box[2]/2, box[1] - box[3]/2))
    br = np.int0((box[0] + box[2]/2, box[1] + box[3]/2))
    tl = tl.reshape(2)
    br = br.reshape(2)
    tl[0] = np.clip(tl[0], 0, frame_width).astype(int)
    br[0] = np.clip(br[0], 0, frame_width).astype(int)
    tl[1] = np.clip(tl[1], 0, frame_height).astype(int)
    br[1] = np.clip(br[1], 0, frame_height).astype(int)
    return (tl[0], tl[1]), (br[0],br[1])


def deleteOverlappingNewWindows(windows, list_of_new_boxes, thresh):
    indices_to_delete = set()
    for i, box in enumerate(list_of_new_boxes):
        for wins in windows:
            if utils.isOverLap(box, wins.kalman.statePost, thresh):
                indices_to_delete.add(i)
                continue
    return indices_to_delete


def givePairs(list_of_current_windows, list_of_new_boxes, pixelMovThresh, overlapThresh, frame_HSV):
    pairs = list()
    for i, wins in enumerate(list_of_current_windows):
        new_matched_windows = list()
        kalmanWindow = np.array([wins.kalman.statePost[0], wins.kalman.statePost[1], wins.kalman.statePost[2], wins.kalman.statePost[3]], dtype=np.int32)
        for j, box in enumerate(list_of_new_boxes):
            if utils.isOverLap(box, kalmanWindow, overlapThresh) and \
                    (abs(wins.kalman.statePost[0] - box[0]) < pixelMovThresh) and \
                    (abs(wins.kalman.statePost[1] - box[1]) < pixelMovThresh):
                new_matched_windows.append(j)
        if len(new_matched_windows)==1:
            pairs.append((new_matched_windows[0], i))
        elif len(new_matched_windows)>1:
            # we will have to break tie here
            score = [None] * len(new_matched_windows)
            for k, new_win_index in enumerate(new_matched_windows):
                # get the histogram of this new window first
                temp_box = list(list_of_new_boxes[new_win_index])
                temp_box[2] = wins.scaleFac * temp_box[2]
                temp_box[3] = wins.scaleFac  * temp_box[3]
                (tl, br) = get_corners(temp_box, frame_HSV.shape[1], frame_HSV.shape[0])

                new_box_roi = frame_HSV[tl[1]:br[1], tl[0]:br[0]]

                histOfNew = cv2.calcHist([new_box_roi], [0, 1], None, [16, 16], [0, 255, 0, 255])
                histOfNew = cv2.normalize(histOfNew, histOfNew, 0, 255, cv2.NORM_MINMAX)

                dotProd = histOfNew * wins.roiHist
                score[k] = dotProd.sum()
            maxIndex = np.argmax(score)
            pairs.append((new_matched_windows[maxIndex], i))
    return pairs


def deleteOverlappingOldWindows(windows, thresh):
    indices_to_delete = set()
    totalOldWindows = len(windows)
    for i, box in enumerate(windows):
        for j in range(i+1,totalOldWindows, 1):
            if utils.isOverLap((box.kalman.statePost[0], box.kalman.statePost[1], box.kalman.statePost[2], box.kalman.statePost[3]),
                               (windows[j].kalman.statePost[0], windows[j].kalman.statePost[1],
                                windows[j].kalman.statePost[2], windows[j].kalman.statePost[3]), thresh):
                indices_to_delete.add(i)
                continue
    return indices_to_delete


def giveContours(ctrs, frame_area, frame_width, frame_height, h_to_w, win_padding, lowerThreshForArea, upperThreshForArea):
    list_of_new_boxes = list()
    # ------------------------------------------- Find Contours ------------------------------------
    for c in ctrs:
        c_area = cv2.contourArea(c)
        if c_area < frame_area *lowerThreshForArea or c_area > frame_area *upperThreshForArea:  # if the contour is too small or too big
            continue
        (x, y, w, h) = cv2.boundingRect(c)
        cx = int(x + w / 2)
        cy = int(y + h / 2)
        if centerOutsideFrame (cx, cy, frame_width, frame_height, win_padding):
            continue
        if (h/w)<h_to_w:
            continue
        list_of_new_boxes.append((cx, cy, w, h))
        #cv2.rectangle(frame, (x-10, y-10), (x + w, y + h), (24, 200, 100), 2)
    return list_of_new_boxes


def purgeAllKalmanWindowsForDeletion(list_of_windows, frame_width, frame_height, win_padding):
    mark_for_del = list()
    for i, win in enumerate(list_of_windows):
        cx = win.kalman.statePost[0]
        cy = win.kalman.statePost[1]
        if centerOutsideFrame (cx, cy, frame_width, frame_height, win_padding):
            win.markForDel = True
        elif win.ctrWithoutMotion > win.ctrWithoutMotionThresh:
            win.markForDel = True
        # if 3 frames without motion, then detect the person in the current window

def centerOutsideFrame (cx, cy, frame_width, frame_height, win_padding=0):
    if (cx <= win_padding or cx >= frame_width - win_padding) \
            or (cy <= win_padding or cy >= frame_height - win_padding):
        return True
    else:
        return False
# ------------------------------------------------------------------------------------------------------


def purgeNewWindowsForPedDetection(list_of_new_boxes, win_W, win_H, frame, hog, scale=1.20):
    list_of_boxes_to_return = list()

    frame_width = frame.shape[0]
    frame_height = frame.shape[1]

    for i, box in enumerate(list_of_new_boxes):
        if box[2] >= win_W and box[3]>= win_H:
            tl = [int(box[0] - scale*box[2] / 2), int(box[1] - scale*box[3] / 2)]
            br = [int(box[0] + scale*box[2] / 2), int(box[1] + scale*box[3] / 2)]
        else:
            tl = [int(box[0] - scale*win_W / 2), int(box[1] - scale*win_H / 2)]
            br = [int(box[0] + scale*win_W / 2), int(box[1] + scale*win_H / 2)]

        tl_x = tl[0]
        tl_y = tl[1]
        br_x = br[0]
        br_y = br[1]
        if tl_x < 0:
            tl[0] = 0
            br[0] = br[0] - tl_x
        if tl_y < 0:
            tl[1] = 0
            br[1] = br[1] - tl_y
        if br_x > frame_width:
            br[0] = frame_width
            tl[0] = tl[0] - br_x + frame_width
        if br_y > frame_height:
            br[1] = frame_width
            tl[1] = tl[1] - br_y + frame_height
        if tl[0]<0 or br[0]>frame_width or tl[1] < 0 or br[1]>frame_height:
            break
        box_frame = frame[tl[1]:br[1], tl[0]:br[0]]
        found, w = hog.detectMultiScale(box_frame, winStride=(8, 8), padding=(4, 4), scale=1.2)
        if len(found)>0:
            for x, y, w, h in found:
                list_of_boxes_to_return.append((tl[0] + x + w/2, tl[1] + y+h/2, w, h))

    return list_of_boxes_to_return

def purgeExistingWindowsForPedDetection(windows, win_W, win_H, frame, hog, scale=1.20):
    indices_to_delete=set()
    frame_width = frame.shape[0]
    frame_height = frame.shape[1]

    for i, win in enumerate(windows):
        if win.ctrWithoutMotion <= win.ctrWithoutMotionThresh:
            continue
        box = [win.kalman.statePost[0], win.kalman.statePost[1], win.kalman.statePost[2], win.kalman.statePost[3]]
        if box[2] >= win_W and box[3]>= win_H:
            tl = [int(box[0] - scale*box[2] / 2), int(box[1] - scale*box[3] / 2)]
            br = [int(box[0] + scale*box[2] / 2), int(box[1] + scale*box[3] / 2)]
        else:
            tl = [int(box[0] - scale*win_W / 2), int(box[1] - scale*win_H / 2)]
            br = [int(box[0] + scale*win_W / 2), int(box[1] + scale*win_H / 2)]

        tl_x = tl[0]
        tl_y = tl[1]
        br_x = br[0]
        br_y = br[1]
        if tl_x < 0:
            tl[0] = 0
            br[0] = br[0] - tl_x
        if tl_y < 0:
            tl[1] = 0
            br[1] = br[1] - tl_y
        if br_x > frame_width:
            br[0] = frame_width
            tl[0] = tl[0] - br_x + frame_width
        if br_y > frame_height:
            br[1] = frame_width
            tl[1] = tl[1] - br_y + frame_height
        if tl[0]<0 or br[0]>frame_width or tl[1] < 0 or br[1]>frame_height:
            break
        box_frame = frame[tl[1]:br[1], tl[0]:br[0]]
        found, w = hog.detectMultiScale(box_frame, winStride=(8, 8), padding=(4, 4), scale=1.2)
        if len(found)==1:
            win.ctrWithoutMotion = 0
            cx = found[0,0] + found[0,1] / 2
            cy = found[0,1] + found[0,2] / 2
            w = found[0,2]
            h = found[0,3]
            measurement = np.array([[cx], [cy], [w], [h]], dtype=np.float32)
            win.correct_with_high_precision(measurement)