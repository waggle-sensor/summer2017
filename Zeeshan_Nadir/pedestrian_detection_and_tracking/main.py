# import the necessary modules
import cv2
import imageProcUtilities as utils
import numpy as np
from Window import Window
import trackingUtilities as track
import matplotlib.pyplot as plt

def main():
    # ------------------------------ Ped Detection Initialization ------------------------------------------------
    # HOG descriptor
    win_W = 64; win_H = 128
    winSize = (win_W, win_H)
    blockSize = (16, 16)
    blockStride = (8, 8)
    cellSize = (8, 8)
    nbins = 9
    hog1 = cv2.HOGDescriptor(winSize, blockSize, blockStride, cellSize, nbins)
    hog1.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    winSize = (int(win_W/2), int(win_H/2))
    blockSize = (8, 8)
    blockStride = (4, 4)
    cellSize = (4, 4)
    nbins = 9
    hog2 = cv2.HOGDescriptor(winSize, blockSize, blockStride, cellSize, nbins)
    hog2.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    hog = [hog1, hog2]
    # -------------------------------------------------------------------------------------------------------------

    # Keep history of deleted pedestrians
    listOfDeletedPedestrians = list()
    totalPedestriansToRemember = 20

    # ------------------------------------------------- Parameters ------------------------------------------------
    # scale factor for reduction of box size for finding initial histogram
    scaleFac = 0.6
    # scale factor for detection window size
    detectScaleUp = 1.6
    # Maximum speed of each window object (in units of pixels per frame)
    maxSpeed = 5
    # height to width ratio to purge windows
    h_to_w = 1.3
    # Kernels for morphological operations`
    kSize = 4
    kernelO = np.ones((kSize, kSize), np.uint8)
    kernelC = np.ones((kSize, kSize), np.uint8)
    # Weight of overlap vs weight of correlation
    overlapWeightage = 0.9
    # Overlap threshold
    overlapThresh = 0.50
    # Appearance Model Threshold
    corrThresh = 0.15
    # Correlation threshold for matching with old windows
    # corrThreshForOldWins = 0.70
    # Threshold for discarding new boxes
    threshForDiscarding = 0.40
    # Detection Rate in units of frames per detection
    detectionRate = 10
    # pixel movement threshold
    pixelMovThresh = 50

    # Window deletion factor
    win_padding = 10

    # List of window objects
    list_of_windows = list()
    counter = 0;

    # Capture the video and set the frame size
    cap = cv2.VideoCapture("C:\\Users\\Zeeshan Nadir\\Documents\\Argonne\\Pedestrian_Detection_Tracking\\data\\towncenter.avi")
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_width = 800
    frame_height = 450
    frame_area = frame_height * frame_width

    # KLT Parameters
    lk_params = dict(winSize=(15, 15),
                     maxLevel=2,
                     criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

    feature_params = dict(maxCorners=100,
                          qualityLevel=0.001,
                          minDistance=3,
                          blockSize=5)

    #frame_height = 360
    #frame_width = 640
    #cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    #cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
    #frame_width =  int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    #frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Video Writer object
    #out = cv2.VideoWriter(".\\data\\results11.avi", -1, fps, (frame_width, frame_height))

    # create background subtraction object
    fgbg = cv2.createBackgroundSubtractorMOG2()
    list_of_new_boxes = list()
    while True:
        counter += 1
        print("Frame = ", counter, "Windows =", len(list_of_windows))
        # -------------------------- grab the current frame ----------------------------------------------------
        ret, frame = cap.read()

        if frame is None:
            break

        if counter ==2000:
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frame = utils.resize(frame, frame_width)
        frame_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # --------------------------------------------------------------------------------------------------------

        # ------------------------------------------- background subtraction ------------------------------------
        fgmask = fgbg.apply(frame)
        ret, fgmask = cv2.threshold(fgmask, 0, 255, 0)
        opening = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernelO, iterations=2)
        sure_fg = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernelC, iterations=2)
        (_, contours, _) = cv2.findContours(sure_fg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # ------------------------------------------------------------------------------------------------------

        # ---------------------------------- Get the list of new boxes -------------------------------------------
        list_of_new_boxes = track.giveBoundingBoxes(contours, frame_area, frame_width, frame_height, h_to_w, win_padding,
                                         0.003/100, 20/100)


        for i, box in enumerate(list_of_new_boxes):
            cx = box[0]
            cy = box[1]
            w  = box[2]
            h  = box[3]
            if win_padding<=cx<=frame_width-win_padding \
                    and win_padding<=cy<=frame_height-win_padding:
                x = int(cx - w/2)
                y = int(cy-h/2)
                cv2.rectangle(sure_fg, (x, y), (x + w, y + h), (127,127,127), 2)
        # -------------------------------------------- Get new Kalman Windows ----------------------------------
        if len(list_of_new_boxes)>0:
            list_of_new_boxes = track.purgeNewWindowsForPedDetection(list_of_new_boxes, win_W, win_H, frame, hog, detectScaleUp)
        # ------------------------------------------------------------------------------------------------------------

        for i, box in enumerate(list_of_new_boxes):
            cx = box[0]
            cy = box[1]
            w  = box[2]
            h  = box[3]
            if win_padding<=cx<=frame_width-win_padding \
                    and win_padding<=cy<=frame_height-win_padding:
                x = int(cx - w/2)
                y = int(cy-h/2)
                cv2.rectangle(sure_fg, (x, y), (x + w, y + h), (255,255,255), 2)
        cv2.imshow('Sure Foreground', sure_fg)
        # ------------------------------------------------------------------------------------------------------
        # ----------------------------- Predict the kalman windows ------------------------------------------------
        for win in list_of_windows:
            win.predict()
        # ------------------------------------------------------------------------------------------------------

        # ----------------------------- Correct Kalman Windows for moving objects ----------------------------------
        new_boxes_to_discard = track.mapMotionToCurrentWindows(list_of_windows, list_of_new_boxes, pixelMovThresh, overlapWeightage,
                                                      threshForDiscarding, overlapThresh, corrThresh, scaleFac, frame_HSV)

        for i, win in enumerate(list_of_windows):
            list_of_windows[i].correct(pixelMovThresh, frame_HSV, corrThresh,
                                       scaleFac, overlapThresh, win_W, win_H, frame, hog, detectScaleUp, overlapWeightage,
                                       prev_gray, frame_gray, lk_params, feature_params, frame_width, frame_height, win_padding)


        # ------------------------------------ Delete all the mapped new boxes ----------------------------------
        if len(list_of_new_boxes) > 0:
            list_of_new_boxes = [i for j, i in enumerate(list_of_new_boxes) if j not in new_boxes_to_discard]
        # ------------------------------------------------------------------------------------------------------

        # ------------------------ Add all the new windows in the current list --------------------
        for new_box in list_of_new_boxes:
            list_of_windows.append(Window(new_box, scaleFac, detectionRate, maxSpeed, frame, frame_HSV, frame_gray,
                                          feature_params))
        # ------------------------------------------------------------------------------------------------------


        # ----------------------------------------- Delete Purged Kalman windows -------------------------------------------
        for win in list_of_windows:
            if win.markForDel is True:
                list_of_windows.remove(win)
                # listOfDeletedPedestrians.append((win.id, win.color, win.appearanceHist))
                # if len(listOfDeletedPedestrians) > totalPedestriansToRemember:
                # del listOfDeletedPedestrians[0]

        # ---------------------------------------------------------------------------------------------------------

        # -------------------------------- Delete outgoing window and plot the rest -----------------------------------
        for i, win in enumerate(list_of_windows):
            cx = win.kalman.statePost[0]
            cy = win.kalman.statePost[1]
            #cv2.putText(frame, str(win.id), (int(cx - win.w / 2), int(cy - win.h / 2)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            if win_padding <= cx <= frame_width - win_padding \
                    and win_padding <= cy <= frame_height - win_padding:
                x = int(cx - win.w / 2)
                y = int(cy - win.h / 2)
                cv2.rectangle(frame, (x, y), (x + win.w, y + win.h), win.color, 2)
                win.resetMotion()
                if win.measurementType==0:
                    cv2.circle(frame, (cx, cy), 2, (255,0,0), thickness=2)
                elif win.measurementType==1:
                    cv2.circle(frame, (cx, cy), 2, (0, 255, 0), thickness=2)
                elif win.measurementType==2:
                    cv2.circle(frame, (cx, cy), 2, (0, 0, 255), thickness=2)
        # ------------------------------------------------------------------------------------------------------
        prev_gray = frame_gray
        #out.write(frame)
        cv2.imshow('Video', frame)
        cv2.waitKey(1)
        # ---------------------------------------------------------------------------------------------------------

    cap.release()
    cv2.destroyAllWindows()

if __name__ =='__main__':
    main()
