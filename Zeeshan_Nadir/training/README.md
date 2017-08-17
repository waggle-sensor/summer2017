# Training for Pedestrian Detection
This readme file explains the different python files in this subdirectory. Particularly, the two files that are described are the following:
1. [**train_ped_detection_with_hard_negative_mining** ](/Zeeshan_Nadir/training/train_ped_detection_with_hard_negative_mining.py)
2. [**pedestrian_detector** ](/Zeeshan_Nadir/training/pedestrian_detector.py)

For each of these two files, we need the following python modules:
- **cv2** 
- **numpy**

We also require a user defined module [**ped_detection_utilities**](/Zeeshan_Nadir/training/ped_detection_utilities.py) that has all the utility functions. We also optionally use **datetime** for timing calculations and **os** for the ease of reading training images from folders.

## 1. [**train_ped_detection_with_hard_negative_mining**](/Zeeshan_Nadir/training/train_ped_detection_with_hard_negative_mining.py)

