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
```
