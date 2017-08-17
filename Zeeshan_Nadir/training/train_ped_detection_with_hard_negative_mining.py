import numpy as np
import cv2
import datetime
import os
import ped_detection_utilities as imutils

class StatModel(object):
    def load(self, fn):
        self.model.load(fn)  # Known bug: https://github.com/opencv/opencv/issues/4969
    def save(self, fn):
        self.model.save(fn)

class SVM(StatModel):
    def __init__(self, C = 0.01, gamma = 0.5):
        self.model = cv2.ml.SVM_create()
        self.model.setGamma(gamma)
        self.model.setC(C)
        self.model.setKernel(cv2.ml.SVM_LINEAR)
        self.model.setType(cv2.ml.SVM_C_SVC)

    def train(self, samples, responses):
        self.model.train(samples, cv2.ml.ROW_SAMPLE, responses)

    def predict(self, samples):
        return self.model.predict(samples)[1].ravel()


def pyramid(image, scale = 1.5, minsize=(64, 128)):
    compundScale = 1
    # yield the original image
    yield (image, compundScale)
    while True:
        # updagte the compound scale so far
        compundScale = compundScale * scale
        # compute the new width
        w = int(image.shape[1]/scale)
        image = imutils.resize(image, width = w)
        # check if the image is larger than the smallest possible size
        if image.shape[0]< minsize[1] or image.shape[1] < minsize[0]:
            break
        # yield the next image
        yield (image, compundScale)

def sliding_window(image, winStride, windowSize):
    for y in range(0, image.shape[0]-windowSize[1], winStride[1]):
        for x in range(0, image.shape[1]-windowSize[0], winStride[0]):
            yield (x, y, image[y:y+windowSize[1], x:x+windowSize[0]])


def preProcess(img):
    # This is a function which is quite arbitray
    # In particular it depends on what kind of data you are reading
    # This function should be customized to different training sets
    img = img[17:145, 17:81, :]
    return img

def collectINRAPosSamples(path_of_input_images, featureLength, hog):
    # path_of_input_images is the path of the input images
    # featureLenght is the length of the features
    # hog is the HOGDescriptor

    # Get the list of all files
    list_of_file_names = os.listdir(path_of_input_images)
    samples = np.zeros((len(list_of_file_names), featureLength), dtype=np.float32) # form the samples matrix

    for counter, fileName in enumerate(list_of_file_names):
        path_to_file = os.path.join(path_of_input_images, fileName)
        img = cv2.imread(path_to_file)
        img = preProcess(img)
        h = hog.compute(img)
        samples[counter,:] = h.reshape(-1,h.shape[0])
    return samples


def collectINRANegSamples(path_of_input_images, winW, winH, featureLength, hog):
    # path_of_input_images is the path of the input images
    # featureLenght is the length of the features
    # hog is the HOGDescriptor

    no_of_windows_per_image = 10 # number of negative windows sampled from each image
    list_of_files = os.listdir(path_of_input_images)

    samples = np.zeros((len(list_of_files)*no_of_windows_per_image, featureLength), dtype=np.float32)
    counter = 0

    xIndex = np.zeros((1), dtype=np.int32)
    yIndex = np.zeros((1), dtype=np.int32)

    for names in list_of_files:
        fileName = os.path.join(path_of_input_images, names)
        for i in range(no_of_windows_per_image):
            img = cv2.imread(fileName)

            # generate a random index inside the image
            cv2.randu(xIndex, 0, img.shape[0]-winH)
            cv2.randu(yIndex, 0, img.shape[1]-winW)
            # get a window of 128x64 image

            img_H_W = img[xIndex[0]:xIndex[0]+winH, yIndex[0]:yIndex[0]+winW, :]

            # get the hog descriptor
            h = hog.compute(img_H_W)

            # append this to the samples file
            samples[counter, :] = h.reshape(-1, h.shape[0])
            counter = counter + 1
    return samples

def findFalsePositiveSamples(path_of_neg_images, max_num_of_false_pos_per_image, featureLength, scale, winStride, winW, winH, hog, SVM_Object):
    list_of_files = os.listdir(path_of_neg_images)
    totalFiles = len(list_of_files)
    # Variable for False Positive Feats
    falsePFeats = np.empty((1,featureLength), dtype=np.float32)
    for k, names in enumerate(list_of_files):
        if k%200 == 0:
            print ('\r', int((k/totalFiles)*100), 'percent complete')

        counter = 0
        fileName = os.path.join(path_of_neg_images, names)
        img = cv2.imread(fileName)
        for (resized_img, overall_scale) in pyramid(img, scale):
            if counter == max_num_of_false_pos_per_image:
                break
            for (x, y, window) in sliding_window(resized_img, winStride, (winW, winH)):
                # compute hog feature
                h = hog.compute(window)
                h = h.reshape(-1, h.shape[0])
                label = SVM_Object.model.predict(h)
                if label[1] == 1:
                    falsePFeats = np.concatenate((falsePFeats, h))
                    counter = counter + 1
                if counter == max_num_of_false_pos_per_image:
                    break
    labelsForFalsePosSamples = np.zeros((falsePFeats.shape[0]-1), dtype=np.int32) # 1 subtracted to account for initial empty entry
    labelsForFalsePosSamples.fill(-1)
    return falsePFeats[1:, :], labelsForFalsePosSamples # 1 sample discarded to account for initial empty entry

