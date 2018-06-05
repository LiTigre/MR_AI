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




# plt.subplot(121),plt.imshow(img, cmap = 'gray')
# plt.title('Input Image'), plt.xticks([]), plt.yticks([])
# plt.imshow(magnitude_spectrum, cmap = 'gray')
# plt.xticks([]), plt.yticks([])
# # plt.show()

# # plt.xticks([]), plt.yticks([])
# plt.savefig('/Users/li-tigre/Desktop/foo.jpg')


# im = Image.fromarray(fshift, 'L')
# im.save('/Users/li-tigre/Desktop/lol.jpg')
# img_data = img.get_data()
# gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# define evaluation points
# x = -0.5 + np.random.rand(1000)
# print(x)
# print(img)
# # define Fourier coefficients
# N = 10000
# k = N // 2 + np.arange(N)
# f_k = np.random.randn(N)

# # direct Fourier transform
# f_x_fast = nfft.nfft(img, f_k)
# print('hi\n')
# print(f_x_fast.shape)

# # out = nfft(img, f_k)
# # print(type(out))
# im = Image.fromarray(f_x_fast, 'L')
# im.save('/Users/li-tigre/Desktop/lol.jpg')






# def transform_image_to_kspace(img, dim=None, k_shape=None):
#     """ Computes the Fourier transform from image space to k-space space
#     along a given or all dimensions
#     :param img: image space data
#     :param dim: vector of dimensions to transform
#     :param k_shape: desired shape of output k-space data
#     :returns: data in k-space (along transformed dimensions)
#     """
#     if not dim:
#         dim = range(img.ndim)

#     k = fftshift(fftn(ifftshift(img, axes=dim), s=k_shape, axes=dim), axes=dim)
#     k /= np.sqrt(np.prod(np.take(img.shape, dim)))
#     return k

# def transform_kspace_to_image(k, dim=None, img_shape=None):
#     """ Computes the Fourier transform from k-space to image space
#     along a given or all dimensions
#     :param k: k-space data
#     :param dim: vector of dimensions to transform
#     :param img_shape: desired shape of output image
#     :returns: data in image space (along transformed dimensions)
#     """
#     if not dim:
#         dim = range(k.ndim)

#     img = fftshift(ifftn(ifftshift(k, axes=dim), s=img_shape, axes=dim), axes=dim)
#     img *= np.sqrt(np.prod(np.take(img.shape, dim)))
#     return img


# T1 = '/Users/li-tigre/Downloads/lol/T1/s_1.jpg'

# img = cv2.imread(T1)
# # img_data = img.get_data()
# gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# out = transform_image_to_kspace(gray_image)
# print(str(type(out)) + " hi\n")

# im = Image.fromarray(out, 'L')
# im.save('/Users/li-tigre/Desktop/lol.jpg')




# # img = cv2.imread('/Users/li-tigre/Desktop/lol.jpg')
# # img_data = img.get_data()
# # gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# out = transform_kspace_to_image(out)
# im = Image.fromarray(out, 'L')
# im.save('/Users/li-tigre/Desktop/lol2.jpg')




# # img = cv2.imread(T1)
# # # out_1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# # # out = transform_image_to_kspace(out_1)
# # out = transform_image_to_kspace(img)

# # # print(out)

# # print(type(out))
# # slice_0_img = Image.fromarray(out)
# # print('hi')
# # slice_0_img.save('/Users/li-tigre/Desktop/lol.jpg')
# # # cv2.imwrite('/Users/li-tigre/Desktop/lol.jpg', out)
