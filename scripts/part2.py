# -*- coding: utf-8 -*-
"""Copy of MR_AI thingy - v1

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1eN6eiyvtllew2gaTzaXr89E7rTUeVcNA
"""

import os
import time
import platform
import io

import matplotlib.pyplot as plt
from matplotlib.pyplot import cm


# from __future__ import print_function, division
import pandas as pd
from skimage import io, transform
import numpy as np
import matplotlib.pyplot as plt

# !wget https://raw.githubusercontent.com/StefOe/colab-pytorch-utils/master/utils.py
# import utils as colabutils

# Ignore warnings
import warnings
warnings.filterwarnings("ignore")

# from google.colab import files
import zipfile

# from pydrive.auth import GoogleAuth
# from pydrive.drive import GoogleDrive
# from google.colab import auth
# from oauth2client.client import GoogleCredentials

# def install_pytorch():
#     os = platform.system()
#     if os == "Linux":
#         !pip3 install http://download.pytorch.org/whl/cu90/torch-0.4.0-cp36-cp36m-linux_x86_64.whl
#     elif os == "Windows":
#         !pip3 install http://download.pytorch.org/whl/cu90/torch-0.4.0-cp36-cp36m-win_amd64.whl 
#     !pip3 install torchvision

# # Install PyTorch.
# install_pytorch()

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils


from PIL import Image
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
        # with open ('drive/outfile.p', 'rb') as fp:
        # itemlist = pickle.load(fp)
        # print(self.data_info[0])
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


def register_extension(id, extension): Image.EXTENSION[extension.lower()] = id.upper()
Image.register_extension = register_extension
def register_extensions(id, extensions): 
  for extension in extensions: register_extension(id, extension)
Image.register_extensions = register_extensions

#my_dataset_test = CustomDatasetFromImages("/content/data/train/train_names.csv", "train")

# my_dataset_val = CustomDatasetFromImages("/Users/li-tigre/Downloads/reconstruction_val_names.csv", "/Users/li-tigre/Downloads/Validation")

my_dataset_train = CustomDatasetFromImages("/Users/li-tigre/Downloads/reconstruction_val_names.csv", "/Users/li-tigre/Downloads/Validation")

import torchvision.datasets as data

import torchvision.transforms as transforms

import random

batch_size = 2

train_loader = torch.utils.data.DataLoader(my_dataset_train, batch_size, shuffle=True)

# test_loader = torch.utils.data.DataLoader(my_dataset_test, batch_size, shuffle=True)

# val_loader = torch.utils.data.DataLoader(my_dataset_val, batch_size, shuffle=True)

#create dictionary for hyperparameters
#following Sumana's recommendations


params1 =  {
    
    #256, 256, 1
    'conv1': {
        'in_channel': 1,
#         'in_channel': 3,   #to change depending on input
        'out_channel': 8,
        'kernel_size': 5,
        'stride': 1
    },
    #254, 254, 8 
    'conv2': {
        'in_channel': 8, #refer to conv1_out_channel
        'out_channel': 16,
        'kernel_size': 5,
        'stride': 1
    },
    #252, 252, 16
    'conv3': {
        'in_channel': 16, #refer to conv1_out_channel
        'out_channel': 32,
        'kernel_size': 5,
        'stride': 1
    },
    #250, 250, 32
    'conv4': {
        'in_channel': 32, #refer to conv1_out_channel
        'out_channel': 64,
        'kernel_size': 5,
        'stride': 1
    },
    #248, 248, 64
    'conv5': {
        'in_channel': 64, #refer to conv1_out_channel
        'out_channel': 128,
        'kernel_size': 5,
        'stride': 1
    },
    #12, 12, 128
    #maxpoll
    #6, 6, 128
    
}





import torch
import torch.nn as nn
import tensorflow as tf
import torch.nn.functional as F
from scipy import signal as signal
# torch.manual_seed(1234)

