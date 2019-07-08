import random
import numpy as np
import matplotlib.pyplot as plt
import math
import json
import sys
from collections import Counter
import cv2
from random import randint
import scipy.io

colors = [[255, 0, 0], [255, 85, 0], [255, 170, 0], [255, 255, 0], [170, 255, 0], [85, 255, 0], [0, 255, 0],
          [0, 255, 85], [0, 255, 170], [0, 255, 255], [0, 170, 255], [0, 85, 255], [0, 0, 255], [85, 0, 255],
          [170, 0, 255], [255, 0, 255], [255, 0, 170], [255, 0, 85]]



path=sys.argv[1]
idx=1
cap = cv2.VideoCapture(path+"/video.avi")
capssl = cv2.VideoCapture(path+"/ssl.avi")
numberFrame=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print("number of frames {}".format(numberFrame))
frameShape=(int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))) # removed .cv to fit newer version of opencv

#We create a dictionary for each frame containing the pose and the ssl
framesDic=[{'det':[]} for n in range(numberFrame)]


FBs= open(path+"/detections.txt")
lines =FBs.readlines()
for idx,line in enumerate(lines):
    elements = line.split(' ')
    idxFrame = int(elements[0])-1
    framesDic[idxFrame]['det'].append(map(lambda x: int(float(x)), elements[1:]))

idxFrame=0    
while True:
    ret2, frameSSL = capssl.read()
    if (not ret2):
        end=True
        break
    
    ssl=cv2.resize(frameSSL,(frameShape[1],frameShape[0]), interpolation=cv2.INTER_CUBIC)
    framesDic[idxFrame]['ssl']=ssl
    idxFrame+=1

    
idxFrame=0    
while True:
    ret, frame = cap.read()
    if (not ret) or 'ssl' not in framesDic[idxFrame]:
        end=True
        break

    # we convert the ssl to color heatmap
    sslDisplay=cv2.applyColorMap(framesDic[idxFrame]['ssl'], cv2.COLORMAP_JET)
    matdisp=cv2.addWeighted(frame, 0.7, sslDisplay, 0.3, 0)

    # we display the poses
    for nbDet,det in enumerate(framesDic[idxFrame]['det']):
        for pt in range(0,35,2):
            yi=det[pt]
            xi=det[pt+1]
            if xi>0 and yi>0:
                cv2.circle(matdisp, (yi, xi), 2, colors[pt/2], 2)


    cv2.imshow('Observations',matdisp)
    cv2.waitKey(10)
    idxFrame+=1
