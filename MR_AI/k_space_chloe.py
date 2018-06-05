import numpy as np
from numpy.fft import fftshift, ifftshift, fftn, ifftn
import cv2
from PIL import Image
import nibabel as nib
from matplotlib import pyplot as plt

#choose image that you want to convert to kspace
T1 = '/Users/li-tigre/Downloads/lol/T1/s_1.jpg'

#read the image
img = cv2.imread(T1, 0)

#perform the 
f = np.fft.fft2(img)
fshift = np.fft.fftshift(f)
magnitude_spectrum = 20*np.log(np.abs(fshift))


img_f = Image.fromarray(magnitude_spectrum)
# img_f.show()
img_f = img_f.convert('L')


img_f.save('/Users/li-tigre/Desktop/foo.jpg')
