import os
import numpy as np
import nibabel as nib
from nibabel.testing import data_path
from PIL import Image
import SimpleITK as sitk
import random
import math
import sys
import cv2
from numpy.fft import fftshift, ifftshift, fftn, ifftn
from scipy.ndimage import gaussian_filter


# Normalize the image to (0, 255)
def normalization(my_slice):
    my_mean = np.mean(my_slice)
    my_std = np.std(my_slice)
    my_adjusted_0 = np.true_divide(my_slice - my_mean, my_std)
    my_max = np.nanmax(my_adjusted_0)
    my_min = np.nanmin(my_adjusted_0)
    my_difference = my_max - my_min
    my_adjusted = np.true_divide(my_adjusted_0 - my_min, my_difference) * 255
    return my_adjusted


def normalization_slice(my_volume):
    my_mean = np.mean(my_volume)
    print(type(my_mean))
    print(my_mean)
    my_std = np.std(my_volume)
    normalized_volume = np.true_divide(my_volume - my_mean, my_std)
    return normalized_volume


# Store all the coordinates on that slice to a list
def to_coordinates(my_slice):
    it = np.nditer(my_slice, flags=['multi_index'])
    list_of_coordinates = []
    while not it.finished:
        list_of_coordinates.append(it.multi_index)
        it.iternext()
    return list_of_coordinates


# Perform translation to the coordinates
def coordinates_translation(coordinates, t):
    dimension = 3
    translation = sitk.TranslationTransform(dimension, t)
    rigid_euler = sitk.Euler3DTransform()
    rigid_euler.SetTranslation(translation.GetOffset())
    translated = [translation.TransformPoint(p) for p in coordinates]
    return translated


def coordinates_rotation(coordinates, axis, angle, rotationCenter):
    rotation = sitk.VersorTransform(axis, angle, rotationCenter)
    rigid_euler = sitk.Euler3DTransform()
    rigid_euler.SetMatrix(rotation.GetMatrix())
    rigid_euler.SetCenter(rotation.GetCenter())
    rotated_coordinates = [rigid_euler.TransformPoint(p) for p in coordinates]
    return rotated_coordinates


def fetch_points(transformed_coordinates, volume_data, slice_index):
    new_slice = np.zeros((256, 256))
    counter = 0
    for j in range(256):
        for i in range(256):
            coordinate_tuple = transformed_coordinates[counter]
            x = int(coordinate_tuple[0])
            y = int(coordinate_tuple[1])
            z = int(coordinate_tuple[2] + slice_index)
            if 0 <= x < 256 and 0 <= y < 256 and 0 <= z < 130:
                new_slice[i, j] = volume_data[x, y, z]
            else:
                new_slice[i, j] = 0
            counter += 1
    return new_slice


def rigid_transform(image, volume, x, y, z, theta, phi, r, slice_index):
    # image: input slice, 2d array
    # volume: original volume, 3d array
    # x, y, z: amount of translation along x, y and z axes
    # theta: rotation angle along x axis, up and down
    # phi: rotation angle along y axis, left and right
    # r: rotation angle along z axis, turn within the same plane
    coordinates = to_coordinates(np.expand_dims(np.copy(image), axis=2))
    if x != 0 or y != 0 or z != 0:
        t = [x, y, z]
        coordinates = coordinates_translation(coordinates, t)
    rotationCenter = (128, 128, 0)
    if theta != 0:
        coordinates = coordinates_rotation(coordinates, [1,0,0], theta, rotationCenter)
    if phi != 0:
        coordinates = coordinates_rotation(coordinates, [0,1,0], phi, rotationCenter)
    if r != 0:
        coordinates = coordinates_rotation(coordinates, [0,0,1], r, rotationCenter)
    slice_1 = fetch_points(coordinates, volume, slice_index)
    adjusted_1 = normalization(slice_1)
    return adjusted_1


def random_movement_translation():
    x = math.floor(random.uniform(-4.999, 5.999))
    y = math.floor(random.uniform(-4.999, 5.999))
    z = math.floor(random.uniform(-4.999, 5.999))
    return x, y, z


def random_movement_rotation():
    theta = random.uniform(-5, 5)*np.pi/180
    phi = random.uniform(-5, 5) * np.pi/180
    r = random.uniform(-5, 5)*np.pi/180
    return theta, phi, r


def merge_k_spaces(og_image, tilted_image, percentage):
    #perform the fft
    f_1 = np.fft.fft2(og_image)
    f_2 = np.fft.fft2(tilted_image)
    #add the two images together with the percentage
    f_out = f_1*(1-percentage) + f_2*percentage
    #reverse the fft
    arr_out = np.fft.ifft2(f_out)
    img_out = Image.fromarray(np.abs(arr_out))
    img_blur = gaussian_filter(img_out, sigma=0.1)
    img_show = Image.fromarray(np.abs(img_blur))
    return img_show


# load file
example_filename = os.path.join(data_path, sys.argv[1])
# example_filename = os.path.join(data_path, '/Users/chloewang/Downloads/MRI_1000_T2/127731_3T_T2w_SPC1.nii.gz')
volume = nib.load(example_filename)
volume_data = volume.get_data()
print(volume_data.shape)
for i in range(40, 90, 1):
    slice_index = i
    # select original slice
    slice_0 = volume_data[:,:,slice_index]
    adjusted_0 = normalization(slice_0)
    slice_0_img = Image.fromarray(adjusted_0)
    slice_0_img.convert('RGB').save('/Users/chloewang/Downloads/Train/' + 'S_' + sys.argv[2] + '_' + str(slice_index) +'.jpg', 'JPEG')
    print('/Users/chloewang/Downloads/Test/' + 'S_' + sys.argv[2] + '_' + str(slice_index) +'.jpg')
    # get transformed slice
    x, y, z = random_movement_translation()
    theta, phi, r = random_movement_rotation()
    slice_1 = rigid_transform(slice_0, volume_data, x, y, z, theta, phi, r, slice_index)
    # merge two slices
    percentage = random.uniform(0.2, 0.5)
    new_slice_img = merge_k_spaces(adjusted_0, slice_1, percentage)
    new_slice_img.convert('RGB').save('/Users/chloewang/Downloads/Train/' + 'T_' + sys.argv[2] + '_' + str(slice_index) + '.jpg', 'JPEG')
    print('/Users/chloewang/Downloads/Test/' + 'T_' + sys.argv[2] + '_' + str(slice_index) + '.jpg')