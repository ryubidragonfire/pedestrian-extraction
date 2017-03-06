# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 15:27:22 2017

@author: cyyam
purpose: check for labels used
"""

### -i ./data/val_annotations.pkl
### set 00 to set 05:
### set 06 to set 07: {'people', 'person', 'person?', 'person-fa'}
### set 08 to set 10:

import pickle
import argparse

def main():
    
    ### User input
    argparser = argparse.ArgumentParser(description="This script will take a Caltech pedestrain annotation file in \
                                        pkl format, return a list of unique labels used to label images in the dataset.")
    
    argparser.add_argument('-i', '--pklIn', help='filename.pkl', required=True)
    args = argparser.parse_args()
    pklIn = args.pklIn
    
    annotations = pickle.load(open(pklIn, "rb" ))
    
    # a list to store labels, i.e. 'lbl'
    lbl_list = []
    
        # for each image set, e.g. set00, set01, ...set10
    for imageset, imageset_dict in sorted(annotations.items()):
        print('image set:' + imageset) # image set: '00', '01', ....'10'
        
        #for each sequence in a set, e.g. '00', '01', ...
        for seq, seq_dict in sorted(imageset_dict.items()):
            print('   sequence: ' + seq) # sequence in each image set: '00', '01', '02', ... '18'
            #print(seq_dict.keys()) # 'frames', 'logLen', 'log', 'altered', 'nFrame', 'maxObj'
            
            # get frames of type dict from a sequence, e.g. 
            frames = seq_dict.get('frames'); #print(len(frames))
            
            # counter
            count = 0
            
            for frame, frame_list in frames.items(): 
                #print(frame) # frame number?
                for fr in frame_list:
                    # put all 'lbl' in a list
                    lbl_list.append(fr['lbl'])
    
    lbl_unique = set(lbl_list) # unique element in a list
    print(lbl_unique)
    
if __name__ == '__main__':
    main()