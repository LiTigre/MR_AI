#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 14:20:40 2018

@author: jenisha
"""

import numpy as np
import matplotlib.pyplot as plt
import cv2



def sampling_radially(image_path,n_sampling_points,n_sample_spacing, sampling_radius, sampling_angle = 2*np.pi ):
    #Read the image
    img = cv2.imread(image_path, 0)
    
    #perform the fft
    image_fft = np.fft.fft2(img)
    

    # Determine center of figure from which sampling will tsart
    width, height = image_fft.shape
    center_x = width //2
    center_y = height //2
    
    
    #Ranndom circular coordinate generation for sampling 
    r_ran = np.random.uniform(low=0, high=sampling_radius, size=n_sampling_points)  # radius
    theta_ran = np.random.uniform(low=0, high=sampling_angle, size=n_sampling_points)  # angle
    x_random = np.sqrt(r_ran) * np.cos(theta_ran)
    y_random = np.sqrt(r_ran) * np.sin(theta_ran)
    
    x_random = x_random + sampling_radius
    y_random  =y_random + sampling_radius
    
    plt.plot(x_random , y_random , '.')
    plt.show()
    
    #Uniform circular coordinate generation for sampling 
    #r_uniform = np.linspace(0, sampling_radius, num=n_sampling_points, retstep=n_sample_spacing)
    #theta_uniform = np.linspace(0, sampling_angle, num=n_sampling_points, retstep=n_sample_spacing)
    #x_uniform = np.sqrt(r_uniform) * np.cos(theta_uniform)
    #y_uniform = np.sqrt(r_uniform ) * np.sin(theta_uniform)
    
    #x_uniform = x_uniform + width
    #y_uniform  =y_uniform+ height
    
    return (x_random,y_random )

def sampling_image(image_path, image_transformed_path, x_random, y_random):
    
    #Read the images
    img = cv2.imread(image_path, 0)
    img_trans = cv2.imread(image_transformed_path, 0)
    
    #perform the fft
    image_fft = np.fft.fft2(img)
    width, height = image_fft.shape
    image_trans_fft = np.fft.fft2(img_trans)
    width2, height2 = image_trans_fft.shape
    
    #Determine sampling arrays
    sampling_array = np.ones((width, height))
    sampling_array2 = np.zeros((width2, height2))
    list_coordinates = list(zip( np.rint(x_random),  np.rint(y_random)))
    
    for x,y in list_coordinates:
        sampling_array[x,y] = 0
        sampling_array2[x,y] = 1 #could we just invert?
    
    return np.multiply(image_fft,sampling_array) + np.multiply(image_trans_fft,sampling_array2)
    
