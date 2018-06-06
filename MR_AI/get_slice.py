import os
import nibabel as nib
import numpy as np
from nibabel.testing import data_path
from PIL import Image
import SimpleITK as sitk


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


def coordinates_rotation(coordinates, axis, theta, rotationCenter):
    rotation = sitk.VersorTransform(axis, theta, rotationCenter)
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
            ###
            # print(i,j)
            coordinate_tuple = transformed_coordinates[counter]
            # print(coordinate_tuple)
            x = int(coordinate_tuple[0])
            y = int(coordinate_tuple[1])
            z = int(coordinate_tuple[2] + slice_index)
            print(i, j)
            print(x, y, z)
            if x < 256 and y < 256 and z < 130:
                new_slice[i, j] = volume_data[x, y, z]
            else:
                new_slice[i, j] = 0
            counter += 1
    return new_slice


# load file
example_filename = os.path.join(data_path, '/Users/chloewang/Downloads/guest-20180601_154359/104_HH/T2/NIfTI/IXI104-HH-1450-T2.nii.gz')
volume = nib.load(example_filename)
my_volume_data = volume.get_data()
# print(my_volume_data.shape)
my_slice_index = 65
slice_0 = my_volume_data[:, :, my_slice_index]
# normalize pixel intensities to (0, 255)
adjusted_0 = normalization(slice_0)
# visualize the image
slice_0_img = Image.fromarray(adjusted_0)
slice_0_img.show("gray")
#slice_0_img.save('/Users/chloewang/Desktop/test_img/orginal.jpg')

# Get coordinates from the slice
slice_0_expanded = np.expand_dims(slice_0, axis=2)
my_coordinates = to_coordinates(slice_0_expanded)
# perform translation
t = (0,0,0)
translated_coordinates = coordinates_translation(my_coordinates, t)
# perform rotation
# x: up and down
# y: left and right
# z: rotate within plane
axis = [1, 0, 0]
theta = -np.pi/30
rotationCenter = (128, 128, 0)
my_transformed_coordinates = coordinates_rotation(translated_coordinates, axis, theta, rotationCenter)
#print(translated_and_rotated_coordinates)
#print(transformed_coordinates)

# Fetch points based on transformed coordinates. Put together new slice.
slice_1 = fetch_points(my_transformed_coordinates, my_volume_data, my_slice_index)
adjusted_1 = normalization(slice_1)
adjusted_1_img = Image.fromarray(adjusted_1)
adjusted_1_img.show("gray")
# adjusted_1_img.save('/Users/chloewang/Desktop/test_img/pi_over_90.jpg')
