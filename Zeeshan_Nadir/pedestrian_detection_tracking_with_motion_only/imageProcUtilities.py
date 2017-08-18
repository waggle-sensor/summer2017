# import the necessary packages
import cv2
import numpy as np

def draw_detections(img, rects, thickness=3):
    for x, y, w, h in rects:
        # the HOG detector returns slightly larger rectangles than the real objects.
        # so we slightly shrink the rectangles to get a nicer output.
        pad_w, pad_h = int(0.15 * w), int(0.15 * h)
        cv2.rectangle(img, (x + pad_w, y + pad_h), (x + w - pad_w, y + h - pad_h), (0, 255, 0), thickness)


def draw_detections_using_corners(img, rects, thickness=1):
    for x1, y1, x2, y2 in rects:
        # the HOG detector returns slightly larger rectangles than the real objects.
        # so we slightly shrink the rectangles to get a nicer output.
        x1 = int(x1 + int(0.07 * x1))
        y1 = int(y1 + int(0.07 * y1))
        x2 = int(x2 - int(0.07 * x2))
        y2 = int(y2 - int(0.07 * y2))
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), thickness)


def inside(r, q):
    rx, ry, rw, rh = r
    qx, qy, qw, qh = q
    return rx > qx and ry > qy and rx + rw < qx + qw and ry + rh < qy + qh


def sliding_window(image, winStride, windowSize):
    for y in range(0, image.shape[0] - windowSize[1], winStride[1]):
        for x in range(0, image.shape[1] - windowSize[0], winStride[0]):
            yield (x, y, image[y:y + windowSize[1], x:x + windowSize[0]])


def pyramid(image, scale=1.5, minsize=(64, 128)):
    compoundScale = 1
    # yield the original image
    yield (image, compoundScale)

    while True:
        # updagte the compound scale so far
        compoundScale = compoundScale * scale
        # compute the new width
        w = int(image.shape[1] / scale)
        image = resize(image, width=w)
        # check if the image is larger than the smallest possible size
        if image.shape[0] < minsize[1] or image.shape[1] < minsize[0]:
            break
        # yield the next image
        yield (image, compoundScale)


def resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation=inter)

    # return the resized image
    return resized


def non_max_suppression(boxes, probs=None, overlapThresh=0.3):
    # if there are no boxes, return an empty list
    if len(boxes) == 0:
        return []

    # if the bounding boxes are integers, convert them to floats -- this
    # is important since we'll be doing a bunch of divisions
    if boxes.dtype.kind == "i":
        boxes = boxes.astype("float")

    # initialize the list of picked indexes
    pick = []

    # grab the coordinates of the bounding boxes
    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 2]
    y2 = boxes[:, 3]

    # compute the area of the bounding boxes and grab the indexes to sort
    # (in the case that no probabilities are provided, simply sort on the
    # bottom-right y-coordinate)
    area = (x2 - x1 + 1) * (y2 - y1 + 1)

    # if probabilities are provided, sort on them instead
    if probs is not None:
        idxs = probs

    # sort the indexes
    idxs = np.argsort(y2)

    # keep looping while some indexes still remain in the indexes list
    while len(idxs) > 0:
        # grab the last index in the indexes list and add the index value
        # to the list of picked indexes
        last = len(idxs) - 1
        i = idxs[last]
        pick.append(i)

        # find the largest (x, y) coordinates for the start of the bounding
        # box and the smallest (x, y) coordinates for the end of the bounding
        # box
        xx1 = np.maximum(x1[i], x1[idxs[:last]])
        yy1 = np.maximum(y1[i], y1[idxs[:last]])
        xx2 = np.minimum(x2[i], x2[idxs[:last]])
        yy2 = np.minimum(y2[i], y2[idxs[:last]])

        # compute the width and height of the bounding box
        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)

        # compute the ratio of overlap
        temp = np.minimum(area[i], area[idxs[:last]])
        overlap = (w * h) / temp

        # overlap = (w*h)/area[idxs[:last]]

        # delete all indexes from the index list that have overlap greater
        # than the provided overlap threshold
        idxs = np.delete(idxs, np.concatenate(([last], np.where(overlap > overlapThresh)[0])))

    # return only the bounding boxes that were picked
    return boxes[pick].astype("int")


def isOverLap(box1, box2, thresh):
    # This function accepts two boxes and returns True if they have an overlap more than the threshold
    x1 = np.maximum(box1[0] - box1[2] / 2, box2[0] - box2[2] / 2)
    y1 = np.maximum(box1[1] - box1[3] / 2, box2[1] - box2[3] / 2)
    x2 = np.minimum(box1[0] + box1[2] / 2, box2[0] + box2[2] / 2)
    y2 = np.minimum(box1[1] + box1[3] / 2, box2[1] + box2[3] / 2)

    # compute the width and height of the bounding box
    w = np.maximum(0, x2 - x1)
    h = np.maximum(0, y2 - y1)

    overlap_ratio = (w * h) / (np.minimum(box1[2] * box1[3], box2[2] * box2[3]))

    if (overlap_ratio > thresh):
        return True
    else:
        return False
