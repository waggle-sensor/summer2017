# Pedestrian Detection and Tracking using Kalman Filter and KLT Tracker

## Introduction
Pedestrian detection and tracking is an important problem in the field of computer vision and is still being researched. Similar it may sound, but pedestrian detection and tracking are two separate problems. In this description, I shall discuss both the two problems, give a brief literature survey and then describe the approach that I have taken to tackle these problems. I shall then provide a unified framework for pedestrian detection and tracking in real time video sequences.

Pedestrian detection and tracking problem is defined as keeping track of existing pedestrians in the video and finding new pedestrians as they become visible. Typically, the detection part is posed as a machine learning problem where a set of features are chosen to distinguish between pedestrian and non-pedestrian images and are then fed to a classifier such as [Support Vector Machines](http://docs.opencv.org/2.4/modules/ml/doc/support_vector_machines.html). In 2005, Navneet and Dalal popularized [Histogram of gradients (HOG)](https://lear.inrialpes.fr/people/triggs/pubs/Dalal-cvpr05.pdf) as a set of features for their effectivity in pedestrian detection problems. In this paper, we shall use HOG based pedestrian detector along with a linear Support vector machine to detect pedestrians. Major challenges that are faced in pedestrian detection are occlusion, non-rigid nature of pedestrians and slanted pose angles of pedestrians with respect to the camera. The result of these challenges are missed detections (false negatives) and detections of non-pedestrian regions of images as pedestrians (false positives).

Once an object is detected in a particular frame of a video sequence, we want to keep a track of this detected object. Therefore, as we receive new frame, we want to mark the location of the pedestrians in earlier frames. Major challenges of tracking the pedestrians in videos include partial and full occlusion, abrupt motion of pedestrians, changing appearance of objects due to change in pose, illumniation etc., changing appearance of the scene, non-rigid object structures. Furthermore, because of such challenges, we may also have missed detections of already existing pedestrians in the video. The result of these challenges is abrupt stops in the tracks of pedestrians, abrupt changes in the tracks of pedestrians, noisy tracks and missing tracks. 

In order to tackle the challenges faced in tracking the pedestrians, pedestrian tracking methods typically incorporate dynamic models and appearance models. Dynamic models help in missing the "gaps" in the tracks of predictions for example in case of occlusion or missed detections. They also help in smoothing out the track of pedestrians. In essence, dynamic models constrain the motion of the pedestrians by using prior information in terms of how the pedestrians move e.g., linear motion models assume a constant velocity. This may or may not be a very accurate assumption, however, it tends to be a good model especially for making predictions near in time. In contrast to dynamic models, appearance models define the apperance of the object in terms of features that can be computed inexpensively. Color histograms and corner points are popular features that are used in apperance models. The main purpose of appearance models is to solve the data association problem i.e., given multiple detections in frame n, how do we associate these detections with the existing pedestrians from frame n-1. In this work, I shall use both dynamic model and appearance model to track pedestrians. The following flow chart gives provides a visual description of how each of these two models are used in tracking.

![picture3](https://user-images.githubusercontent.com/29146711/29339017-ccfef8c0-81dd-11e7-852c-44a6f59c8680.png)

The rest of the read me documentation is organized as follows:
1. Pedestrian Detection
2. Background Subtraction
3. Pedestrian Tracking using Kalman Filtering and Kanade Lucas Tomasi (KLT) Tracker
4. Detection and Tracking Algorithm
5. Results

## Pedestrian Detection using HOG Features and Linear SVM
Generally, a basic object detection problem is defined as finding a given object of interest in any given image of a fixed size. Therefore, given an image of predefined size, the object detector must decide if the image is of the object of interest or not. However, in practice, the size of the object in real images need not be equal to the predefined size, that is, the object can be at different scale levels (zoom levels) inside the image. Moreover, real images can have the objects of interest in any possible location inside the image i.e., at different coordinates inside the image. In order to cope with this, we use a basic object detector and use sliding window and scale space to try to detect objects inside the images. In the context of pedestrian detection, what this means is that given any monocular image that may or may not contain pedestrians, we want to detect pedestrians inside this image and indicate it's location by drawing a (preferably tight) bouding box around the pedestrian. One of the most popular method to detect pedestrians is based on [Histogram of Gradients (HOG)](https://lear.inrialpes.fr/people/triggs/pubs/Dalal-cvpr05.pdf) by Navneet and Dalal. We shall be using HOG in our work to detect pedestrians. 

The following block diagram gives a brief overview of pedestrian detection pipeline.

![picture1](https://user-images.githubusercontent.com/29146711/29368654-fb9db90e-8265-11e7-8ec5-34d1047917e7.png)
Given an input image, we extract some features that help us discriminate between pedestrians/non-pedestrian images. Next, we feed it to our SVM classifier (must be trained by us offline) and then finally we get our decision if it's a pedestrian or not. 

### Feature Extraction
We use the Histogram of Gradient features for pedestrian detection. In simple words, these features use the information in the edges of the images to distinguish between pedestrian and non-pedestrians. This makes a lot of sense, since for pedestrian images, gradients have a lot of information in them as opposed to smooth images. One could expect a lot of vertical gradients in pedestrian images because of the edges of torso, legs, and arms. Though we shall be using opencv's ``` hog ``` class, however, I think it's instructive to give a brief description of how it works.
- Compute the gradient of the input image
- Divide the input image in different cells and blocks (blocks are larger than cells)
- Compute the a histogram of gradients corresponding to these cells
- Normalize the histogram of gradients in each cell using the corresponding block
- Combine the histogram of gradients from all the cells to make the feature vector
 
An example of gradient images from an image of a pedestrian (guess who this person is?) is shown below.
![picture5](https://user-images.githubusercontent.com/29146711/29377799-87ff619c-8282-11e7-97b6-4742c6859b95.png)

It can be seen that it's still easy for a human to tell that it's a pedestrian's image simply by looking at the gradient images.
The green boxes represent different cells in which we have divided our image into. In this particular example, we are using the most popular 8x8 cells. The blue box represents a block. In this particular example, we have chosen a block size of 4x4 cells.
An example of computed features of a single 8x8 cell is shown below.
![picture4](https://user-images.githubusercontent.com/29146711/29377824-9b7da4d6-8282-11e7-8209-938c5d1bc028.png)
The matrix on the left hand side represents the direction of the gradient and the matrix on the right hand side represents the corresponding magnitude. In order to get the histogram, we divide the angles in a set number of bins. For example, in the given example, we use 9 bins and each magnitude gradient is assigned to a bin or two based upon their angle. More details about this can be found [here](http://www.learnopencv.com/histogram-of-oriented-gradients/). 

All of this can be performed using the opencv library functions. Following code snippet gives an example of computing the HOG features for a given image:
```
winSize = (64, 128)
blockSize = (16, 16)
blockStride = (8, 8)
cellSize = (8, 8)
nbins = 9
hog  = cv2.HOGDescriptor(winSize, blockSize, blockStride, cellSize, nbins)
h = hog.compute(image)
```
### Training the SVM Classifier
I shall be using the linear SVM classifier to classify between pedestrian/non-pedestrian images. The training consists of two major parts. First part is the initial set of training with a large number of positive (images containing pedestrians) and negative (images not containing pedestrians). Once the first round of training is done, next step is called "Hard Negative Mining". This consists of getting rid of false positive detections i.e., detecting a pedestrian when there is actually none. The way this works is that, after our first set of training, we run our initial classifier on all the negative images and save all the windows/regions where the model thinks we have a pedestrians. We then re-feed these windows/regions in to our training set and re-train the model. This has an effect of essentially telling the classifier that there isn't a pedestrians in these images and therefore, it shouldn't detect one. The file [**train_ped_detection_with_hard_negative_mining** ](/Zeeshan_Nadir/train_ped_detection_with_hard_negative_mining.py) contains the code that can be used to train an SVM classifier for pedestrian detection with hard negative mining. 

The two variables that are most important in this code are **path_of_pos_input_images** and **path_of_neg_input_images**. These variables are used to pass the paths of positive and negative training images. In this example, we are using the [INRIA](http://pascal.inrialpes.fr/data/human/) training dataset. The final outcome of this code is in the form of an XML file that stores the SVM model's parameters. This XML file can later be read to load the SVM model and used for the purposes of detecting pedestrians.

Note that since we are working with a pedestrian detection window of 128x64, therefore, depending upon the image database that we are using for training, we may have to pre-process our training images to make sure we have pedestrian images of size 128x64 which are aligned roughly in the center of this 128x64 window. The following code snippet shows the **preProcess** function that we are using inside the file [**train_ped_detection_with_hard_negative_mining** ](/Zeeshan_Nadir/train_ped_detection_with_hard_negative_mining.py):
```
def preProcess(img):
    # This is a function which is quite arbitray
    # In particular it depends on what kind of data you are reading
    # This function should be customized to different training sets
    img = img[17:145, 17:81, :] 
    return img
```
### Detecting Pedestrians in Images
After training the SVM classifier with HOG features, the next natural step is to detect pedestrians in images. The file [new_ped_detector.py](/Zeeshan_Nadir/new_ped_detector.py) contains the code that can be used to detect pedestrians in images. It includes the module named **tkinter** that helps the user select an arbitrary image file and then uses the opencv's default pedestrian detector as well as our trained detector from the previous section to detect pedestrians. An example of results from our pedestrian detector is given as follows:
![picture6](https://user-images.githubusercontent.com/29146711/29382250-98ef552a-8291-11e7-9ca2-a9dc95562f02.png)

## Background Subtraction
In practice, however, performing detection on each of the input video frames may be computationally prohibitive to yield real time processing results. Therefore, we use an additional preprocessing step of [Background Subtraction](http://docs.opencv.org/3.1.0/db/d5c/tutorial_py_bg_subtraction.html). This removes all the background clutter from the video frame, thereby helping us focus computations on the regions in the image belonging to the foreground. In other words, as we process each of the incoming frames of the video, we only focus on regions where we have motion, thereby, essentially not spending computations on regions that do not have motion. Fruther, in order to improve performance, we can disregard motion regions that are very small e.g., motion of a dog or leave, or motion regions that are extremely large e.g., motion of a large truck or a random illumination change due to lightning etc. This is done by using opencv's mixture of Gaussians based background detector. 

In simple words, this works by maintaining a running model for the background where each pixels is assumed to have a Gaussian mixture distribution. When we encoutner some pixel that cannot be explained by model, we declare that it's a foreground pixel. Following code snippet gives a brief example of how this can be done in opencv:
```
# create background subtraction object
fgbg = cv2.createBackgroundSubtractorMOG2()
fgmask = fgbg.apply(frame)
```
More details about background subtraction can be seen [here](http://docs.opencv.org/3.0-beta/modules/video/doc/motion_analysis_and_object_tracking.html#backgroundsubtractormog2), [here](http://docs.opencv.org/3.1.0/db/d5c/tutorial_py_bg_subtraction.html) and [here](https://pythonprogramming.net/mog-background-reduction-python-opencv-tutorial/). Opencv's background subtractor is very versatile and has a lot of builtin funcationlity that can further be explored to further improve the results and the users are encouraged to explore it.

As shown in the figure below, once the background is subtracted, we can separate out the regions in the foreground and try to search pedestrians in the windows around the foreground region. It's important to keep the window around the foreground object a little bit bigger than the actual foreground object to make sure that we don't accidently miss part of the pedestrian.

![background_subtraction](https://user-images.githubusercontent.com/29146711/29384202-e1282c16-8298-11e7-807e-c6c3116c81c2.png)


## Pedestrian Tracking using Kalman Filter and Kanade Lucas Tomasi (KLT) Tracker
A tracking problem by nature works with video signals. Generally, a basic tracking problem is defined as tracking a fixed object inside a video signal. In practice, however, we may want to track multiple objects that may or may not get occluded due to each other or due to other objects that are part of the scene of the video. There are many different approaches to track objects in videos including Point Tracking e.g., [Kalman Filter](https://en.wikipedia.org/wiki/Kalman_filter), Kernel Tracking e.g., [Kanade Lucas Tomasi (KLT) Tracker](https://en.wikipedia.org/wiki/Kanade%E2%80%93Lucas%E2%80%93Tomasi_feature_tracker), and Silhouette Tracking e.g., shape and contour based models. In this work, we shall be using Kalman Filtering and KLT tracking to track pedestrians. Though these methods are not new, however, the important challenge comes in how we combine these two tracking methods to have a robust tracking mechanism that gives good performance while still being in the realm of real time processing. 

Following figure shows the workflow of pedestrian detection and tracking problem:

![picture2](https://user-images.githubusercontent.com/29146711/29378814-12920fa0-8286-11e7-8d2a-11bde795e58d.png)
We detect pedestrians in the input video frames, and then track the pedestrians by updating their current location. Even if we are not able to detect the pedestrian in the input frame, we can use the current location to perform detection as shown by the feedback loop in the above figure. In order to track pedestrians between frames, we shall use a Kalman Filter and KLT tracker. There are many tutorials/documentation available on the internet on these two, therefore, I shall only give a very brief overview. 

### Kalman Filter
In general, Kalman filter helps us estimate the state of a system from it's uncertain and inaccurate measurements. It helps us make an educated guess in the presence of uncertainty. The Kalman filter assumes that all the states have a Gaussian distribution and the measurements that are made of these states also have gaussian noise in them. Further, it assumes a prior model in the form a linear transition between the states from one time instant to the next. More specifically, it assumes that in an ideal case, the new state could be predicted by performing a linear transformation of the existing state. 

At each time instant, we predict the next state and feed the noisy measurements and get our "optimal" estimate of the current state. In our example, we shall want to estimate the location of the pedestrians in the image, therefore, our state variables shall consist of *x-location*, *y-location*, *x-velocity* and *y-velocity*. We use a constant velocity model and therefore, our measurements only consists of the position of the pedestrian. 

A very nice and easy to understand tutorial on kalman filter can be found [here](http://www.bzarg.com/p/how-a-kalman-filter-works-in-pictures/). Somewhat more formal treatments can be found [here](https://www.cl.cam.ac.uk/~rmf25/papers/Understanding%20the%20Basis%20of%20the%20Kalman%20Filter.pdf) and [here](http://biorobotics.ri.cmu.edu/papers/sbp_papers/integrated3/kleeman_kalman_basics.pdf). The documentation of opencv on Kalman filter can be seen [here](http://docs.opencv.org/ref/2.4/dd/d6a/classcv_1_1KalmanFilter.html) and [here](http://docs.opencv.org/2.4/modules/video/doc/motion_analysis_and_object_tracking.html?highlight=kalman#kalmanfilter). Following code snippet shows how to initialize the most important parameters of a Kalman filter robject in opencv.
```
kalman = cv2.KalmanFilter(4,2)
kalman.measurementMatrix = np.array([[1,0,0,0],[0,1,0,0]],np.float32)
kalman.transitionMatrix = np.array([[1,0,1,0],[0,1,0,1],[0,0,1,0],[0,0,0,1]],np.float32)
kalman.processNoiseCov = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]],np.float32) * 0.03
kalman.measurementNoiseCov = np.array([[1,0],[0,1]],np.float32) * 0.00003
```
This filter object is of size 4x2. This means that length of state vector is 4 and lenght of measurement vector is 2. So the state of this kalman filter object consists of two coordinates for location and two for velocity and the object only obtains the two coordinates of current location as a measurement, hence a size of 4x2.

As mentioned above, at each frame, we require a measurement for the Kalman filter. One possible way is to perform a detection at every step and feed that as a measurement to the Kalman filter. A big issue with performing a detection on every step to feed measurements to Kalman filter is that we can have missed detections because of which the location results from Kalman filter may lose their accuracy gradually. Another problem that we may face is false positive detections, however, the problem of false detections doesn't really appear to affect the accuracy that much as it is unlikely to have a false positive detection in the region where we have a pedestrian. Finally, the biggest hurdle in performing a detection every frame is that of computation. If we are tracking dozens of pedestrians in every frame, then performing a detection for each of the pedestrians would be computationally very expensive. Therefore, we only want to perform a detection step once every few number of frames. We want to use a computationally cheaper method to feed the measurements to the Kalman filter and the KLT tracker explained in the next section helps us do that.