class ConvNet(nn.Module):
    def __init__(self):
      
        super(ConvNet, self).__init__()
        
        # Convolution layers
        # torch.nn.Conv2d(in_channels, out_channels, kernel_size, stride=1, padding=0, dilation=1, groups=1, bias=True)[source]
        self.conv1 = nn.Conv2d(in_channels = params1['conv1']['in_channel'], 
                               out_channels = params1['conv1']['out_channel'], 
                               kernel_size = params1['conv1']['kernel_size'], 
                               stride=params1['conv1']['stride'])
        
        self.batch1 = nn.BatchNorm2d(params1['conv1']['out_channel'], eps=1e-5, momentum=0.1, affine=True)

        self.conv2 = nn.Conv2d(in_channels = params1['conv2']['in_channel'], 
                               out_channels = params1['conv2']['out_channel'], 
                               kernel_size = params1['conv2']['kernel_size'], 
                               stride=params1['conv2']['stride'])
        
        self.batch2 = nn.BatchNorm2d(params1['conv2']['out_channel'], eps=1e-5, momentum=0.1, affine=True)

        self.conv3 = nn.Conv2d(in_channels = params1['conv3']['in_channel'], 
                               out_channels = params1['conv3']['out_channel'], 
                               kernel_size = params1['conv3']['kernel_size'], 
                               stride=params1['conv3']['stride'])
        
        self.batch3 = nn.BatchNorm2d(params1['conv3']['out_channel'], eps=1e-5, momentum=0.1, affine=True)

        self.conv4 = nn.Conv2d(in_channels = params1['conv4']['in_channel'], 
                               out_channels = params1['conv4']['out_channel'], 
                               kernel_size = params1['conv4']['kernel_size'], 
                               stride=params1['conv4']['stride'])

        self.batch4 = nn.BatchNorm2d(params1['conv4']['out_channel'], eps=1e-5, momentum=0.1, affine=True)

        self.conv5 = nn.Conv2d(in_channels = params1['conv5']['in_channel'], 
                               out_channels = params1['conv5']['out_channel'], 
                               kernel_size = params1['conv5']['kernel_size'], 
                               stride=params1['conv5']['stride'])
        
        self.batch5 = nn.BatchNorm2d(params1['conv5']['out_channel'], eps=1e-5, momentum=0.1, affine=True)
     
        self.unconv1 = nn.ConvTranspose2d(in_channels = params1['conv5']['out_channel'], 
                                           out_channels = params1['conv5']['in_channel'], 
                                           kernel_size = params1['conv5']['kernel_size'], 
                                           stride=params1['conv5']['stride'])
        self.unconv2 = nn.ConvTranspose2d(in_channels = params1['conv4']['out_channel'], 
                                           out_channels = params1['conv4']['in_channel'], 
                                           kernel_size = params1['conv5']['kernel_size'], 
                                           stride=params1['conv5']['stride'])
        self.unconv3 = nn.ConvTranspose2d(in_channels = params1['conv3']['out_channel'], 
                                           out_channels = params1['conv3']['in_channel'], 
                                           kernel_size = params1['conv5']['kernel_size'], 
                                           stride=params1['conv5']['stride'])
        self.unconv4 = nn.ConvTranspose2d(in_channels = params1['conv2']['out_channel'], 
                                           out_channels = params1['conv2']['in_channel'], 
                                           kernel_size = params1['conv5']['kernel_size'], 
                                           stride=params1['conv5']['stride'])
        self.unconv5 = nn.ConvTranspose2d(in_channels = params1['conv1']['out_channel'], 
                                           out_channels = params1['conv1']['in_channel'], 
                                           kernel_size = params1['conv5']['kernel_size'], 
                                           stride=params1['conv5']['stride'])


        # Pooling layers
        #class torch.nn.MaxPool2d(kernel_size, stride=None, padding=0, dilation=1, return_indices=False, ceil_mode=False)
        self.max2d = nn.MaxPool2d(kernel_size= 2)
        # class torch.nn.AvgPool2d(kernel_size, stride=None, padding=0, ceil_mode=False, count_include_pad=True)
        self.avgpool2d = nn.AvgPool2d(kernel_size = 2)
        
        # Non-linear activations
        self.relu = nn.ReLU()
        self.softmax = nn.Softmax()
        self.sigmoid = nn.Sigmoid()
        
        for m in self.modules():
          if isinstance(m, nn.Conv2d):
            nn.init.xavier_uniform(m.weight.data)
            nn.init.constant(m.bias.data, 0.01)
          elif isinstance(m, nn.Linear):
            nn.init.xavier_uniform(m.weight.data)
            nn.init.constant(m.bias.data, 0.01)
         
          
        
        
