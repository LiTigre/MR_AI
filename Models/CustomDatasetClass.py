import pandas as pd
import numpy as np
import os
import cv2

class CustomDatasetFromImages(Dataset):
    def __init__(self, csv_path, FolderName):
        """
        Args:
            csv_path (string): path to csv file with labels
            img_path (string): path to the folder where images are
            transform: pytorch transforms for transforms and tensor conversion
        """
        # Transforms
        #self.to_tensor = transforms.ToTensor()
        # Read the csv file
        self.data_info = pd.read_csv(csv_path, header=None, nrows=100)
        # First column contains the image paths
        #self.image_arr = np.asarray(self.data_info.iloc[:, 0])
        self.image_arr = np.asarray(self.data_info.iloc[:, 0])
        # Second column is the labels
        #self.label_arr = np.asarray(self.data_info.iloc[:, 1])
        self.label_arr = np.asarray(self.data_info.iloc[:, 1])
        self.data_len = len(self.data_info.index)
        self.foldername = FolderName

    def __getitem__(self, index):
        # Get image name from the pandas df
        print('index number {}'.format(index))
        single_image_name = self.image_arr[index]
        # Open image
        img_as_img = cv2.imread(self.foldername + '/'+ str(single_image_name), 0)
        img_as_img = img_as_img[np.newaxis,...]
        img_as_img = img_as_img/255
        img_as_tensor = torch.tensor(img_as_img, dtype=torch.float)
        
        single_label_name = self.label_arr[index]
        label_as_img = cv2.imread(self.foldername + '/'+ str(single_label_name), 0)
        label_as_img = label_as_img[np.newaxis,...]
        label_as_img = label_as_img/255
        label_as_tensor = torch.tensor(label_as_img, dtype=torch.float)

        return (img_as_tensor, label_as_tensor)
        

    def __len__(self):
        return self.data_len

        