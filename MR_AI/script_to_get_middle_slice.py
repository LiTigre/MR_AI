import os
import nibabel as nib
import numpy as np
from nibabel.testing import data_path
import matplotlib.pyplot as plt
from nibabel import viewers
from PIL import Image

count_t1 = 1
count_t2 = 1

PATH = '/Users/li-tigre/Downloads/guest-20180601_153951/'
T1 = '/Users/li-tigre/Downloads/lol/T1/'
T2 = '/Users/li-tigre/Downloads/lol/T2/'


for file_1 in os.listdir(PATH):
	if '.' not in str(file_1):
		# print(file_1)
		for file_2 in os.listdir(PATH + file_1 + '/'):
			if '.' not in str(file_2):
				print(file_2)
				for file_3 in os.listdir(PATH + file_1 + '/' + file_2 + '/'):
					if '.' not in str(file_3):
						for file_4 in os.listdir(PATH + file_1 + '/' + file_2 + '/' + file_3 + '/'):
							if file_4.endswith('.gz'):
								print(file_4)

								img = nib.load(PATH + file_1 + '/' + file_2 + '/' + file_3 + '/' + file_4)
								img_data = img.get_data()
								# print(img_data.shape)
								# print(list(img_data.shape))

								middle_index = int(min(list(img_data.shape))/2)


								slice_0 = img_data[:, :, middle_index]
								# print(slice_0)

								array_max = np.amax(slice_0)

								adjusted = np.true_divide(slice_0, array_max) * 255

								slice_0_img = Image.fromarray(adjusted).convert('RGB')

								if 'T1' in file_4:
									slice_0_img.save(T1 + 's_' + str(count_t1) + '.jpg')
									count_t1 += 1
								else:
									slice_0_img.save(T2 + 'h_' + str(count_t2) + '.jpg')									
									count_t2 += 1
								
								# slice_0_img.show("gray")


# example_filename = os.path.join(data_path, '/Users/li-tigre/Downloads/guest-20180601_153951/16_Guys/T1/NIfTI/IXI016-Guys-0697-T1.nii.gz')