#         self.block1 = nn.Sequential(
#             #256, 256, 1
#             nn.Conv2d(1, 8, 14, stride=1),
#             #121, 121, 8
#             nn.ReLU(),
#             nn.MaxPool2d(2)
#             #
#         )
            
#         self.block2 = nn.Sequential(
#             nn.Conv2d(8, 16, 5, stride=2),
#             nn.ReLU(),
#             nn.MaxPool2d(2)
#         )
            
#         self.block3 = nn.Sequential(
#             nn.Linear(3600, 3600),
#             nn.Linear(3600, 2),
#             nn.Softmax()
#         )


    def forward(self, x):
        # out = x/255
        out = self.relu(self.batch1(self.conv1(x)))
        out = self.relu(self.batch2(self.conv2(out)))
        out = self.relu(self.batch3(self.conv3(out)))
        out = self.relu(self.batch4(self.conv4(out)))
        out = self.relu(self.batch5(self.conv5(out)))
        # print(out.shape)
        out = self.relu(self.unconv1(out))
        out = self.relu(self.unconv2(out))
        out = self.relu(self.unconv3(out))
        out = self.relu(self.unconv4(out))
        out = self.relu(self.unconv5(out))
        # print(out.shape)
        out = self.sigmoid(out)
        return out

neural_net = ConvNet()

# use_gpu = torch.cuda.is_available()
# print("GPU Available: {}".format(use_gpu))
# if use_gpu:
#   # switch model to GPU
#   neural_net.cuda()

import torch.nn.functional as F
criterion = nn.MSELoss()

def cost_function(prediction, target):
    loss = criterion(prediction, target)
    return loss

# Define optimizer
import torch.optim as optim

# optimizer = optim.SGD(MyFirstModel.parameters(), lr=0.001) 
optimizer = optim.Adam(neural_net.parameters(), lr=0.0001)

def train(epoch, model, train_loader, optimizer):
    model.train()
    
    total_loss = 0
    correct = 0
    t0 = time.time()
    for batch_idx, (data, target) in enumerate(train_loader):
        # target = target.long()
        print('start batch {}'.format(batch_idx))
        t_start = time.time()
        # print(batch_idx)
        # set data and target to cuda
        # if use_gpu:
        #   data = data.cuda()
        #   target = target.cuda()

        # initialize the gradients to zero 
        optimizer.zero_grad()

        # execute the model
        prediction = model(data)

        # # compute the loss
        loss = cost_function(prediction, target)

        # compute the gradients 
        loss.backward()

        # update the parameters 
        optimizer.step()

        # accumulate the loss of each minibatch
        total_loss += loss.data[0]*len(data)

        # compute the accuracy per minibatch  
        # pred_classes = prediction.data.max(1, keepdim=True)[1]
        # correct += pred_classes.eq(target.data.view_as(pred_classes)).sum().double()

        t_end = time.time()

        print('Epoch {}, batch_id: {},  time : {}, loss: {}'.format(epoch, batch_idx,t_end - t_start, loss.data[0]*len(data)))
        # print('Acc: {:.5f} for batch {}'.format(pred_classes.eq(target.data.view_as(pred_classes)).sum().double(), batch_idx))

    tf = time.time()

    print('Epoch {}, time : {}'.format(epoch, tf - t0))

    # compute the mean loss for each epoch 
    mean_loss = total_loss/len(train_loader.dataset)
    
    # compute the accuracy for each epoch 
    acc = correct / len(train_loader.dataset)
        
    print('Train Epoch: {}   Avg_Loss: {:.5f}'.format(
        epoch, mean_loss, correct, len(train_loader.dataset)))   
    
    return mean_loss, acc

