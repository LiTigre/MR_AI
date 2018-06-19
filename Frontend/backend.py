import threading
import time
import os, shutil, webbrowser
import numpy as np


class Backend:
    def __init__(self, typeNeuralNet):
        self.typeNeuralNet = typeNeuralNet
        self.finished = False

    def runModel(self, progressBar):
        time.sleep(5)
        progressBar.stop()
        self.finished = True
        print("Done")
        good = "13"
        uncertain = "4"
        bad = "1996"
        output = (good, uncertain, bad )
        return output
    
    def preprocessing(self, inputFile):
        return
        #TODO


    def loadModel(self, weights):
        return

        # TODO
        # if (self.typeNeuralNet == "Classification-CNN"):
            # neural_net = ConvNet()
            # neural_net.load_state_dict(torch.load(filename))
        # if (self.typeNeuralNet == "Denoising-CNN"):


    def useModel(self, model):
        return
        # TODO
        #dataset = CustomDatasetFromImages("drive/S_and_T_images/Test/Test/test_names.csv", "drive/S_and_T_images/Test/Test/")
        #val_loader = torch.utils.data.DataLoader(my_dataset_val, batch_size = 100, shuffle=True)

    
    def move_files(self, modelOutputs, inputFolder, outputFolder):
        dir1 = "/good"
        dir2 = "/bad"
        dir3 = "/unsure"
        os.makedirs(os.path.join(outputFolder, dir1))
        os.makedirs(os.path.join(outputFolder, dir2))
        os.makedirs(os.path.join(outputFolder, dir3))

        list_input = [i for i in os.listdir(inputFolder)]

        for i, proba in enumerate(modelOutputs):
            if proba < 0.5 :#random number
                shutil.copy(list_input[i], outputFolder+ dir1)              
            elif proba > 0.5 :
                shutil.copy(list_input[i], outputFolder+ dir2)
            else:
                shutil.copy(list_input[i], outputFolder+ dir3)


    def create_csv(self, inputs, outputs, true_values, rmse_vals=None):
        return