# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 15:27:22 2017

@author: cyyam
purpose: extract negative samples
"""

### -i ./data/train_annotations.pkl -o ./for_cntk/small/train/negatives/ -im ./data/train_images/ -n 30
### -i ./data/test_annotations.pkl -o ./for_cntk/small/test/negatives/ -im ./data/test_images/ -n 30
### -i ./data/val_annotations.pkl -o ./for_cntk/small/val/negatives/ -im ./data/val_images/ -n 30

import pickle
import argparse
import shutil
import os
import random

# copy the frame from one folder to another folder
def copynegativeimages(dirIm, filename_bboxes, dirOut):
    srcfile = dirIm + filename_bboxes
    dstdir = dirOut
    shutil.copy(srcfile, dstdir)
    return

def main():
    
    ### User input
    argparser = argparse.ArgumentParser(description="This script will take a Caltech pedestrain annotation file in \
                                        pkl format, filter out images that does not contain a person, copy those\
                                        into a folder as negative samples.")
    
    argparser.add_argument('-i', '--pklIn', help='filename.pkl', required=True)
    argparser.add_argument('-o', '--dirOut', help='directory for output files', required=True)
    argparser.add_argument('-im', '--dirIm', help='directory for images files to copy from', required=True)
    argparser.add_argument('-n', '--n', help='number of samples required, e.g. 20', required=True)
    args = argparser.parse_args()
    pklIn = args.pklIn
    dirOut = args.dirOut
    dirIm = args.dirIm
    n = int(args.n)
    
    annotations = pickle.load(open(pklIn, "rb" ))
    
    # a list to store names of positive images 
    positive_image_list = []
    
   
    all_image_list = os.listdir(dirIm)
    
    # for each image set, e.g. set00, set01, ...set10
    for imageset, imageset_dict in sorted(annotations.items()):
        print('image set:' + imageset) # image set: '00', '01', ....'10'
        
        #for each sequence in a set, e.g. '00', '01', ...
        for seq, seq_dict in sorted(imageset_dict.items()):
            print('   sequence: ' + seq) # sequence in each image set: '00', '01', '02', ... '18'
            #print(seq_dict.keys()) # 'frames', 'logLen', 'log', 'altered', 'nFrame', 'maxObj'
            
            # get frames of type dict from a sequence, e.g. 
            frames = seq_dict.get('frames'); #print(len(frames))
            #positive_image_list.append(list(sorted(frames.keys()))); print('lenght of positive_image_list: ' + str(len(positive_image_list)))
            
            for frame, frame_list in frames.items(): 
                filename_bboxes = 'img{}{}{:04}.jpg'.format(imageset, seq, frame); #print('filename_bboxes: ' + filename_bboxes)
                positive_image_list.append(filename_bboxes)
            
    # a list containing negative samples
    negative_image_list = list(set(all_image_list) - set(positive_image_list))
    
    # randomly select n number of images
    negative_image_list_small = random.sample(negative_image_list, n)
    
    for img in negative_image_list_small:
        # copy negative samples into a folder
        copynegativeimages(dirIm, img, dirOut)
    
            
if __name__ == '__main__':
    main()