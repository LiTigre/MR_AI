import numpy as np
from numpy.fft import fftshift, ifftshift, fftn, ifftn
import cv2
from PIL import Image
import nibabel as nib
from matplotlib import pyplot as plt

# #choose image that you want to convert to kspace
# T1 = '/Users/li-tigre/Downloads/og.jpg'
# T2 = '/Users/li-tigre/Downloads/tilted.jpg'

# #read the image
# img_1 = cv2.imread(T1, 0)
# img_2 = cv2.imread(T2, 0)


def merge_k_spaces(og_image, tilted_image, percentage = 0.5):

	#perform the fft
	f_1 = np.fft.fft2(img_1)
	f_2 = np.fft.fft2(img_2)

	#add the two images together
	f_out = f_1*(1-percentage) + f_2*percentage


	rip_1 = np.fft.ifft2(f_out)

	rip2 = Image.fromarray(np.abs(rip_1))
	rip2.show()


	return rip_1
