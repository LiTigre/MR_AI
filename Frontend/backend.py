import threading
import time
import os, shutil, webbrowser
import numpy as np

from PIL import Image

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torchvision.datasets as data
import torchvision.transforms as transforms
import random

from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils
import tensorflow as tf

from scipy import signal as signal
import cv2

class CustomDatasetFromImages(Dataset):
    def __init__(self, csv_path, FolderName):
        """
        Args:
            csv_path (string): path to csv file with labels
            img_path (string): path to the folder where images are
            transform: pytorch transforms for transforms and tensor conversion
        """

        self.data_info = pd.read_csv(csv_path, header=None)
        
        self.image_arr = np.asarray(self.data_info.iloc[:, 0])

        self.label_arr = np.asarray(self.data_info.iloc[:, 1])
        self.data_len = len(self.data_info.index)
        self.foldername = FolderName

    def __getitem__(self, index):
        single_image_name = self.image_arr[index]

        img_as_img = cv2.imread(self.foldername + '/'+ str(single_image_name), 0)
        img_as_img = img_as_img[np.newaxis,...]
        img_as_img = img_as_img/255
        
        img_as_tensor = torch.tensor(img_as_img, dtype=torch.float)
        single_image_label = self.label_arr[index]

        return (img_as_tensor, single_image_label)
        

    def __len__(self):
        return self.data_len


def register_extension(id, extension): Image.EXTENSION[extension.lower()] = id.upper()
Image.register_extension = register_extension
def register_extensions(id, extensions): 
  for extension in extensions: register_extension(id, extension)
Image.register_extensions = register_extensions

params =  {

    'conv1': {
        'in_channel': 1,
#         'in_channel': 3,   #to change depending on input
        'out_channel': 8,
        'kernel_size': 3,
        'stride': 1
    },

    'conv2': {
        'in_channel': 8, #refer to conv1_out_channel
        'out_channel': 16,
        'kernel_size': 3,
        'stride': 1
    },
    
    'conv3': {
        'in_channel': 16, #refer to conv1_out_channel
        'out_channel': 32,
        'kernel_size': 3,
        'stride': 1
    },

    'conv4': {
        'in_channel': 32, #refer to conv1_out_channel
        'out_channel': 64,
        'kernel_size': 3,
        'stride': 1
    },


    'conv5': {
        'in_channel': 64, #refer to conv1_out_channel
        'out_channel': 128,
        'kernel_size': 3,
        'stride': 1
    },

 
    'flatten': 6*6*128,
    
    'linear': {
        'lin1_in': 6*6*128, 
        'lin1_out': 3000,
        'lin2_in': 3000,
        'lin2_out': 2000,
        'lin3_in': 2000,
        'lin3_out': 2
    }
    
}

class ConvNet(nn.Module):
    def __init__(self):
      
        super(ConvNet, self).__init__()
        self.conv1 = nn.Conv2d(in_channels = params['conv1']['in_channel'], 
                               out_channels = params['conv1']['out_channel'], 
                               kernel_size = params['conv1']['kernel_size'], 
                               stride=params['conv1']['stride'])
        self.batch1 = nn.BatchNorm2d(params['conv1']['out_channel'], eps=1e-5, momentum=0.1, affine=True)
        self.conv2 = nn.Conv2d(in_channels = params['conv2']['in_channel'], 
                               out_channels = params['conv2']['out_channel'], 
                               kernel_size = params['conv2']['kernel_size'], 
                               stride=params['conv2']['stride'])
        self.batch2 = nn.BatchNorm2d(params['conv2']['out_channel'], eps=1e-5, momentum=0.1, affine=True)
        self.conv3 = nn.Conv2d(in_channels = params['conv3']['in_channel'], 
                               out_channels = params['conv3']['out_channel'], 
                               kernel_size = params['conv3']['kernel_size'], 
                               stride=params['conv3']['stride'])
        self.batch3 = nn.BatchNorm2d(params['conv3']['out_channel'], eps=1e-5, momentum=0.1, affine=True)
        self.conv4 = nn.Conv2d(in_channels = params['conv4']['in_channel'], 
                               out_channels = params['conv4']['out_channel'], 
                               kernel_size = params['conv4']['kernel_size'], 
                               stride=params['conv4']['stride'])
        self.batch4 = nn.BatchNorm2d(params['conv4']['out_channel'], eps=1e-5, momentum=0.1, affine=True)
        self.conv5 = nn.Conv2d(in_channels = params['conv5']['in_channel'], 
                               out_channels = params['conv5']['out_channel'], 
                               kernel_size = params['conv5']['kernel_size'], 
                               stride=params['conv5']['stride']) 
        self.batch5 = nn.BatchNorm2d(params['conv5']['out_channel'], eps=1e-5, momentum=0.1, affine=True)
        
        #Linear layers
        self.linear1 = nn.Linear(in_features = params['linear']['lin1_in'], out_features=params['linear']['lin1_out'])
        self.linear2 = nn.Linear(in_features = params['linear']['lin2_in'], out_features=params['linear']['lin2_out'])
        self.linear3 = nn.Linear(in_features = params['linear']['lin3_in'], out_features=params['linear']['lin3_out']) 
        self.batch_lin_1 = nn.BatchNorm1d(params['linear']['lin1_out'])
        self.batch_lin_2 = nn.BatchNorm1d(params['linear']['lin2_out'])
        self.batch_lin_3 = nn.BatchNorm1d(params['linear']['lin3_out'])

        # Pooling layers
        self.max2d = nn.MaxPool2d(kernel_size= 2)
        self.avgpool2d = nn.AvgPool2d(kernel_size = 2)
        
        # Non-linear activations
        self.relu = nn.ReLU()
        self.softmax =  nn.Softmax()
        
        for m in self.modules():
          if isinstance(m, nn.Conv2d):
            nn.init.xavier_uniform(m.weight.data)
            nn.init.constant(m.bias.data, 0.01)
          elif isinstance(m, nn.Linear):
            nn.init.xavier_uniform(m.weight.data)
            nn.init.constant(m.bias.data, 0.01)
         

    def forward(self, x):
        # out = x/255
        out = self.max2d(self.relu(self.batch1(self.conv1(x))))
        out = self.max2d(self.relu(self.batch2(self.conv2(out))))
        out = self.max2d(self.relu(self.batch3(self.conv3(out))))
        out = self.max2d(self.relu(self.batch4(self.conv4(out))))
        out = self.max2d(self.relu(self.batch5(self.conv5(out))))
        out = out.view(out.size(0), -1)
        out = self.batch_lin_1(self.linear1(out))
        out = self.batch_lin_2(self.linear2(out))
        out = self.batch_lin_3(self.linear3(out))
        out = self.softmax(out)
        
        return out

