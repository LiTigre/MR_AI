import numpy as np
from numpy.fft import fftshift, ifftshift, fftn, ifftn
import cv2
import os
from PIL import Image
import nibabel as nib
from matplotlib import pyplot as plt

#PATHS to the images
T1 = '/Users/li-tigre/Downloads/lol/T1/'
T2 = '/Users/li-tigre/Downloads/lol/T2/'
EXPORT_T1 = '/Users/li-tigre/Downloads/lol/T1_k_space/'
EXPORT_T2 = '/Users/li-tigre/Downloads/lol/T2_k_space/'


#make the directories if they do not exist
if not os.path.exists(EXPORT_T1):
	os.makedirs(EXPORT_T1)

if not os.path.exists(EXPORT_T2):
	os.makedirs(EXPORT_T2)

for file in os.listdir(T1):
	if file != '.DS_Store':
		print(file)
		#read the image in black/white
		img = cv2.imread(T1 + file, 0)

		#perform the fft
		f = np.fft.fft2(img)
		fshift = np.fft.fftshift(f)
		magnitude_spectrum = 20*np.log(np.abs(fshift))


		img_f = Image.fromarray(magnitude_spectrum)
		# img_f.show()
		img_f = img_f.convert('L')


		img_f.save(EXPORT_T1 + file)


for file in os.listdir(T2):
	if file != '.DS_Store':
		print(file)
		#read the image in black/white
		img = cv2.imread(T2 + file, 0)

		#perform the fft
		f = np.fft.fft2(img)
		fshift = np.fft.fftshift(f)
		magnitude_spectrum = 20*np.log(np.abs(fshift))


		img_f = Image.fromarray(magnitude_spectrum)
		# img_f.show()
		img_f = img_f.convert('L')


		img_f.save(EXPORT_T2 + file)


