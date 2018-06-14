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

# from write_names import 

import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
from sklearn.decomposition import PCA

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
        self.data_info = pd.read_csv(csv_path, header=None)
        # First column contains the image paths
        #self.image_arr = np.asarray(self.data_info.iloc[:, 0])
        # with open ('drive/outfile.p', 'rb') as fp:
        # itemlist = pickle.load(fp)
        
        self.image_arr = np.asarray(self.data_info.iloc[:, 0])
        # Second column is the labels
        #self.label_arr = np.asarray(self.data_info.iloc[:, 1])
        self.label_arr = np.asarray(self.data_info.iloc[:, 1])
        self.data_len = len(self.data_info.index)
        self.foldername = FolderName

    def __getitem__(self, index):
        # Get image name from the pandas df
        single_image_name = self.image_arr[index]
        
        # Open image
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

my_dataset_test = CustomDatasetFromImages("/Users/li-tigre/Downloads/plot_names.csv", "/Users/li-tigre/Downloads/plot_test")

# my_dataset_val = CustomDatasetFromImages("/Users/li-tigre/Downloads/val_names.csv", "/Users/li-tigre/Downloads/Validation")

# my_dataset_train = CustomDatasetFromImages("/Users/li-tigre/Downloads/train_names.csv", "/Users/li-tigre/Downloads/Train")

import torchvision.datasets as data

import torchvision.transforms as transforms

import random

batch_size = 51

# train_loader = torch.utils.data.DataLoader(my_dataset_train, batch_size, shuffle=True)

test_loader = torch.utils.data.DataLoader(my_dataset_test, batch_size, shuffle=True)

# val_loader = torch.utils.data.DataLoader(my_dataset_val, batch_size, shuffle=True)

#create dictionary for hyperparameters
#following Sumana's recommendations


