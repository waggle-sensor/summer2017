This folder contains all the files needed to run the pedestrian detection and tracking module. This consists of four files:

1. [**main**](/Zeeshan_Nadir/pedestrian_detection_and_tracking/main.py)
2. [**Window**](/Zeeshan_Nadir/pedestrian_detection_and_tracking/Window.py)
3. [**trackingUtilities**](/Zeeshan_Nadir/pedestrian_detection_and_tracking/trackingUtilities.py)
4. [**imageProcUtilities**](/Zeeshan_Nadir/pedestrian_detection_and_tracking/imageProcUtilities.py)

The modules that are required to run this code are given as follows:

- **numpy**
- **cv2**

## 1. [**main.py**](/Zeeshan_Nadir/pedestrian_detection_and_tracking/main.py)
The main function of this module is in the file [**main.py**](/Zeeshan_Nadir/pedestrian_detection_and_tracking/main.py). As such, the main function doesn't receive it's input parameters through command line arguments, although the code can be modified in a straight forward way so that the main function receives all it's input parameters from the command line. Right now, all the input parameters are given at the top of the file [**main.py**](/Zeeshan_Nadir/pedestrian_detection_and_tracking/main.py) and we shall give a brief description of them here.

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
Note that, here we are using two different sets of parameters for histogram of gradient features. This is because we use two different detector models for the window sizes of 128x64 and 64x32.

Other parameters that are being used in this file are given as follows:
```
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
# Weight of overlap vs weight of correlation
overlapWeightage = 0.9

# Overlap threshold
overlapThresh = 0.50

# Appearance Model Threshold
corrThresh = 0.15

# Threshold for discarding new boxes
threshForDiscarding = 0.40

# Detection Rate in units of frames per detection
detectionRate = 10

# pixel movement threshold
pixelMovThresh = 50

# Window deletion factor
win_padding = 10
```

Following is a brief discription about each of these parameters:

- **scaleFac** - The reduction in size of the box around the pedestrian to get the color histogram of the pedestrian. This is because, typically, the bounding box almost always have some background area as well. By descreasing it's width and height by a scale factor, we make sure that we mostly use the region that falls inside the body of the pedestrian.

- **detectScaleUp** - The factor by which we increase the size of the bounding box around the foreground objects. This is because we want to make sure that we do not miss any part of the pedestrian due to shortcomings of background subtractor. Therefore, we increase the width and height of the bounding box obtained from the background subtractor by a factor of *detectScaleUp* and then detect the pedestrian in relatively larger window.

- **maxSpeed** - The maximum speed in terms of pixels per frame for each of the pedestrians. This is to make sure that none of the pedestrian objects goes astray. *Note that in practice, this parameter should depend on the frame rate of the input capture device and the distance of the pedestrian from the camera.*

- **h_to_w** - The ratio of height to width of the foreground objects that background subtractor gives. We use this parameter to delete all the foreground objects whose height to width ratio is smaller than *h_to_w*. This is because, we expect that typically, the height of pedestrians is more than twice as much their width. We typically set this anywhere between 1.3 to 1.5.
*This parameter may have to be tweaked a bit or completely taken out if shadows are messing with the suggested proposal regions for finding pedestrians by the background subtractor*

- **kSize** - The kernel size. This parameter is used to specify the diameter of the structure element in the morphological operations of erosion and dilation. This parameter can be tweaked depending upon the resolution of the input images and the distance of the pedestrians from the camera.

- **overlapThresh** - Overlap threshold. In order to map new pedestrian windows to old ones, we require a certain amount of threshold. If the overlap area is smaller than the set threshold given by *overlapThresh* then we don't map the existing pedestrian to this new location.

- **corrThresh** - Correlation threshold. In order to map new pedestrian windows to the old onws, we require that their appearance model have similarity more than a set threshold level given by *corrThresh*. When we acquire a new pedestrian window, we take it's color histogram and take a dot product with the existing pedestrians color histogram. This dot product should be more than *corrThresh* for them to be matched.

- **threshForDiscarding** - Threshold for discarding new windows. As we acquire each frame, we perform pedestrian detection in the regions where we sensed motion. Now, some of these pedestrians might be new, however, others are just existing pedestrians. We treat all pedestrians as an instance of existing pedestrian if they have an overlap of more than *threshForDiscarding* with any existing pedestrian. 

