# Training for Pedestrian Detection
This readme file explains the different python files in this subdirectory. Particularly, the two files that are described are the following:
1. [**train_ped_detection_with_hard_negative_mining** ](/Zeeshan_Nadir/training/train_ped_detection_with_hard_negative_mining.py)
2. [**pedestrian_detector** ](/Zeeshan_Nadir/training/pedestrian_detector.py)


## 1. [**train_ped_detection_with_hard_negative_mining**](/Zeeshan_Nadir/training/train_ped_detection_with_hard_negative_mining.py)
For this file, we need the following python modules:
- **cv2** 
- **numpy**

We also require a user defined module [**ped_detection_utilities**](/Zeeshan_Nadir/training/ped_detection_utilities.py) that has all the utility functions. We also optionally use **datetime** for timing calculations and **os** for the ease of reading training images from folders.

This file doesn't receive it's input arguments from command line, although, it's straight forward to modify this file so that it can receive it's input arguments from command lines. There are a few important parameters that need to be specified for this file. We shall describe each of them.

Following are the parameters of the histogram of gradient features. 
```
winSize = (64, 128)
cellSize = (8, 8) 
blockSize = (16, 16)
blockStride = (8, 8)
nbins = 9
```

- **winSize** is to specify the size of the detection window for pedestrians
- **cellSize** is to specify the size of each cell over which a histogram of gradients is computed
- **blockSize** is to specify the size of each block used to normalize all the histograms that fall within this block
- **blockStride** is to specify the jump that we take to go from one small patch of the image to the next to compute the histograms
- **nbins** is to specify the number of bins that we use to discretize the ranges of angles/orientation of histograms
For more details about these parameters, please see [this](http://docs.opencv.org/2.4/modules/gpu/doc/object_detection.html).

Following are the parameters that are used to specify the paths of the input images for training:
```
path_of_pos_input_images 
path_of_neg_input_images
``` 

- **path_of_pos_input_images** is used to specify the path of positive training images (images containing pedestrians)
- **path_of_neg_input_images** is used to specify the path of negative training images (images not containing pedestrians)


Following is an outline of this code works:

- Obtains all the positive samples along with it's labels
- Obtains all the negative samples along with it's labels
- Concatenates the samples and the labels
- Trains the SVM model (can use to train both linear and non-linear SVM models)
- Saves the intial SVM model
- Finds false positive samples in the negative images
- Concatenates the false positive samples to the initial samples 
- Trains a final SVM model and saves it


## 2. [**pedestrian_detector**](/Zeeshan_Nadir/training/pedestrian_detector.py)
For this file, we need the following python modules:
- **cv2** 
- **numpy**

We also require a user defined module [**ped_detection_utilities**](/Zeeshan_Nadir/training/ped_detection_utilities.py) that has all the utility functions. We also optionally use **tkinter** for the ease of selecting a file from a graphical interface from the local file storage system. 

This code is primarily to test the trained SVM model for pedestrian detection. As such, this code has the same input parameters for the HOG feature set. Other than that, this code doesn't require any other input parameters. Following is the gernal outline of how this code works:

- Asks to select an input image
- Obtains an input image to test for pedestrian
- Scans the image at multiple scales/zoom levels and at multiple locations to look for pedestrians
- Uses the trained SVM model to decide if there is a pedestrian or not
- Uses the opencv's builtin pedestrian detector model as well to give a comparison
- Shows the images of detected pedestrians for both these models in separate windows


Note: The trained XML files corresponding to the SVM classifier for pedestrian detection can be found on DropBox.