params =  {
    
    #256, 256, 1
    'conv1': {
        'in_channel': 1,
#         'in_channel': 3,   #to change depending on input
        'out_channel': 8,
        'kernel_size': 3,
        'stride': 1
    },
    #254, 254, 8
    
    #maxpoll  
    
    #127, 127, 8
    'conv2': {
        'in_channel': 8, #refer to conv1_out_channel
        'out_channel': 16,
        'kernel_size': 3,
        'stride': 1
    },
    #125, 125, 16
    
    
    #maxpoll
    
    
    #62, 62, 16
    
    'conv3': {
        'in_channel': 16, #refer to conv1_out_channel
        'out_channel': 32,
        'kernel_size': 3,
        'stride': 1
    },
    #60, 60, 32
    
    #maxpoll
    
    #30, 30, 32
    'conv4': {
        'in_channel': 32, #refer to conv1_out_channel
        'out_channel': 64,
        'kernel_size': 3,
        'stride': 1
    },
    #28, 28, 64
    
    #maxpoll
    #14, 14, 64

    'conv5': {
        'in_channel': 64, #refer to conv1_out_channel
        'out_channel': 128,
        'kernel_size': 3,
        'stride': 1
    },
    #12, 12, 128
    #maxpoll
    #6, 6, 128

    
    
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

import torch
import torch.nn as nn
import tensorflow as tf
import torch.nn.functional as F
from scipy import signal as signal
# torch.manual_seed(1234)


def plot_thingy(out, y):

    out = out.detach().numpy()
    y = y.detach().numpy()
    pca = PCA(n_components=2)
    X_r = pca.fit(out).transform(out)*255
    print(X_r[:2])
    plt.figure()
    #colors = ['navy','darkorange']
    #lw = 2
    target_names = ['clean', 'blurred']
    #for color, i in zip(colors, [0, 1]):
    plt.scatter(X_r[:, 0], X_r[:, 1], c=y)
    plt.legend(loc='best', shadow=False, scatterpoints=1)
    plt.title('dataset')
    plt.show()


class ConvNet(nn.Module):
    def __init__(self):
      
        super(ConvNet, self).__init__()
        
        # Convolution layers
        # torch.nn.Conv2d(in_channels, out_channels, kernel_size, stride=1, padding=0, dilation=1, groups=1, bias=True)[source]
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
        # class torch.nn.Linear(in_features, out_features, bias=True)
        self.linear1 = nn.Linear(in_features = params['linear']['lin1_in'], out_features=params['linear']['lin1_out'])
        self.linear2 = nn.Linear(in_features = params['linear']['lin2_in'], out_features=params['linear']['lin2_out'])
        self.linear3 = nn.Linear(in_features = params['linear']['lin3_in'], out_features=params['linear']['lin3_out'])
        
        self.batch_lin_1 = nn.BatchNorm1d(params['linear']['lin1_out'])
        self.batch_lin_2 = nn.BatchNorm1d(params['linear']['lin2_out'])
        self.batch_lin_3 = nn.BatchNorm1d(params['linear']['lin3_out'])

        # Pooling layers
        #class torch.nn.MaxPool2d(kernel_size, stride=None, padding=0, dilation=1, return_indices=False, ceil_mode=False)
        self.max2d = nn.MaxPool2d(kernel_size= 2)
        # class torch.nn.AvgPool2d(kernel_size, stride=None, padding=0, ceil_mode=False, count_include_pad=True)
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
        out = self.max2d(self.relu(self.batch1(self.conv1(x))))
        out = self.max2d(self.relu(self.batch2(self.conv2(out))))
        out = self.max2d(self.relu(self.batch3(self.conv3(out))))
        out = self.max2d(self.relu(self.batch4(self.conv4(out))))
        out = self.max2d(self.relu(self.batch5(self.conv5(out))))

        print(out.size())
        out = out.view(out.size(0), -1)
        # out = self.batch_lin_1(self.linear1(out))
        # out = self.batch_lin_2(self.linear2(out))
        # out = self.batch_lin_3(self.linear3(out))
        out = self.relu(self.linear1(out))
        out = self.relu(self.linear2(out))


        #remove one layer --> and train another model

        # out = self.relu(self.linear3(out))
        #out = self.softmax(out)
        
        return out

neural_net = ConvNet()





# use_gpu = torch.cuda.is_available()
# print("GPU Available: {}".format(use_gpu))
# if use_gpu:
#   # switch model to GPU
#   neural_net.cuda()

import torch.nn.functional as F

def cost_function(prediction, target):
    loss = F.cross_entropy(prediction, target)
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

        # compute the loss
        loss = cost_function(prediction, target)

        # compute the gradients 
        loss.backward()

        # update the parameters 
        optimizer.step()

        # accumulate the loss of each minibatch
        total_loss += loss.data[0]*len(data)

        # compute the accuracy per minibatch  
        pred_classes = prediction.data.max(1, keepdim=True)[1]
        correct += pred_classes.eq(target.data.view_as(pred_classes)).sum().double()

        t_end = time.time()

        print('Epoch {}, batch_id: {},  time : {}'.format(epoch, batch_idx,t_end - t_start))
        print('Acc: {:.5f} for batch {}'.format(pred_classes.eq(target.data.view_as(pred_classes)).sum().double(), batch_idx))

    tf = time.time()

    print('Epoch {}, time : {}'.format(epoch, tf - t0))

    # compute the mean loss for each epoch 
    mean_loss = total_loss/len(train_loader.dataset)
    
    # compute the accuracy for each epoch 
    acc = correct / len(train_loader.dataset)
        
    print('Train Epoch: {}   Avg_Loss: {:.5f}   Acc: {}/{} ({:.3f}%)'.format(
        epoch, mean_loss, correct, len(train_loader.dataset),
        100. * acc))   
    
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
        plot_thingy(prediction, target)
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

def load_model(epoch, model, path='/Users/li-tigre/Desktop/MR_AI/scripts/Models/neural_net/'):
    
    # file name and path 
    filename = path + 'neural_network_{}.pt'.format(epoch)
    
    # load the model parameters 
    model.load_state_dict(torch.load(filename))
    
    
    return model





# Number of epochs 
numEpochs = 1

# checkpoint frequency 
checkpoint_freq = 2

# path to save the data 
path = './'

# empty lists 
train_losses = []
val_losses = []
test_losses = []

train_accuracies = []
val_accuracies = []
test_accuracies = []

neural_net = load_model(4, neural_net)

#traininng 
# for epoch in range(1, numEpochs + 1):
    
#     # train() function (see above)
#     # train_loss, train_acc = train(epoch, neural_net, train_loader, optimizer)
    
#     # eval() functionn (see above)
#     # val_loss, val_acc = eval(neural_net, val_loader)    
#     # test_loss, test_acc = eval(neural_net, test_loader)    

    
#     # append lists for plotting and printing 
#     train_losses.append(train_loss)    
#     val_losses.append(val_loss)

    
#     train_accuracies.append(train_acc)    
#     val_accuracies.append(val_acc)
    
#     #Checkpoint
#     if epoch % checkpoint_freq ==0:
#         save_model(epoch, neural_net, path)

# Last checkpoint
# save_model(numEpochs, neural_net, path)
    
print("\n\n\nOptimization ended.\n")

test_loss, test_acc = eval(neural_net, test_loader)
# print(test_acc)




def resizeAndPad(img, size, padColor=0):

    h, w = img.shape[:2]
    sh, sw = size

    # interpolation method
    if h > sh or w > sw: # shrinking image
        interp = cv2.INTER_AREA
    else: # stretching image
        interp = cv2.INTER_CUBIC

    # aspect ratio of image
    aspect = w/h  # if on Python 2, you might need to cast as a float: float(w)/h

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


img_as_img = cv2.imread('/Users/li-tigre/Downloads/rip.jpg', 0)
print(img_as_img)
img_as_img = resizeAndPad(img_as_img, (256, 256), 0)
print(img_as_img.shape)
img_as_img = img_as_img[np.newaxis, ...]
img_as_img = img_as_img[np.newaxis, ...]
img_as_img = img_as_img/255
print(img_as_img.shape)

img_as_tensor = torch.tensor(img_as_img, dtype=torch.float)

out = neural_net(img_as_tensor)
print(out)

# x = list(range(len(train_accuracies)))

# ax = plt.subplot(111)
# plt.plot(x, train_accuracies, 'r', label="Train")
# plt.plot(x, val_accuracies, 'g', label="Validation")
# plt.title('Accuracy')
# leg = plt.legend(loc='best', ncol=2, mode="expand", shadow=False, fancybox=False)
# leg.get_frame().set_alpha(0.99)

# x = list(range(len(train_accuracies)))

# ax = plt.subplot(111)
# plt.plot(x, train_accuracies, 'r', label="Train")
# plt.plot(x, val_accuracies, 'g', label="Validation")
# plt.title('Accuracy')
# leg = plt.legend(loc='best', ncol=2, mode="expand", shadow=False, fancybox=False)
# leg.get_frame().set_alpha(0.99)
