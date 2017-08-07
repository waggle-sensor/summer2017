# Pedestrian detection using HOG Descriptor and Support Vector Machine from OpenCV

* The detection uses HOG descriptor provided by OpenCV. Also, linear SVM is used to classify input images. Detection size (window size) is (64, 128). The detector is written in Python and performs about 3 frames per second when the image is 640x480 (0.3 Mpixel) on Edge processor.

* Instructions to perform training, detection are described [here](https://github.com/waggle-sensor/edge_processor/tree/image-pipeline/image/pipeline/pedestrian_detector/training)

* crop_images files are the screenshots of the GUI that a person annotates people in the image to extract positive images for training.

* Detections files are results of the detection by the classifier.

* Detections_raw.jpg is the raw file that you can open and see the results in its exif (Exchangable image file format).

* property_detail.jpg is a screenshot of property window showing results that are encoded by exif.
