import numpy as np
from numpy.fft import fftshift, ifftshift, fftn, ifftn
import cv2
from PIL import Image
import nibabel as nib
from matplotlib import pyplot as plt

#choose image that you want to convert to kspace
T1 = '/Users/li-tigre/Downloads/og.jpg'
T2 = '/Users/li-tigre/Downloads/tilted.jpg'

#read the image
img_1 = cv2.imread(T1, 0)
img_2 = cv2.imread(T2, 0)



#perform the fft
f_1 = np.fft.fft2(img_1)
f_2 = np.fft.fft2(img_2)
print(len(f_2))


# f_1[64:256-64, :] = f_2[64+10:256-64+10, :]


#add the two images together
f_out = (f_1 +f_2)/2


rip_1 = np.fft.ifft2(f_out)
# rip_2 = np.fft.ifft2(f_2)

rip2 = Image.fromarray(np.abs(rip_1))
rip2.show()

img_o = Image.fromarray(f_o).convert('L')
# img1_o = Image.fromarray(img_o)

img_o.save('/Users/li-tigre/Desktop/foo.jpg')




img_2 = cv2.imread('/Users/li-tigre/Desktop/foo.jpg', 0)

f_o = np.fft.ifft2(img_2)
img_o = Image.fromarray(np.abs(f_o)).convert('L')
img_o.save('/Users/li-tigre/Desktop/foo2.jpg')



# f_2 = np.abs(np.fft.ifft2(f))
# img_f = Image.fromarray(f_2)
# img_f.show()





# # fshift_o = np.fft.fftshift(f_o)
# f = np.fft.ifft2(fshift_o)
# # fshift = np.abs(np.fft.ifftshift(f))
# img_f = Image.fromarray(fshift)
# img_f.show()



# magnitude_spectrum = 20*np.log(np.abs(fshift))


# img_f = Image.fromarray(magnitude_spectrum)
# # img_f.show()
# img_f = img_f.convert('L')


# img_f.save('/Users/li-tigre/Desktop/foo.jpg')



# ##########reverse fft


# #read the image
# img = cv2.imread('/Users/li-tigre/Desktop/foo.jpg', 0)

# #perform the 
# f = np.fft.ifft2(img)
# fshift = np.fft.ifftshift(f)

# f_2 = np.abs(np.fft.ifft2(fshift))
# img_f = Image.fromarray(f_2)
# img_f.show()

# # fshift = np.fft.ifftshift(f)
# # magnitude_spectrum = np.power(np.abs(fshift),)
# # magnitude_spectrum = 20*np.log(np.abs(fshift))



# img_f = Image.fromarray(magnitude_spectrum)
# # img_f.show()
# img_f = img_f.convert('L')


# img_f.save('/Users/li-tigre/Desktop/foo2.jpg')


