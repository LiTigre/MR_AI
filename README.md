# MR_AI
## Context/ Problem
Small movements during an MRI scan can lead to motion artefacts ie distortions in the final images. In a clinical setting, these distortions are usually found much later and require another scan from the patient. In other words, the lack of automated noise detection algorithm for MRIs leads to unnecessary expenditure in time and money. We have therefore implemented a classifier that detects motion artefacts in MRIs
## Dataset creation
From the public IXI dataset, we obtained 576 T2 brain volumes. We proceeded to extract 50 central axial slices from each slice and systemically introduced random noise to the slices. 

## Deep convolutional neural network
We implemented a neural network with 5 convolutional layers and 3 fully connected layers. Batch normalization was done in each layer.

## User interface
Using the built-in Python GUI ie TKinter, we implemented a desktop application that asks the user for an input folder with brain slices ie MRI pictures and for an output folder. There is also an advanced option tabs with includes an option to change the threshold output probability for the neural net. To start the classification process, the users presses on the "start" button. The integrated neural net proceeds to separate the slices into 3 categories: "good" scans ie no motion artefacts, "bad" scans ie with motion artefacts and "uncertain" scans for the scans associated with lower probability values than the threshold probability

## Future directions
