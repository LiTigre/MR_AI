#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 11:34:39 2018

@author: jenisha
"""

import cv2
import numpy as np



def translate_MRI(image_name, shift_coordinates):
    # Load an color image in grayscale
    img = cv2.imread(image_name,0)
    rows,cols = img.shape
    
    x, y = shift_coordinates
    M = np.float32([[1,0,x],[0,1,y]])
    dst = cv2.warpAffine(img,M,(cols,rows))

    cv2.imshow('img',dst)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    
    

    