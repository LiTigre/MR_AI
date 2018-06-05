import numpy as np
import os
import cv2
import nibabel as nib

from nibabel.testing import data_path
import matplotlib.pyplot as plt
from nibabel import viewers
from PIL import Image


def noisy(noise_typ,image):
	if noise_typ == "gauss":
		row, col, ch = image.shape
		mean = 0
		var = 0.1
		sigma = var**0.5
		gauss = np.random.normal(mean,sigma,(row,col,ch))
		gauss = gauss.reshape(row,col,ch)
		noisy = image + gauss
		return noisy
	elif noise_typ == "s&p":
		row,col,ch = image.shape
		s_vs_p = 0.5
		amount = 0.004
		out = np.copy(image)
		# Salt mode
		num_salt = np.ceil(amount * image.size * s_vs_p)
		coords = [np.random.randint(0, i - 1, int(num_salt))
				for i in image.shape]
		out[coords] = 1

		# Pepper mode
		num_pepper = np.ceil(amount* image.size * (1. - s_vs_p))
		coords = [np.random.randint(0, i - 1, int(num_pepper))
				for i in image.shape]
		out[coords] = 0
		return out
	elif noise_typ == "poisson":
		vals = len(np.unique(image))
		vals = 2 ** np.ceil(np.log2(vals))
		noisy = np.random.poisson(image * vals) / float(vals)
		return noisy
	elif noise_typ =="speckle":
		row,col,ch = image.shape
		gauss = np.random.randn(row,col,ch)
		gauss = gauss.reshape(row,col,ch)        
		noisy = image + image * gauss
		return noisy


T1 = '/Users/li-tigre/Downloads/lol/T1/'
T1_noise = '/Users/li-tigre/Downloads/lol/T1_noisy/'
T2 = '/Users/li-tigre/Downloads/lol/T2/'
T2_noise = '/Users/li-tigre/Downloads/lol/T2_noisy/'

for file in os.listdir(T1):
	print(file)
	if file != '.' and file != '.DS_Store':
		img = cv2.imread(T1 + file)
		# img_data = img.get_data()

		out = noisy("gauss", img)
		# slice_0_img = Image.fromarray(out)
		cv2.imwrite(T1_noise + file, out)
		# out.save(T1_noisy + file)

for file in os.listdir(T2):
	print(file)
	if file != '.' and file != '.DS_Store':
		img = cv2.imread(T2 + file)
		# img_data = img.get_data()

		out = noisy("gauss", img)
		# slice_0_img = Image.fromarray(out)
		cv2.imwrite(T2_noise + file, out)
		# out.save(T1_noisy + file)


# img = nib.load(PATH + file_1 + '/' + file_2 + '/' + file_3 + '/' + file_4)
# img_data = img.get_data()
# # print(img_data.shape)
# # print(list(img_data.shape))

# middle_index = int(min(list(img_data.shape))/2)


# slice_0 = img_data[:, :, middle_index]
# # print(slice_0)

# array_max = np.amax(slice_0)

# adjusted = np.true_divide(slice_0, array_max) * 255

# slice_0_img = Image.fromarray(adjusted).convert('RGB')

# if 'T1' in file_4:
#   slice_0_img.save(T1 + 's_' + str(count_t1) + '.jpg')
#   count_t1 += 1
# else:
#   slice_0_img.save(T2 + 'h_' + str(count_t2) + '.jpg')                  
#   count_t2 += 1
				








