import os
import time
import platform
import io

import matplotlib.pyplot as plt
from matplotlib.pyplot import cm

import pandas as pd
from skimage import io, transform
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils

import torchvision.datasets as data

import torchvision.transforms as transforms

import random

from PIL import Image
import cv2

import tensorflow as tf
from scipy import signal as signal


#import the dataloader class

#import the dictionary with the parameters

#import the conv_deconv v1

#import cost function for MSE cost

#import save and load



def register_extension(id, extension): Image.EXTENSION[extension.lower()] = id.upper()
Image.register_extension = register_extension

def register_extensions(id, extensions): 
    for extension in extensions: register_extension(id, extension)
Image.register_extensions = register_extensions


#DATASETS

#my_dataset_test = CustomDatasetFromImages("/content/data/train/train_names.csv", "train")

# my_dataset_val = CustomDatasetFromImages("/Users/li-tigre/Downloads/reconstruction_val_names.csv", "/Users/li-tigre/Downloads/Validation")

my_dataset_train = CustomDatasetFromImages("/Users/li-tigre/Downloads/reconstruction_val_names.csv", "/Users/li-tigre/Downloads/Validation")




#BATCH SIZE & DATA LOADERS

batch_size = 5

train_loader = torch.utils.data.DataLoader(my_dataset_train, batch_size, shuffle=True)

# test_loader = torch.utils.data.DataLoader(my_dataset_test, batch_size, shuffle=True)

# val_loader = torch.utils.data.DataLoader(my_dataset_val, batch_size, shuffle=True)





neural_net = ConvNet()

# use_gpu = torch.cuda.is_available()
# print("GPU Available: {}".format(use_gpu))
# if use_gpu:
#   # switch model to GPU
#   neural_net.cuda()


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

        plt.imshow(prediction[0][0].data.numpy())

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

