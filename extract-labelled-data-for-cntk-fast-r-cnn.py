# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 13:45:34 2017

@author: cyyam
purpose: extract data for CNTK Fast-R-CNN
"""

### -i ./data/val_annotations.pkl -o ./output_for_cntk/

import pickle
import argparse

def main():
    
    ### User input
    argparser = argparse.ArgumentParser(description="This script will take a Caltech pedestrain annotation file in \
                                        pkl format, and extract images containing at least a person in a frame, and \
                                        return a folder called 'positives', with files contatining the location of \
                                        the bounding box, labels, and copy over corresponding image files.")
    
    argparser.add_argument('-i', '--pklIn', help='filename.pkl', required=True)
    argparser.add_argument('-o', '--dirOut', help='directory for output files', required=True)
    args = argparser.parse_args()
    pklIn = args.pklIn
    dirOut = args.dirOut
    
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
            
            # counter
            count = 0
            
            for frame, frame_list in frames.items(): 
                #print(frame) # frame number?
                
                # for every frame
                for fr in frame_list:
                    # a list to hold multiple 'posv_rounded'
                    list_posv_rounded = []
                
                    # if 'lbl' contain object of interest, i.e. fr['lbl']=='people' or fr['lbl']=='person'
                    if fr['lbl'] in lbl_wanted:
                        # if type is list
                        if type(fr['posv']) is list:
                            # if obj is visible, i.e. is 'posv' is non zeros
                            if fr['posv'] != [0,0,0,0]:
                                # if obj size satisfied a threshold, i.e. w > 20 and h > 40
                                if fr['posv'][2]>=20 and fr['posv'][3]>=40: 
                                    # a list to hold rounded 'posv'
                                    posv_rounded = []
                            
                                    #print(v['lbl']) # not needed
                                    #print(v['posv']) # YES, NEEDED
                                    # round up decimal
                                    posv_rounded = [round(p) for p in fr['posv']]; #print(posv_rounded)
                                    # convert from [x, y, w, h] to [x_topleft, y_topleft, x_bottomright, y_bottomright]
                                    posv_rounded[2] = posv_rounded[0] + posv_rounded[2]
                                    posv_rounded[3] = posv_rounded[1] + posv_rounded[3]; #print(posv_rounded)
                                    # put posv_rounded into the list list_posv_rounded, required when more than one obj present in a single frame
                                    list_posv_rounded.append(posv_rounded); #print(list_posv_rounded)
                                
                                    #print(v['id']) # not needed
                                    #print(v['str']) # not needed
                                    #print(v['end']) # not needed
                                    count = count + 1
                                    #print(frame) 
                                    #print('..........count............' + str(count))
                    
                                    # write out list_posv_rounded
                                    import csv
                                    filename_bboxes = 'img{}{}{:04}.jpg'.format(imageset, seq, frame); #print('filename_bboxes: ' + filename_bboxes)
                                    with open('./output_for_cntk/positives/' + filename_bboxes + '.bboxes.tsv', 'w', newline='') as f:
                                        writer = csv.writer(f, delimiter='\t')
                                        writer.writerows(list_posv_rounded)
                                        
                                    # write out labels
                                    with open('./output_for_cntk/positives/' + filename_bboxes + '.bboxes.labels.tsv', 'w', newline='') as f:
                                        writer = csv.writer(f)
                                        for l in range(len(list_posv_rounded)):
                                            writer.writerow(['person'])
                                        if len(list_posv_rounded) > 1:
                                            print('> 1 object : filename_bboxes: ' + filename_bboxes)
                
                                    # copy the frame from one folder to another folder
                                    import shutil
                                    srcfile = './data/val_images/' + filename_bboxes
                                    dstdir = './output_for_cntk/positives/'
                                    shutil.copy(srcfile, dstdir)


if __name__ == '__main__':
    main()

