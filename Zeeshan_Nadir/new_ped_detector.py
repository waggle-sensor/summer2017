import numpy as np
import cv2
import datetime
import ped_detection_utilities as utils
import tkinter as tk
from tkinter import filedialog

def main():
    winH = 128
    winW = 64

    # load the SVM model
    model = cv2.ml.SVM_load(".//model_linear_with_hard_neg_mining_128_64.xml")

    # Make an HOG Descriptor
    # HOG descriptor
    winSize = (64, 128)
    blockSize = (16, 16)
    blockStride = (8, 8)
    cellSize = (8, 8)
    nbins = 9
    hog  = cv2.HOGDescriptor(winSize, blockSize, blockStride, cellSize, nbins)
    hog2 = cv2.HOGDescriptor(winSize, blockSize, blockStride, cellSize, nbins)
    hog2.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    print("Beginning testing pedestrian detection algorithm")
    while True:
        #name_of_test_image = input("Enter the name of test image with extension:")
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()
        img = cv2.imread(file_path)
        #img = utils.resize(img, width=min(350, img.shape[1]))
        img = utils.resize(img, width=350)
        if img is None:
            continue

        # Variable for box
        boxes = np.empty((1, 4), dtype=np.int)

        start = datetime.datetime.now()
        for (resized_img, overall_scale) in utils.pyramid(img, 1.2):
            for (x, y, window) in utils.sliding_window(resized_img, (4, 4), (winW, winH)):
                #if window.shape[0] != winH or window.shape[1] != winW:
                #    continue
                # compute hog feature
                h = hog.compute(window)

                label = model.predict(h.reshape(-1, h.shape[0]))
                if label[1] == 1:
                    temp = overall_scale*np.array([[x, y, x+winW, y+winH]],dtype=np.int)
                    boxes = np.concatenate((boxes, temp))

        boxes = boxes[1:,:]

        filtered_boxes = utils.non_max_suppression(boxes, probs=None, overlapThresh=0.60)
        print(filtered_boxes)
        print("[INFO] detection before ] took: {}s".format(
            (datetime.datetime.now() - start).total_seconds()))

        clone = img.copy()
        utils.draw_detections_using_corners(img, filtered_boxes, 3)

        cv2.imshow('img using my detector', img)

        start = datetime.datetime.now()
        found, w = hog2.detectMultiScale(clone, winStride=(4, 4), padding=(16, 16), scale=1.2)
        print(found)
        utils.draw_detections(clone, found)
        cv2.imshow('img using default detector', clone)
        print("[INFO] detection before ] took: {}s".format(
            (datetime.datetime.now() - start).total_seconds()))

        ch = cv2.waitKey()

        cv2.imwrite('my_custom_detector.jpg', img)
        cv2.imwrite('openCV_detector.jpg', clone)

if __name__ == '__main__':
    main()