import numpy as np
from numpy.fft import fftshift, ifftshift, fftn, ifftn
import cv2
from PIL import Image
import nibabel as nib
from matplotlib import pyplot as plt
from scipy.ndimage import gaussian_filter



def merge_k_spaces(og_image, tilted_image, percentage = 0.5):

	#perform the fft
	f_1 = np.fft.fft2(img_1)
	f_2 = np.fft.fft2(img_2)

	#add the two images together with the percentage
	f_out = f_1*(1-percentage) + f_2*percentage

	#reverse the fft
	arr_out = np.fft.ifft2(f_out)

	img_out = Image.fromarray(np.abs(arr_out))
	img_blur = gaussian_filter(img_out, sigma=0.1)

	#temporary to show the image
	print(type(img_blur))
	img_show = Image.fromarray(np.abs(img_blur))	
	print(type(img_show))
	img_show.show()


	return img_blur


#choose image that you want to convert to kspace
T1 = '/Users/li-tigre/Downloads/og.jpg'
T2 = '/Users/li-tigre/Downloads/tilted_1.jpg'

#read the image
img_1 = cv2.imread(T1, 0)
img_2 = cv2.imread(T2, 0)
print(img_1)

merge_k_spaces(img_1, img_2, 0.15)



