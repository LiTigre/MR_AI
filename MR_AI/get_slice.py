import os
import nibabel as nib
import numpy as np
from nibabel.testing import data_path
from PIL import Image
import SimpleITK as sitk
import random
import math


# Normalize the image to (0, 255)
def normalization(my_slice):
    my_max = np.nanmax(my_slice)
    my_adjusted = np.true_divide(my_slice, my_max) * 255
    return my_adjusted


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
    # print(translated[:5])
    return translated


def coordinates_rotation(coordinates, axis, angle, rotationCenter):
    rotation = sitk.VersorTransform(axis, angle, rotationCenter)
    # theta = np.pi/1000
    # rotation = sitk.VersorTransform()
    # type_of_rotation = "x"
    # if type_of_rotation == "x":
    #     rotation.SetMatrix([math.cos(theta), -math.sin(theta), 0, math.sin(theta), math.cos(theta), 0, 0, 0, 1])
    # if type_of_rotation == "y":
    #     rotation.SetMatrix([math.cos(theta), 0, math.sin(theta), 0, 1, 0, -math.sin(theta), 0, math.cos(theta)])
    # if type_of_rotation == "z":
    #     rotation.SetMatrix([1, 0, 0, 0, math.cos(theta), -math.sin(theta), 0, math.sin(theta), math.cos(theta)])
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
            # print(i,j)
            coordinate_tuple = transformed_coordinates[counter]
            # print(coordinate_tuple)
            x = int(coordinate_tuple[0])
            y = int(coordinate_tuple[1])
            z = int(coordinate_tuple[2] + slice_index)
            # print(i, j)
            # print(x, y, z)
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
    adjusted_1_img = Image.fromarray(adjusted_1)
    return adjusted_1_img


def random_movement_translation():
    x = math.floor(random.uniform(-2.999, 3.999))
    y = math.floor(random.uniform(-2.999, 3.999))
    z = math.floor(random.uniform(-2.999, 3.999))
    return x, y, z


def random_movement_rotation():
    theta = random.uniform(-5, 5)*np.pi/180
    phi = random.uniform(-5, 5) * np.pi / 180
    r = random.uniform(-5, 5)*np.pi/180
    return theta, phi, r


# load file
example_filename = os.path.join(data_path, '/Users/chloewang/Downloads/guest-20180601_154359/104_HH/T2/NIfTI/IXI104-HH-1450-T2.nii.gz')
volume = nib.load(example_filename)
volume_data = volume.get_data()
# print(volume_data.shape)
# select central slice
slice_index = int(min(list(volume_data.shape))/2)
slice_0 = volume_data[:, :, slice_index]
# normalize pixel intensities to (0, 255)
adjusted_0 = normalization(slice_0)
# visualize the central slice
slice_0_img = Image.fromarray(adjusted_0)
slice_0_img.show("gray")
# get random motion parameters
x, y, z = random_movement_translation()
print(x, y, z)
theta, phi, r = random_movement_rotation()
print(theta, phi, r)
# get transformed slice and visualize it
new_slice_img = rigid_transform(slice_0, volume_data, x, y, z, theta, phi, r, slice_index)
new_slice_img.show("gray")
