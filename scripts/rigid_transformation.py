#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 13:57:37 2018

@author: jenisha
"""

import nibabel as nib
import numpy as np
from nibabel.affines import apply_affine

def rigid_transformation(filename, scaling, rotation, translation):
    """
    Parameters: 
        
        
        
        
        
    Returns 

    
    """

    img = nib.load(filename)
    img_data = img.fget_data()
    image_width, image_height, image_depth =  img_data.shape
    
    center_i = (image_width - 1) // 2  # // for integer division
    center_j = (image_height - 1) // 2
    center_k = (image_depth - 1) // 2
    
    # Scaling
    s_x, s_y, s_z = scaling
    scaling_affine = np.array([[s_x, 0, 0, 0],
                              [0, s_y, 0, 0],
                              [0, 0, s_z, 0],
                              [0, 0, 0, 1]])
    # Rotation
    r_cos, r_sin = rotation
    cos_gamma = np.cos(r_cos)
    sin_gamma = np.sin(r_sin)
    
    rotation_affine = np.array([[1, 0, 0, 0],
                              [0, cos_gamma, -sin_gamma, 0],
                              [0, sin_gamma, cos_gamma, 0],
                              [0, 0, 0, 1]])
    
    t_x, t_y, t_z = translation
    translation_affine = np.array([[1, 0, 0, t_x],
                                   [0, 1, 0, t_y],
                                   [0, 0, 1, t_z],
                                   [0, 0, 0, 1]])
    
    aff = (rotation_affine.dot(scaling_affine)).dot(translation_affine)
    # Apply transformation
    tranformed = apply_affine(aff, img_data)
