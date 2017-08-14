# Pedestrian Detection and Tracking using Kalman Filter and KLT Tracker

Pedestrian detection and tracking is an important problem in the field of computer vision and is still being researched. Similar it may sound, but pedestrian detection and tracking are two separate problems. In this description, I shall discuss both the two problems, give a brief literature survey and then describe the approach that I have taken to tackle these problems.

Generally, a basic object detection problem is defined as finding a given object of interest in any given image of a fixed size. Therefore, given an image of predefined size, the object detector must decide if the image is of the object of interest or not. However, in practice, real images can have the objects of interest in any possible location inside the image. Morever, the size of the object in real images need not be equal to the predefined size, that is, the object can be at different scale levels (zoom levels) inside the image. In order to cope with this, we use a basic object detector and use sliding window and scale space to try to detect objects inside the images.