def main():
    beginingOfTime = datetime.datetime.now()

    # HOG descriptor
    winSize = (64, 128); blockSize = (16, 16); blockStride = (8, 8); cellSize = (8, 8); nbins = 9
    hog = cv2.HOGDescriptor(winSize, blockSize, blockStride, cellSize, nbins)

    # compute the feature vector length
    featureLength = int(nbins * (blockSize[0] / cellSize[0]) * (blockSize[1] / cellSize[1]) \
                        * (winSize[0] / blockStride[0] - 1) * (winSize[1] / blockStride[1] - 1))

    # Collect positive samples
    start = datetime.datetime.now()
    print('Obtaining Positive/Negative Samples for Training ... Please be patient!!!')
    path_of_pos_input_images ='C:\\Users\\Zeeshan Nadir\\Documents\\Argonne\\INRIAPerson\\train_64x128_H96\\pos'
    pos_samples = collectINRAPosSamples(path_of_pos_input_images, featureLength, hog)

    # Collect negative samples
    path_of_neg_input_images = 'C:\\Users\\Zeeshan Nadir\\Documents\\Argonne\\INRIAPerson\\train_64x128_H96\\neg\\'
    neg_samples = collectINRANegSamples(path_of_neg_input_images, winSize[0], winSize[1], featureLength, hog)

    # Concatenate negative and positive samples
    samples = np.concatenate((pos_samples, neg_samples))

    y_pos = np.zeros((pos_samples.shape[0]), dtype=np.int32)
    y_pos.fill(1)

    y_neg = np.zeros((neg_samples.shape[0]), dtype=np.int32)
    y_neg.fill(-1)

    y_labels = np.concatenate((y_pos, y_neg))

    # Write out the original samples on a binary file
    outFile = open('.//original_samples.dat', 'wb')
    np.save(outFile, samples)
    outFile.close()

    # Write out the original labels on a binary file
    outFile = open('.//original_labels.dat', 'wb')
    np.save(outFile, y_labels)
    outFile.close()
    end = datetime.datetime.now()

    print("[INFO] Total Time in computing features of original samples: {}s\n".format(
        (end-start).total_seconds()))

    # ------------------------- Add your custom training set here ----------------------
    # customSamples <----- Custom Training Samples
    # customLabels  <----- Put 1s and 0s for positive and negative labels
    # samples = np.concetenate((samples, customSamples))
    # y_abels  = np.concatenate((y_labels, customLabels))
    # The other way of doing this is to simply put your samples in the training folders for negative and positive training images
    # ---------------------------------------------------------------------------

    # Training the initial SVM Classifier
    print('Training the initial SVM classifier ... Please be patient!!!')
    start = datetime.datetime.now()
    SVM_Object = SVM()
    SVM_Object.train(samples, y_labels)
    end = datetime.datetime.now()
    print("[INFO] Total Time in Computing Features of Initial Samples: {}s\n".format(
        (end-start).total_seconds()))

    # Save the linear classifier without the hard negative mining
    print('Saving the Initial SVM Classifier ... Please be patient!!!')
    start = datetime.datetime.now()
    SVM_Object.save("./model_linear.xml")
    end = datetime.datetime.now()
    print("[INFO] Total Time in Saving the Initial SVM Classifier: {}s\n".format(
        (end-start).total_seconds()))

    # Find the false positives
    print('Finding the False Positives to Perform Hard Negative Mining... Please be patient!!!')
    start = datetime.datetime.now()
    max_num_of_false_pos_per_image = 10
    scale = 1.2
    winStride = (4,4)
    falsePosSamples, labelsForFalsePosSamples = findFalsePositiveSamples(path_of_neg_input_images,
                                                                         max_num_of_false_pos_per_image, featureLength, scale,
                                                                         winStride, winSize[0], winSize[1], hog, SVM_Object)

    finalSamples = np.concatenate((samples, falsePosSamples))
    finalLabels  = np.concatenate((y_labels, labelsForFalsePosSamples))
    end   = datetime.datetime.now()
    print("[INFO] Total Time in Finding and Appending the False Positive Samples: {}mins\n".format(
        int((end - start ).total_seconds()/60)) )

    # Train the SVM Classifier with Hard Negative Mining
    start = datetime.datetime.now()
    print('Training the Final SVM classifier with Hard Negative Mining... Please be patient!!!')
    SVM_Object.train(finalSamples, finalLabels)
    end = datetime.datetime.now()
    print("[INFO] Total Time in Training the Final SVM Classifier: {}s\n".format(
        (end-start).total_seconds()))

    # Save the linear classifier without the hard negative mining
    print('Saving the Final SVM Classifier ... Please be patient!!!')
    start = datetime.datetime.now()
    SVM_Object.save("./model_linear_with_hard_neg_mining_128_64.xml")
    end = datetime.datetime.now()
    print("[INFO] Total Time in Saving the Final SVM Classifier: {}s\n".format(
        (end-start).total_seconds()))

    print("[INFO] Total Time in All the Procedure: {}mins".format(
        int((end - beginingOfTime ).total_seconds()/60)) )

if __name__ == '__main__':
    main()