- **detectionRate** - Detection rate for detecting pedestrians. This parameter specifies the number of frames after which we do a detection step for each pedestrian window. Before *detectionRate* number of frames, we keep using KLT tracker.

- **pixelMovThresh** - Pixel move threshold. When we match new pedestran windows to the existing ones, we want to make sure that the motion of pedestrians is not abrupt. Therefore, the parameter *pixelMovThresh* specifies the maximum change in the x and y coordinates of the pedestrians that is allowed. This parameter may serve a role similar to *overlapThresh* and can be further investigated for it's utility.

- **win_padding** - Window padding. This parameter is used to specify the margin after which we don't consider the foreground object as a valid pedestrian. So as the x, y coordinate of the foreground objects given by background subtractror becomes smaller than *win_padding* or larger than *width - win_padding* or *height - win_padding*, we do not consider these foreground objects. This parameter needs to be investigated more for it's utility.

## 2. [**Window.py**](/Zeeshan_Nadir/pedestrian_detection_and_tracking/Window.py)
This module contains the code for the Window class that we have created to manage all the pedestrians. Each pedestrian is represented by an object of the clas Window. First we describe the attributes of this class and then we shall briefly describe it's important methods.

Following are the parameters related to the Kalman Filter for each pedestrian.
```
self.kalman = cv2.KalmanFilter(4, 2)
self.kalman.measurementMatrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0]], np.float32)
self.kalman.transitionMatrix = np.array([[1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1]], np.float32)
self.kalman.processNoiseCov = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], np.float32) * 0.03
self.kalman.measurementNoiseCov = np.array([[1, 0], [0, 1]], np.float32) * 0.0003
```
The meaning of each of these parameters is evident from their names. For more details about Kalman filter, see [this](http://docs.opencv.org/trunk/dd/d6a/classcv_1_1KalmanFilter.html).

Other parameters are given as follows:


- **w** - Width of the pedestrian bounding box 
- **h** - Height of the pedestrian bounding box
- **maxSpeed** - Maximum speed of each window object (in units of pixels per frame)
- **detectionRate** - Detection rate in units of frames per detection
- **counter** - Counter for counting the frames for each pedestrian
- **measurement** - Variable for acquiring measurements from detections or KLT tracker
- **roiHist** - Variable for Hue and Saturation histogram of the pedestrian
- **appearanceHist** This variable is similar to *roiHist*, except that it's flattened out as a 1D array
- **color** - Color of the bounding box of the pedestrian
- **markForDel** - Boolean variable to delete the current pedestrian
- **isWindowMoving** - Boolean variable to keep track of if the pedestrian is moving or not 
- **ctrWithoutMotion** - Counts the number of frames without getting a measurement from detection or KLT tracker
- **ctrWithoutMotionThresh** - Threshold for maximum number of frames a pedestrian can go without getting any kind of measurement at all
- **measurementType** - Variable that changes the color of the centroid of the bounding box to indicate if it is getting updated by a detection, KLT tracker or simply by a prediction. If the pedestrian object gets it's measurement by a detection, we display a blue dot, if it receives measurement by KLT tracker, we use a green dot, if it doesn't receive any measurement and we are simply updating using prediction, then we display a red dot.

Following are the parameters of the window class that pertain to the KLT tracker.
- **tracks** - This variable stores all the path of the feature points
-**countAfterLastDetection** - Counter after the last time the pedestrian received a detection
- **detectCtrThresh** - Threshold after which we stop using a KLT tracker
- **track_len** - Number of times of the past locations for each feature point
- **totalPtsThresh** - Minimum number of feature points required in KLT tracker to track the location
- **pixelThreshForPurgingPts** - This is a parameter used in KLT tracking to get rid of feature points that don't appear to be well tracked
- **totalPts** - Total number of feature points being tracked

Following are the most notable methods of the class Window:

- **predict** - This function is used to predict the location of the pedestrian. It helps in smoothing out the trajectory of the pedestrians as well as keeping track of the motion when we don't have a detection or KLT tracker based measurement available for the pedestrians.

- **correct** - This function is used to correct the location of the pedestrians by incorporating a measurement either by a detection or KLT tracker.


To get more details about the algorithm used to track pedestrians, please see this [documentation](/Zeeshan_Nadir/readme.md)