class Backend:
    def __init__(self, typeNeuralNet):
        self.typeNeuralNet = typeNeuralNet
        self.finished = False
        self.good = 0
        self.uncertain = 0
        self.bad = 0

    def runModel(self, progressBar, inputDir, outputDir):
        #time.sleep(5)
        self.inputDirectory = inputDir
        self.outputDirectory = outputDir

        self.model = ConvNet()
        self.loadModel("")
        self.useModel()
        self.move_files(self.predicitons, self.inputDirectory, self.outputDirectory)

        progressBar.stop()
        self.finished = True
        print("Done")
 
        return (self.good, self.uncertain, self.bad )
    
    def preprocessing(self, img, size, padColor=0):
        h, w = img.shape[:2]
        sh, sw = size

        # interpolation method
        if h > sh or w > sw: # shrinking image
            interp = cv2.INTER_AREA
        else: # stretching image
            interp = cv2.INTER_CUBIC

        # aspect ratio of image
        aspect = w/h  

        # compute scaling and pad sizing
        if aspect > 1: # horizontal image
            new_w = sw
            new_h = np.round(new_w/aspect).astype(int)
            pad_vert = (sh-new_h)/2
            pad_top, pad_bot = np.floor(pad_vert).astype(int), np.ceil(pad_vert).astype(int)
            pad_left, pad_right = 0, 0
        elif aspect < 1: # vertical image
            new_h = sh
            new_w = np.round(new_h*aspect).astype(int)
            pad_horz = (sw-new_w)/2
            pad_left, pad_right = np.floor(pad_horz).astype(int), np.ceil(pad_horz).astype(int)
            pad_top, pad_bot = 0, 0
        else: # square image
            new_h, new_w = sh, sw
            pad_left, pad_right, pad_top, pad_bot = 0, 0, 0, 0

        # set pad color
        if len(img.shape) is 3 and not isinstance(padColor, (list, tuple, np.ndarray)): # color image but only one color provided
            padColor = [padColor]*3

        # scale and pad
        scaled_img = cv2.resize(img, (new_w, new_h), interpolation=interp)
        scaled_img = cv2.copyMakeBorder(scaled_img, pad_top, pad_bot, pad_left, pad_right, borderType=cv2.BORDER_CONSTANT, value=padColor)

        return scaled_img


    def loadModel(self, weightsPath):
        self.model.load_state_dict(torch.load(weightsPath))


    def useModel(self):
        self.dataset = CustomDatasetFromImages("drive/S_and_T_images/Test/Test/test_names.csv", "drive/S_and_T_images/Test/Test/")
        self.testLoader = torch.utils.data.DataLoader(self.dataset, batch_size = 100)#, shuffle=True)

        # set the model in .eval() mode 
        self.model.eval()
        
         # iterate over all the mini-batches
        self.predictions = []
        for batch_idx, (data, target) in enumerate(self.testLoader):
            prediction = self.model(data)
            self.predictions.append(prediction)


    def useModel2(self):
        img_as_img = cv2.imread('test.jpg', 0)
        print(img_as_img)
        img_as_img = preprocessing(img_as_img, (256, 256), 0)
        print(img_as_img.shape)
        img_as_img = img_as_img[np.newaxis, ...]
        img_as_img = img_as_img/255
        
        img_as_tensor = torch.tensor(img_as_img, dtype=torch.float)
        out = self.model(img_as_tensor)
        print(out)
    
    def move_files(self, modelOutputs, inputFolder, outputFolder):
        dir1 = "/good"
        dir2 = "/bad"
        dir3 = "/unsure"
        os.makedirs(os.path.join(outputFolder, dir1))
        os.makedirs(os.path.join(outputFolder, dir2))
        os.makedirs(os.path.join(outputFolder, dir3))

        list_input = [i for i in os.listdir(inputFolder)]

        for i, proba in enumerate(modelOutputs):
            probGood = proba[0]
            probBad = proba[1]

            if probGood > 0.5 :
                shutil.copy(list_input[i], outputFolder+ dir1)
                self.good = self.good + 1
           
            elif probBad > 0.5 :
                shutil.copy(list_input[i], outputFolder+ dir2)
                self.bad = self.bad + 1
            else:
                shutil.copy(list_input[i], outputFolder+ dir3)
                self.uncertain = self.uncertain + 1


    def create_csv(self, inputs, outputs, true_values, rmse_vals=None):
        return



        