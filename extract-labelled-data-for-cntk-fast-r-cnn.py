# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 13:45:34 2017

@author: cyyam
purpose: extract data for CNTK Fast-R-CNN
"""

### -i ./data/val_annotations.pkl -o ./output_for_cntk/val/positives/ -im ./data/val_images/
### -i ./data/train_annotations.pkl -o ./for_cntk/train/positives/ -im ./data/train_images/

import pickle
import argparse
import shutil
import csv
import sys

# write out bounding boxes
def writebboxes(dirOut, filename_bboxes, list_posv_rounded):
    with open(dirOut + filename_bboxes + '.bboxes.tsv', 'w', newline='') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerows(list_posv_rounded)
    return
 
# write out labels
def writelabels(dirOut, filename_bboxes, list_posv_rounded):
    with open(dirOut + filename_bboxes + '.bboxes.labels.tsv', 'w', newline='') as f:
        writer = csv.writer(f)
        for l in range(len(list_posv_rounded)):
            writer.writerow(['person'])
        #if len(list_posv_rounded) > 1:
        #    print('> 1 object : filename_bboxes: ' + filename_bboxes)
    return

# copy the frame from one folder to another folder
def copypositiveimages(dirIm, filename_bboxes, dirOut):
    srcfile = dirIm + filename_bboxes
    dstdir = dirOut
    shutil.copy(srcfile, dstdir)
    return

def main():
    
    ### User input
    argparser = argparse.ArgumentParser(description="This script will take a Caltech pedestrain annotation file in \
                                        pkl format, and extract images containing at least a person in a frame, and \
                                        return a folder called 'positives', with files contatining the location of \
                                        the bounding box, labels, and copy over corresponding image files.")
    
    argparser.add_argument('-i', '--pklIn', help='filename.pkl', required=True)
    argparser.add_argument('-o', '--dirOut', help='directory for output files', required=True)
    argparser.add_argument('-im', '--dirIm', help='directory for images files to copy from', required=True)
    args = argparser.parse_args()
    pklIn = args.pklIn
    dirOut = args.dirOut
    dirIm = args.dirIm
    
    annotations = pickle.load(open(pklIn, "rb" ))
    
    # wanted labels
    lbl_wanted = ['people', 'person']
    
    # for each image set, e.g. set00, set01, ...set10
    for imageset, imageset_dict in sorted(annotations.items()):
        print('image set:' + imageset) # image set: '00', '01', ....'10'
        #for each sequence in a set, e.g. '00', '01', ...
        for seq, seq_dict in sorted(imageset_dict.items()):
            print('   sequence: ' + seq) # sequence in each image set: '00', '01', '02', ... '18'
            #print(seq_dict.keys()) # 'frames', 'logLen', 'log', 'altered', 'nFrame', 'maxObj'
            # get frames of type dict from a sequence, e.g. 
            frames = seq_dict.get('frames'); #print(len(frames))
            #print(seq_dict.keys())
            # counter
            count = 0
            
            for frame, frame_list in frames.items(): 
                #print(frame) # frame number?
                # a list to hold multiple 'posv_rounded'
                list_posv_rounded = []
                # for every frame
                for fr in frame_list:
                    # if 'lbl' contain object of interest, i.e. fr['lbl']=='people' or fr['lbl']=='person'
                    if fr['lbl'] in lbl_wanted:
                        # if type is list
                        if type(fr['pos']) is list:
                            # if obj is visible, i.e. is 'posv' is non zeros
                            if fr['pos'] != [0,0,0,0]:
                                # if obj size satisfied a threshold, i.e. w > 30 and h > 60
                                if fr['pos'][2]>=40 and fr['pos'][3]>=70: 
                                    # a list to hold rounded 'posv'
                                    posv_rounded = []
                            
                                    #print(v['lbl']) # not needed
                                    #print(v['posv']) # YES, NEEDED
                                    # round up decimal
                                    posv_rounded = [round(p) for p in fr['pos']]; #print(posv_rounded)
                                    # convert from [x, y, w, h] to [x_topleft, y_topleft, x_bottomright, y_bottomright]
                                    posv_rounded[2] = posv_rounded[0] + posv_rounded[2]
                                    posv_rounded[3] = posv_rounded[1] + posv_rounded[3]; #print(posv_rounded)
                                    # put posv_rounded into the list list_posv_rounded, required when more than one obj present in a single frame
                                    list_posv_rounded.append(posv_rounded); #print('\n'+'list_posv_rounded' + str(list_posv_rounded))
                                    
                                    #print(v['id']) # not needed
                                    #print(v['str']) # not needed
                                    #print(v['end']) # not needed
                                    count = count + 1
                                    #print(frame) 
                                    #print('..........count............' + str(count))
                    
                                    # generate filename
                                    filename_bboxes = 'img{}{}{:04}.jpg'.format(imageset, seq, frame); #print('filename_bboxes: ' + filename_bboxes)
                    
                                    # write out list_posv_rounded
                                    writebboxes(dirOut, filename_bboxes, list_posv_rounded)    
                                    
                                    # write out labels
                                    writelabels(dirOut, filename_bboxes, list_posv_rounded)
            
                                    # copy the frame from one folder to another folder
                                    copypositiveimages(dirIm, filename_bboxes, dirOut)
                                    
                #sys.exit()


if __name__ == '__main__':
    main()


########################################################################################################
#{'end': 924,                   #the last frame in which object appears (1 indexed)
# 'hide': 0,                    #0/1 value indicating object is 'hidden' (used during labeling)
# 'id': 3,
# 'init': 1,                    #0/1 value indicating whether object w given id exists
# 'lbl': 'person',              #a string label describing object type (eg: 'pedestrian')
# 'lock': 1,                    #0/1 value indicating bb is 'locked' (used during labeling)
# 'occl': 1,                    #0/1 value indicating if bb is occluded
# 'pos': [586.9452554744529,    #[l t w h]: bb indicating predicted object extent
#         154.16479147988605,
#         25.5445751443807,
#         75.21355401889747],
# 'posv': [588.3018808211706,   #[l t w h]: bb indicating visible region (may be [0 0 0 0])
#          159.0577355188155,
#          24.4093609898772,
#          25.750538092197132],
# 'str': 885}                   #the first frame in which object appears (1 indexed)
########################################################################################################
