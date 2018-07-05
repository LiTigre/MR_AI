# MR_AI
## Context/ Problem
Small movements during an MRI scan can lead to motion artefacts ie distortions in the final images. In a clinical setting, these distortions are usually found much later and require another scan from the patient. Meanwhile, for brain researchers, going through all the raw acuisitions to find usuable data is time-consuming as well. Hence, the lack of automated noise detection algorithm for MRIs leads to unnecessary expenditure in time and money. 

## Solution
We implemented a classifier that detects motion artefacts in MRIs using a deep learning. A convolutional neural network with five fully connected layers were used, as well as three linear layers. In the context of our project, we have also decided to create a prototype of a desktop application with user interface to demo our project.

## Dataset creation
From the public IXI dataset, we obtained 576 T2 brain volumes from healthy subjects taken with 3T or 1.5T scanners. The dataset was split into train (360 brain volumes), validation (109 brain volumes) and test sets (109 brain volumes) on the patient level and we systematically introduce noise by combining the orginal slice and a rigidly transformed slice in the same 3D volume. We proceeded to extract 50 central axial slices from each slice and systemically introduced random noise to the slices.

## Architecture of the model
We are using a convolutional neural network with five fully connected layers. For each layers, we used kernel size of 5 with stride of 1. We then also applied batch normalization, tanh activation function, and finally maxpoll with a 2 by 2 kernel.

## User interface
Using the built-in Python GUI ie TKinter, we implemented a desktop application that asks the user for an input folder with brain slices ie MRI pictures and for an output folder. There is also an advanced option tabs with includes an option to change the threshold output probability for the neural net. To start the classification process, the users presses on the "start" button. The integrated neural net proceeds to separate the slices into 3 categories: "good" scans ie no motion artefacts, "bad" scans i.e. with motion artefacts and "uncertain" scans for the scans associated with lower probability values than the threshold probability.
![Alt Text](https://media.giphy.com/media/MVge7VhZAZ2MORlvsW/giphy.gif)

## Future directions
We hope to integrate our project into the MRI scanner such that it will be able to immediately detect a blurry image and perform another scan right away. We would also like to modify our project such that different research labs are able to train their own model with their own data to help with their progress.
