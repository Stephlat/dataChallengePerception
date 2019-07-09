#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 09:43:55 2017

@author: durand

Random assignation of labels to sequences
"""

import os
import numpy as np

# home_dir = os.environ['HOME']
challenge_path = "C:/Users/sebbe/OneDrive/Dokument/GitHub/dataChallengePerception/randomGuess"
# challenge_path = home_dir + os.sep + "tmp" +os.sep + "Msiam" + os.sep
# challenge_path += "DataChallenge" + os.sep + "2017-2018" + os.sep + "ScriptsJB"

# challenge_path = home_dir + os.sep + "Davfs2" + os.sep + "Cloud-ljk" + os.sep + "Tmp" + os.sep
# challenge_path += "DataChallenge" + os.sep + "2017-2018" + os.sep + "ScriptsJB"

os.chdir(challenge_path)

scenario = "Scenario03-05"

input_dir = "C:\\Users\\sebbe\\OneDrive\\Dokument\\GitHub\\dataChallenge\\" + scenario

def parse_detections(input_dir, read_nb_speakers=True, detections=True):
    """
    :param 
        - input_dir: input directory name
        - read_nb_speakers: True iff number of speakers is guessed 
            from directory name (from file contents otherwise)
        - detections: True iff detections.txt is used (groundTruth.txt otherwise)

    :return 
        - nb_speakers: number of detected persons
	- nb_persons_frame: number of persons (for each line of input, indexed from 1)
	- contents: line contents (for each line of input, indexed from 1)
	- frame_id: frame of each line
	- nb_persons_changes: lines with changes in number of detectespeakers
    """
    if detections:
        input_file = input_dir + os.sep + "detections.txt"
    else:
        input_file = input_dir + os.sep + "groundTruth.txt"
    
    # Read input file
    
    # Read directory name (number of speakers)
    
    dir_name = os.path.basename(input_dir)
    
    nb_speakers_from_dir = int(dir_name.split("-")[1])
    
    # number of speakers guessed from contents
    nb_speakers_from_file = 0
    
    f = open(input_file, "r")
    
    contents = {}
    nblines = 0
    nb_persons_frame = ["Nan"] # number of detected persons per frame
    # (indexed from 0)
    frame_id = ["Nan"] # Frame of line
    for line in f:
        nblines += 1
        contents[nblines] = line
        frame = line.split(" ")[0] # frame id
        line_search = nblines-1 # line where to search same frame id
        persons_frame = 1 # number of persons detected in frame
        while line_search > 0:
            past_frame = contents[line_search].split(" ")[0]
            if past_frame == frame:
                persons_frame = nb_persons_frame[line_search] + 1
                nb_speakers_from_file = max(nb_speakers_from_file, persons_frame)
                nb_persons_frame[line_search] = persons_frame
                line_search -= 1
            else:
                line_search = 0
        frame_id += [frame]
        nb_persons_frame += [persons_frame]   
    
    f.close()
    
    nb_persons_changes = [] # frames where nb persons changes
    for i in range(1, len(contents)+1):
        if nb_persons_frame[i] != nb_persons_frame[i-1]:
            nb_persons_changes += [i]
    
    if read_nb_speakers:
        nb_speakers_from_file = nb_speakers_from_dir
            
    return(nb_speakers_from_file, nb_persons_frame, contents, frame_id, 
           nb_persons_changes)

def independent_simulation(input_dir, nb_persons_frame, contents, frame_id, 
                           speech_prob=0.5):
    """
    Independent random simulation of labels: 
        independance of labels and speach utterance wrt frames
        
    :param 
        - input_dir: input directory name
    """
    # Write output file
    output_file = input_dir + os.sep + "independent_random_predictions.txt"
    f = open(output_file, "w")
    for line in range(1, len(nb_persons_frame)):
        strcont = contents[line].split(" ")
        frame = strcont[0] # frame id
        f.write(str(frame) + " ")
        # Random permutation of labels
        # Identify whether a new frame begins
        if frame_id[line] != frame_id[line-1]:
            line_in_frame = 0 # Id of line within frame
            rperm_frame = np.random.permutation(nb_persons_frame[line])+1
        else:
            line_in_frame += 1
        # Write label of current person
        f.write(str(rperm_frame[line_in_frame]) + " ")
        # Write uterrance of speach
        f.write(str(np.random.binomial(1, speech_prob, 1)[0]) + " ")
        # Write end of line
        f.write(" ".join(strcont[1:]))
    
    f.close()

def dependent_simulation(input_dir, nb_persons_frame, contents, frame_id, 
                         nb_persons_changes, speech_change_prob=0.5):
    """
    Piecewise deterministic random simulation of labels: 
        Persistence of labels and Markovian speach utterance wrt frames
        
    :param 
        - input_dir: input directory name
        - read_nb_speakers: True iff number of speakers is guessed 
            from directory name (from file contents otherwise)
    """
    # Write output file
    output_file = input_dir + os.sep + "dependent_random_predictions.txt"
    f = open(output_file, "w")
    nb_changes = 0
    for line in range(1, len(nb_persons_frame)):
        strcont = contents[line].split(" ")
        frame = strcont[0] # frame id
        f.write(str(frame) + " ")
        # Detect change in the number of persons
        if (nb_changes < len(nb_persons_changes)) and \
            (nb_persons_changes[nb_changes] == line):
            # Random permutation of labels
            rperm_frame = np.random.permutation(nb_persons_frame[line])+1
            # Determines speaker
            # 0: nobody
            speaking = np.random.permutation(nb_persons_frame[line]+1)
            speaking = speaking[0]
            nb_changes += 1
        # Identify whether a new frame begins
        if frame_id[line] != frame_id[line-1]:
            line_in_frame = 0 # Id of line within frame 
        else:
            line_in_frame += 1
        # Write label of current person
        f.write(str(rperm_frame[line_in_frame]) + " ")
        # Determines whether speaker changes
        if (np.random.binomial(1, speech_change_prob, 1)[0] == 0):
            speaking = np.random.permutation(nb_persons_frame[line]+1)
            speaking = speaking[0]
        if (line_in_frame + 1 == speaking):
            f.write("1" + " ")
        else:
            f.write("0" + " ")
        # Write end of line
        f.write(" ".join(strcont[1:]))
    
    f.close()

def permute_ground_truth(input_dir, contents):
    """
    Permutation of labels in ground truth
    """
    # Determines number of persons
    nb_pers = max([int(v.split(" ")[1]) for v in contents.values()])
    rperm = np.random.permutation(nb_pers)+1
    while (str(rperm) == str(np.arange(nb_pers)+1)):
        rperm = np.random.permutation(nb_pers)+1
    # Write output file    
    output_file = input_dir + os.sep + "permuted_groundTruth.txt"
    f = open(output_file, "w")
    for line in range(1, max(contents.keys())+1):
        strcont = contents[line].split(" ")
        frame = strcont[0] # frame id
        f.write(str(frame) + " ")
        f.write(str(rperm[int(strcont[1])-1]) + " ")
        # Write end of line
        f.write(" ".join(strcont[2:]))
    
    f.close()
