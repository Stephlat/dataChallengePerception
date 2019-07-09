#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 09:43:55 2017

@author: durand

Replicate random assignations of labels to sequences and 
plot metrics distribution
"""
import os
import numpy as np

home_dir = os.environ['HOME']
challenge_path = home_dir + os.sep + "tmp" +os.sep + "Msiam" + os.sep
challenge_path += "DataChallenge" + os.sep + "2017-2018" + os.sep + "ScriptsJB"

os.chdir(challenge_path)

from random_assignation import *

import sys
sys.path += [challenge_path + os.sep + "metric_final"]

from compute_metric import *

input_dir = os.pardir+os.sep+"dataChallenge"+os.sep+"Scenario03-05"

read_nb_speakers=True

# Parse detections.txt

nb_speakers_from_file, nb_persons_frame, contents, frame_id, \
           nb_persons_changes = parse_detections(input_dir, read_nb_speakers)

# Generate random labels and speech utterance
independent_simulation(input_dir, nb_persons_frame, contents, frame_id, 
                       speech_prob=0.5)

dependent_simulation(input_dir, nb_persons_frame, contents, frame_id, 
                     nb_persons_changes, speech_change_prob=0.5)


# Parse GroundTruth.txt
nb_speakers_from_file, nb_persons_frame, contents, frame_id, \
           nb_persons_changes = parse_detections(input_dir, True, False)

permute_ground_truth(input_dir, contents)

