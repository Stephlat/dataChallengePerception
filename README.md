# Data Challenge organized by Inria-Perception

This repository contains the basic scripts that are provided for the challenge:

## Dependencies
You need to install opencv-python and  numpy. Some other recommended librairies are listed on the [data challange page](https://team.inria.fr/perception/research/data-challenge/). The scripts have been tested with opencv cv2 version 2.4.13 and python 2.7.12.

## Scripts
We provide the following scripts:
* visualizeObs.py: visualize the observations (visual and audio) we provide for one given video
```
python visualizeObs.py ..data/videoDirectory/
```
* visualizePred.py: visualize the prediction for one given video. It can be also used to visualize the groundTruth of a video.
```
python visualizePred.py ..data/videoDirectory/prediction.txt
```
* evaluatePred.py: evaluate the prediction for one given video (NOT AVAILABLE)
```
python evaluatePred.py ..data/videoDirectory/prediction.txt
```

We strongly recommend to use these scipts to code the loading function of your own programm.


## Format of the data
./data contains one folder per video sequence. Each folder contains:

* video.avi: the video it-self.
* ssl.avi: the video of the Sound Source Localization (SSL) heat map (downsample by a factor 2). It gives the probability according to our SSL that their is a sound source at each pixel.
* detections.txt: full body detections of the video. We ran a [multiple person detector](https://github.com/ZheC/Realtime_Multi-Person_Pose_Estimation) in order to obtained the coordinates (x, y) of 18 joints (nose, shoulders, elbows...) of the persons of each frame. The file contains one detection per line. The format of each line is the following:
```
frameNumber x0 y0 x1 y1....x17 y17 
```
When a joint is not detected, the corresponding  xi and yi are set to -1

* groundTruth.txt: full body detections with and with an index to indentify them across time and a seapking label. It contains one person per line. The format of each line is the following:
```
frameNumber personIndex speakingLabel x0 y0 x1 y1....x35 y35 
```
speakingLabel=1 if the person is speaking, 0 otherwise. 

* prediction.txt: this is what you have to generate. We give an example of this file in data/video1/. It has to respect the same format than groundTruth.txt to be used by visualizePred.py and evaluatePred.py 

## Data
The link to the data can be found on the [data challange page](https://team.inria.fr/perception/research/data-challenge/).