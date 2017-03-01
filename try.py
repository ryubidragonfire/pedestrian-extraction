# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pickle

filename = './data/val_annotations.pkl'

anno = pickle.load(open(filename, "rb" ))

# https://www.haykranen.nl/2016/02/13/handling-complex-nested-dicts-in-python/