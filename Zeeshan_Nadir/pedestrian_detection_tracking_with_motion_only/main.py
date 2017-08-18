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
    hog = cv2.HOGDescriptor(winSize, blockSize, blockStride, cellSize, nbins)
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    # scale factor for reduction of box size for CAMShift
    scaleFac = 0.70

    # height to width ratio to purge windows
    h_to_w = 1.3


    # Capture the video and set the frame size
    cap = cv2.VideoCapture("C:\\Users\\Zeeshan Nadir\\Documents\\Argonne\\Pedestrian_Detection_Tracking\\data\\passageway.avi")
    #frame_height = 360
    #frame_width = 640
    #cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    #cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    #frame_width =  int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    #frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    #cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    #cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

    # Video Writer object
    #out = cv2.VideoWriter(".\\data\\results.avi", -1, fps, (800, 640))

    # create background subtraction object
    fgbg = cv2.createBackgroundSubtractorMOG2()

    # Kernels for morphological operations
    kSize = 3
    kernelO = np.ones((kSize, kSize), np.uint8)
    kernelC = np.ones((kSize, kSize), np.uint8)

    # Overlap threshold
    overlapThresh = 0.40
    thresh_for_old = 0.90
    # pixel movement threshold
    pixelMovThresh = 100

    # Window deletion factor
    win_padding = 5

    # List of window objects
    list_of_windows = list()
    counter = 0;

    # Initial condition for all the new windows
    list_of_new_boxes = list()
    while True:
        counter = counter + 1
        print("Frame = ", counter, "Windows Tracked =", len(list_of_windows))
        # -------------------------- grab the current frame ----------------------------------------------------
        ret, frame = cap.read()

        if frame is None:
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        frame = utils.resize(frame, 800)

        frame_width = frame.shape[1]
        frame_height = frame.shape[0]

        frame_area = frame_height * frame_width
        frame_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # --------------------------------------------------------------------------------------------------------

        # ------------------------------------------- background subtraction ------------------------------------
        fgmask = fgbg.apply(frame)
        ret, fgmask = cv2.threshold(fgmask, 0, 255, 0)
        opening = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernelO, iterations=2)
        sure_fg = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernelC, iterations=2)
        (_, contours, _) = cv2.findContours(sure_fg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # --------------------------------------------------------------------------------------------------------

        # ---------------------------------- Get the list of new boxes -------------------------------------------
        list_of_new_boxes = track.giveContours(contours, frame_area, frame_width, frame_height, h_to_w, win_padding,
                                         0.003, 0.20)
        # ---------------------------------------------------------------------------------------------------------

        # ----------------------------- Predict the kalman windows ------------------------------------------------
        for win in list_of_windows:
            win.predict()

        # ----------------------------- Correct Kalman Windows for moving objects ----------------------------------
        if len(list_of_new_boxes) > 0:
            pairs = track.givePairs(list_of_windows, list_of_new_boxes, pixelMovThresh, overlapThresh, frame_HSV)
            for k in pairs:
                cx, cy, w, h = list_of_new_boxes[k[0]]
                measurement = np.array([ [cx], [cy], [w], [h]], dtype = np.float32)
                #list_of_windows[k[1]].predict()
                list_of_windows[k[1]].correct_with_new_motion(measurement)
            # ------------------------------------------------------------------------------------------------------

        # ------------------------ Correct Kalman Windows for stationary objects -------------------------------
        #for win in list_of_windows:
        #    if win.isWindowMoving ==False:
        #        win.correct_with_color(pixelMovThresh, frame_HSV)
        # -------------------------------------------------------------------------------------------------------

        # ------------------------ Correct Kalman Windows for moving objects ----------------------------------
        if len(list_of_new_boxes)>0:
            mark_new_boxes_for_del = list()
            for k in pairs:
                mark_new_boxes_for_del.append(k[0])

            list_of_new_boxes = [i for j, i in enumerate(list_of_new_boxes) if j not in mark_new_boxes_for_del]
        # ------------------------------------------------------------------------------------------------------

        if len(list_of_new_boxes)>=1:
            list_of_new_boxes = track.purgeNewWindowsForPedDetection(list_of_new_boxes, win_W, win_H, frame, hog, 1.50)

        # ------------------------ Add all the new windows in the current list --------------------
        for new_box in list_of_new_boxes:
            list_of_windows.append(Window(new_box, scaleFac, frame_HSV))
        # ------------------------------------------------------------------------------------------------------


        # ------------------------ Delete all the old windows that overlap ---------------- --------------------
        if len(list_of_windows) > 1:
            mark_for_del = track.deleteOverlappingOldWindows(list_of_windows, thresh_for_old)
            list_of_windows = [i for j, i in enumerate(list_of_windows) if j not in mark_for_del]
        # ------------------------------------------------------------------------------------------------------

        # ------------------------------------------ Purge existing kalman windows -----------------------------
        if len(list_of_windows) >=1:
            track.purgeExistingWindowsForPedDetection(list_of_windows, win_W, win_H, frame, hog, 1.20)

        # ----------------------------------------- Purge Kalman windows -------------------------------------------
        if len(list_of_windows)>=1:
            track.purgeAllKalmanWindowsForDeletion(list_of_windows, frame_width, frame_height, win_padding)
        for win in list_of_windows:
            if win.markForDel is True:
                list_of_windows.remove(win)
        # ---------------------------------------------------------------------------------------------------------

        # -------------------------------- Delete outgoing window and plot the rest -----------------------------------
        for i, win in enumerate(list_of_windows):
            cx = win.kalman.statePost[0]
            cy = win.kalman.statePost[1]
            if win_padding<=cx<=frame_width-win_padding \
                    and win_padding<=cy<=frame_height-win_padding:
                w = win.kalman.statePost[2]
                h = win.kalman.statePost[3]
                x = int(cx - w/2)
                y = int(cy - h/2)
                cv2.rectangle(frame, (x, y), (x + w, y + h), win.color, 2)
                cv2.circle(frame, (cx, cy), 2, win.color, thickness=2)
                win.resetMotion()
        # ------------------------------------------------------------------------------------------------------

        #if counter > 380:
        #    out.write(sure_fg)

        cv2.imshow('Original', frame)
        cv2.imshow('Sure Foreground', sure_fg)
        cv2.waitKey(1)

        #plt.imshow(frame)
        #sleep(5 / 1000.0);
        #plt.close()
    #out.release()
    cap.release()
    cv2.destroyAllWindows()

if __name__ =='__main__':
    main()