def save_model(epoch, model, path='/Users/li-tigre/Downloads/'):
    
    # file name and path 
    filename = path + 'neural_network_{}.pt'.format(epoch)
    
    # load the model parameters 
    torch.save(model.state_dict(), filename)
    
    return model

def eval(model, test_loader):
    
    # set the model in .eval() mode 
    model.eval()
    
    total_loss = 0
    correct = 0
    
    # iterate over all the mini-batches 
    for batch_idx, (data, target) in enumerate(test_loader):
        

        # if use_gpu:
        #   data = data.cuda()
        #   target = target.cuda()
        
        prediction = model(data)
        
        # compute the loss
        # cross entrophy function
        loss = cost_function(prediction, target) 
        
        # accumulate the loss of each minibatch
        total_loss += loss.data[0]*len(data)
        
        # compute the accuracy per minibatch  
        pred_classes = prediction.data.max(1, keepdim=True)[1]
        correct += pred_classes.eq(target.data.view_as(pred_classes)).sum().double()
    # compute the mean loss
    mean_loss = total_loss/len(test_loader.dataset)
    
    # compute the accuracy 

    acc = correct / len(test_loader.dataset)
        
    print('Eval:  Avg_Loss: {:.5f}   Acc: {}/{} ({:.3f}%)'.format(
        mean_loss, correct, len(test_loader.dataset),
        100. * acc)) 
    
    return mean_loss, acc

def load_model(epoch, model, path='/Users/li-tigre/Downloads/'):
    
    # file name and path 
    filename = path + 'neural_network_{}.pt'.format(epoch)
    
    # load the model parameters 
    model.load_state_dict(torch.load(filename))
    
    
    return model

# Number of epochs 
numEpochs = 4

# checkpoint frequency 
checkpoint_freq = 2

# path to save the data 
path = './'

# empty lists 
train_losses = []
val_losses = []

train_accuracies = []
val_accuracies = []

# traininng 
for epoch in range(1, numEpochs + 1):
    
    # train() function (see above)
    train_loss, train_acc = train(epoch, neural_net, train_loader, optimizer)
    
    # eval() functionn (see above)
    # val_loss, val_acc = eval(neural_net, val_loader)    
    
    # append lists for plotting and printing 
    train_losses.append(train_loss)    
    # val_losses.append(val_loss)
    
    train_accuracies.append(train_acc)    
    # val_accuracies.append(val_acc)
    
    # Checkpoint
    # if epoch % checkpoint_freq ==0:
    save_model(epoch, neural_net, path)

# Last checkpoint
save_model(numEpochs, neural_net, path)
    
print("\n\n\nOptimization ended.\n")

test_loss, test_acc = eval(neural_net, test_loader)
print(test_acc)

x = list(range(len(train_accuracies)))

ax = plt.subplot(111)
plt.plot(x, train_accuracies, 'r', label="Train")
plt.plot(x, val_accuracies, 'g', label="Validation")
plt.title('Accuracy')
leg = plt.legend(loc='best', ncol=2, mode="expand", shadow=False, fancybox=False)
leg.get_frame().set_alpha(0.99)

x = list(range(len(train_accuracies)))

ax = plt.subplot(111)
plt.plot(x, train_accuracies, 'r', label="Train")
plt.plot(x, val_accuracies, 'g', label="Validation")
plt.title('Accuracy')
leg = plt.legend(loc='best', ncol=2, mode="expand", shadow=False, fancybox=False)
leg.get_frame().set_alpha(0.99)
