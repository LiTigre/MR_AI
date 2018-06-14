import os
import nibabel as nib
import numpy as np
from nibabel.testing import data_path
from PIL import Image
import SimpleITK as sitk
import random
import math
import cv2


# Normalize the image to (0, 255)
def normalization(my_slice):
    my_max = np.nanmax(my_slice)
    my_min = np.nanmin(my_slice)
    my_difference = my_max - my_min
    print(my_difference)
    my_adjusted = np.true_divide(my_slice - my_min, my_difference) * 255
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
    #new_slice = np.zeros((256, 256))
    new_slice = np.zeros((256, 320))
    counter = 0
    for j in range(320):
    #for j in range(255):
        for i in range(256):
            #for i in range(256)
            # print(i,j)
            coordinate_tuple = transformed_coordinates[counter]
            # print(coordinate_tuple)
            x = int(coordinate_tuple[0])
            y = int(coordinate_tuple[1])
            z = int(coordinate_tuple[2] + slice_index)
            print(i, j)
            print(x, y, z)
            # if 0 <= x < 256 and 0 <= y < 256 and 0 <= z < 130:
            if 0 <= x < 256 and 0 <= y < 320 and 0 <= z < 320:
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
    #rotationCenter = (128, 128, 0)
    rotationCenter = (128, 160, 0)
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


def resizeAndPad(img, size, padColor=0):

    h, w = img.shape[:2]
    sh, sw = size

    # interpolation method
    if h > sh or w > sw: # shrinking image
        interp = cv2.INTER_AREA
    else: # stretching image
        interp = cv2.INTER_CUBIC

    # aspect ratio of image
    aspect = w/h  # if on Python 2, you might need to cast as a float: float(w)/h

    # compute scaling and pad sizing
    if aspect > 1: # horizontal image
        new_w = sw
        new_h = np.round(new_w/aspect).astype(int)
        pad_vert = (sh-new_h)/2
        pad_top, pad_bot = np.floor(pad_vert).astype(int), np.ceil(pad_vert).astype(int)
        pad_left, pad_right = 0, 0
    elif aspect < 1: # vertical image
        new_h = sh
        new_w = np.round(new_h*aspect).astype(int)
        pad_horz = (sw-new_w)/2
        pad_left, pad_right = np.floor(pad_horz).astype(int), np.ceil(pad_horz).astype(int)
        pad_top, pad_bot = 0, 0
    else: # square image
        new_h, new_w = sh, sw
        pad_left, pad_right, pad_top, pad_bot = 0, 0, 0, 0

    # set pad color
    if len(img.shape) is 3 and not isinstance(padColor, (list, tuple, np.ndarray)): # color image but only one color provided
        padColor = [padColor]*3

    # scale and pad
    scaled_img = cv2.resize(img, (new_w, new_h), interpolation=interp)
    scaled_img = cv2.copyMakeBorder(scaled_img, pad_top, pad_bot, pad_left, pad_right, borderType=cv2.BORDER_CONSTANT, value=padColor)

    return scaled_img

# load file
# example_filename = os.path.join(data_path, '/Users/chloewang/Downloads/guest-20180601_154359/104_HH/T2/NIfTI/IXI104-HH-1450-T2.nii.gz')
example_filename = os.path.join(data_path, '/Users/chloewang/Downloads/MRI_1000_T2/100307_3T_T2w_SPC1.nii.gz')
volume = nib.load(example_filename)
volume_data = volume.get_data()
print(volume_data.shape)
# select central slice
# slice_index = int(min(list(volume_data.shape))/2)
slice_index = 158
slice_0 = volume_data[:,:,slice_index]
# normalize pixel intensities to (0, 255)
adjusted_0 = normalization(slice_0)
# visualize the central slice
slice_0_img = Image.fromarray(adjusted_0)
slice_0_img.show("gray")
# slice_0_img.convert('RGB').save('original.jpg')
# get random motion parameters
x, y, z = random_movement_translation()
print(x, y, z)
theta, phi, r = random_movement_rotation()
print(theta, phi, r)
# get transformed slice and visualize it
new_slice_img = rigid_transform(slice_0, volume_data, x, y, z, theta, phi, r, slice_index)
print(x, y, z)
print(theta, phi, r)
new_slice_img.show("gray")
# new_slice_img.convert('RGB').save('modified.jpg')
new_slice_img.convert('RGB')
new_img = resizeAndPad(new_slice_img, (256, 256), 0)
cv2.imshow("image", new_img)