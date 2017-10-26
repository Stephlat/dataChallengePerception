# Data Challenge organized by Inria-Perception

This repository contains the basic scripts that are provided for the challenge.The goal is to develop an audio-visual diarization model. 
We provide the following observations that must be used as input for your model:
* RGB videos
* Sound Source Localisation (SSL) as heatmaps.
* full body pose estimation

The goal is twofold:
* Perform visual tracking to associate the provided detections through time
* Predict the speaking activity of each tracked person.

We provide the some basic visualization and evaluation scripts.
The data are based on the [AVDIAR dataset](https://team.inria.fr/perception/avdiar/).The data can be downloaded [here](http://perception.inrialpes.fr/Free_Access_Data/dataChallenge/dataChallenge.tar.gz).

## Dependencies
You need to install opencv-python and  numpy. Some other recommended librairies are listed on the. The scripts have been tested with opencv cv2 version 2.4.13 and python 2.7.12.

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

## List of recommended papers or websites
 * Audio-Visual Speaker Diarization Based on Spatiotemporal Bayesian Fusion: https://hal.inria.fr/hal-01413403
 * Tracking a Varying Number of People with a Visually-Controlled Robotic Head: https://hal.inria.fr/hal-01542987v2
 * Mot challenge: https://motchallenge.net/
 * opencv : https://docs.opencv.org/2.4.13.2/index.html
 * scikit-learn: http://scikit-learn.org/stable/
</ul>
<strong>The data:</strong>