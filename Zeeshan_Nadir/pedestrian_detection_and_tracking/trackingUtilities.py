#importing modules

import numpy as np
import cv2
import imageProcUtilities as utils
from matplotlib import pyplot as plt


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
            if utils.giveOverLap(box, wins.kalman.statePost)> thresh:
                indices_to_delete.add(i)
                continue
    return indices_to_delete


def mapMotionToCurrentWindows(list_of_current_windows, list_of_new_boxes, pixelMovThresh, overlapWeightage,
              threshForDiscarding, overlapThresh, corrThresh, scaleFac, frame_HSV):
    new_boxes_to_discard = list()
    list_of_hist = list()
    if len(list_of_new_boxes)>0:
        match = np.zeros((len(list_of_new_boxes), len(list_of_current_windows)), dtype=np.float32)
        overlapOfNewWindowsWithOld = np.zeros((len(list_of_new_boxes), len(list_of_current_windows)), dtype=np.float32)

        # Compute the histogram for each new box
        for i, box in enumerate(list_of_new_boxes):
            box_frame_1 = frame_HSV[int(box[1] - scaleFac * box[3] / 2):int(box[1] + scaleFac* box[3] / 2),
                          int(box[0] - scaleFac * box[2] / 2):int(box[0] + scaleFac * box[2] / 2), :]
            hist_1 = cv2.calcHist([box_frame_1], [0, 1], None, [8, 8], [0, 180, 0, 255])
            hist_1 = cv2.normalize(hist_1, hist_1).flatten()
            list_of_hist.append(hist_1)

        # Compute the match matrix for all new/old pairs
        for i, new_box in enumerate(list_of_new_boxes):
            for j, win in enumerate(list_of_current_windows):
                currentWin = [win.kalman.statePost[0], win.kalman.statePost[1], win.w, win.h]

                overlap = utils.giveOverLap(new_box, currentWin)
                corr    = cv2.compareHist(list_of_hist[i], win.appearanceHist, cv2.HISTCMP_CORREL)
                overlapOfNewWindowsWithOld[i,j]=overlap
                if overlap > overlapThresh and corr > corrThresh and\
                        (abs(win.kalman.statePost[0] - new_box[0]) < pixelMovThresh) and \
                        (abs(win.kalman.statePost[1] - new_box[1]) < pixelMovThresh):
                    match[i,j]= (1-overlapWeightage)*corr + overlapWeightage*overlap

        # MAP the old to new based on match
        for j, win in enumerate(list_of_current_windows):
            i = match[:,j].argmax()
            j_o = match[i,:].argmax()
            if j_o == j and match[i,j] > 0:
                #pairs.append((i,j))
                list_of_current_windows[j].setMeasurement(list_of_new_boxes[i])

        # Delete all the new ones based upon their overlap with old
        if len(list_of_current_windows)>0 and len(list_of_new_boxes) > 0:
            for i, new_box in enumerate(list_of_new_boxes):
                overlap = overlapOfNewWindowsWithOld[i,:].max()
                if overlap > threshForDiscarding:
                    new_boxes_to_discard.append(i)

    return new_boxes_to_discard



# This function could be used to delete extra bounding boxes on the same pedestrian
def deleteOverlappingOldWindows(windows, thresh):
    indices_to_delete = set()
    totalOldWindows = len(windows)
    for i, box in enumerate(windows):
        for j in range(i+1,totalOldWindows, 1):
            if utils.giveOverLap((box.kalman.statePost[0], box.kalman.statePost[1], box.w, box.h),
                               (windows[j].kalman.statePost[0], windows[j].kalman.statePost[1],
                                windows[j].w, windows[j].h))> thresh:
                indices_to_delete.add(i)
                continue
    return indices_to_delete

# This function is used to get a a list of bounding boxes from all the foreground objects
def giveBoundingBoxes(ctrs, frame_area, frame_width, frame_height, h_to_w, win_padding, lowerThreshForArea, upperThreshForArea):
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

