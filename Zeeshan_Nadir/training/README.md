# Training for Pedestrian Detection
This readme file explains the different python files in this subdirectory. Particularly, the two files that are described are the following:
1. [**train_ped_detection_with_hard_negative_mining** ](/Zeeshan_Nadir/training/train_ped_detection_with_hard_negative_mining.py)
2. [**pedestrian_detector** ](/Zeeshan_Nadir/training/pedestrian_detector.py)

For each of these two files, we need the following python modules:
- **cv2** 
- **numpy**

We also require a user defined module [**ped_detection_utilities**](/Zeeshan_Nadir/training/ped_detection_utilities.py) that has all the utility functions. We also optionally use **datetime** for timing calculations and **os** for the ease of reading training images from folders.

## 1. [**train_ped_detection_with_hard_negative_mining**](/Zeeshan_Nadir/training/train_ped_detection_with_hard_negative_mining.py)
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
- **nbies** is to specify the number of bins that we use to discretize the ranges of angles/orientation of histograms
For more details about these parameters, please see [this](http://docs.opencv.org/2.4/modules/gpu/doc/object_detection.html).

Following are the parameters that are used to specify the paths of the input images for training:
```path_of_pos_input_images``` 
```path_of_neg_input_images``` 

-**path_of_pos_input_images** is used to specify the path of positive training images (images containing pedestrians)
-**path_of_neg_input_images** is used to specify the path of negative training images (images not containing pedestrians)


