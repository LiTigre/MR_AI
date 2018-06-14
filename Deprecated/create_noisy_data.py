import os
import nibabel as nib
import numpy as np

from nibabel.testing import data_path
import matplotlib.pyplot as plt
from nibabel import viewers
from PIL import Image


#path to all the data
PATH = '/Users/li-tigre/Downloads/guest-20180601_153951/'

#path to the 'to' folder
T2 = '/Users/li-tigre/Downloads/lol/T2_noisy/'


for file_1 in os.listdir(PATH):
	if '.' not in str(file_1):
		for file_2 in os.listdir(PATH + file_1 + '/'):
			#make sure that it's a T2
			if '.' not in str(file_2) && file_2 == 'T2':
				for file_3 in os.listdir(PATH + file_1 + '/' + file_2 + '/'):
					if '.' not in str(file_3):
						for file_4 in os.listdir(PATH + file_1 + '/' + file_2 + '/' + file_3 + '/'):
							if file_4.endswith('.gz'):
								