def centerOutsideFrame (cx, cy, frame_width, frame_height, win_padding=0):
    if (cx <= win_padding or cx >= frame_width - win_padding) \
            or (cy <= win_padding or cy >= frame_height - win_padding):
        return True
    else:
        return False
# ------------------------------------------------------------------------------------------------------


def purgeNewWindowsForPedDetection(list_of_new_boxes, win_W, win_H, frame, hog, detectScaleUp):
    list_of_boxes_to_return = list()

    frame_width = frame.shape[0]
    frame_height = frame.shape[1]

    for i, box in enumerate(list_of_new_boxes):
        boxes = detectPedestrian(box, win_W, win_H, frame, hog, detectScaleUp, frame_width, frame_height)
        list_of_boxes_to_return = list_of_boxes_to_return + boxes

    return list_of_boxes_to_return


def detectPedestrian(box, winW, winH, frame, hog, detectScaleUp, frame_width, frame_height):
    boxes = list()
    if box[2] >= winW * 0.5 and box[3] >= winH * 0.5:
        tl = [int(box[0] - detectScaleUp * box[2] / 2), int(box[1] - detectScaleUp * box[3] / 2)]
        br = [int(box[0] + detectScaleUp * box[2] / 2), int(box[1] + detectScaleUp * box[3] / 2)]
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

        if tl[0] >= 0 and br[0] < frame_width and tl[1] >= 0 and br[1] < frame_height:
            box_frame = frame[tl[1]:br[1], tl[0]:br[0]]
            if box_frame.shape[1]>=winW and box_frame.shape[0]>=winH:
                found, w = hog[0].detectMultiScale(box_frame, winStride=(4, 4), padding=(16, 16), scale=1.2)
                if len(found) > 0:
                    for x, y, w, h in found:
                        boxes.append((tl[0] + x + w / 2, tl[1] + y + h / 2, w, h))
    elif box[2] >= winW * 0.25 and box[3] >= winH * 0.25:
        tl = [int(box[0] - detectScaleUp * box[2] / 2), int(box[1] - detectScaleUp * box[3] / 2)]
        br = [int(box[0] + detectScaleUp * box[2] / 2), int(box[1] + detectScaleUp * box[3] / 2)]
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

        if tl[0] >= 0 and br[0] < frame_width and tl[1] >= 0 and br[1] < frame_height:
            box_frame = frame[tl[1]:br[1], tl[0]:br[0]]
            if box_frame.shape[1] >= winW/2 and box_frame.shape[0] >= winH/2:
                found, w = hog[1].detectMultiScale(box_frame, winStride=(4, 4), padding=(16, 16), scale=1.2)
                if len(found) > 0:
                    for x, y, w, h in found:
                        boxes.append((tl[0] + x + w / 2, tl[1] + y + h / 2, w, h))
    return boxes

def purgeExistingWindowsForPedDetection(windows, win_W, win_H, frame, hog, detectScaleUp):
    frame_width = frame.shape[0]
    frame_height = frame.shape[1]

    for i, win in enumerate(windows):
        if win.ctrWithoutMotion <= win.ctrWithoutMotionThresh:
            continue
        box = [win.kalman.statePost[0], win.kalman.statePost[1], win.w, win.h]
        if box[2] >= win_W and box[3]>= win_H:
            tl = [int(box[0] - detectScaleUp*box[2] / 2), int(box[1] - detectScaleUp*box[3] / 2)]
            br = [int(box[0] + detectScaleUp*box[2] / 2), int(box[1] + detectScaleUp*box[3] / 2)]
        else:
            tl = [int(box[0] - detectScaleUp*win_W / 2), int(box[1] - detectScaleUp*win_H / 2)]
            br = [int(box[0] + detectScaleUp*win_W / 2), int(box[1] + detectScaleUp*win_H / 2)]

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
        found, w = hog.detectMultiScale(box_frame, winStride=(8, 8), padding=(16, 16), scale=1.5)
        if len(found)>=1:
            win.ctrWithoutMotion = 0
