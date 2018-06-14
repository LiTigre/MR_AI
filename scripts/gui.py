from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os, shutil
import numpy as np

class buildGUI(Frame):
    def __init__(self, typeNeuralNet, master = None):
        Frame.__init__(self, master)
        self.master = master
        self.typeNeuralNet = typeNeuralNet
        self.init_gui()
    
    
    def init_gui(self):
        self.master.title(self.typeNeuralNet)
        self.pack(fill=BOTH, expand=1)
        #Input
        inputLabel = Label(self, text="Input")
        inputLabel.grid(row=0, column=0)

        #Output
        outputLabel = Label(self, text="Output")
        outputLabel.grid(row=1, column=0)

        #Examples
        exampleLabel = Label(self, text="Examples")
        exampleLabel.grid(row=2, column=0)

        self.examples = Entry(self)
        self.examples.grid(row=2, column=1)

        if (self.typeNeuralNet == "Classification-CNN"):
            #Input Folder
            self.inputDir = filedialog.askdirectory()
            self.input = Label(self, text=self.inputDir)
            self.input.grid(row=0, column=1)

            #Output Folder
            self.outputDir = filedialog.askdirectory()
            self.output = Label(self, text=self.outputDir)
            self.output.grid(row=1, column=1)

        if (self.typeNeuralNet == "Denoising-CNN"):
            #Input File
            self.inputFile = filedialog.asksaveasfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
            self.input = Label(self, text=self.inputFile)
            self.input.grid(row=0, column=1)

            #Output Folder
            self.outputDir = filedialog.askdirectory()
            self.output = Label(self, text=self.outputDir)
            self.output.grid(row=1, column=1)

            #Option to display output
            self.display_output = ttk.Checkbutton(self, text="Display Output")
            self.display_output.grid(row=10, column = 0)


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

        list_input = [i for i in os.lisdir(inputFolder)]

        for i, proba in enumerate(modelOutputs):
            if proba < 0.5 :#random number
                copy2(list_input[i], outputFolder+ dir1)              
            elif proba > 0.5 :
                copy2(list_input[i], outputFolder+ dir2)
            else:
                copy2(slist_input[i], outputFolder+ dir3)


    def create_csv(self, inputs, outputs, true_values, rmse_vals=None):
        return
        

class buildMenu(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.master = master
        self.init_gui()

    def init_gui(self):
        self.master.title('MR-AI')
        self.pack(fill=BOTH, expand=1)

        #Neural net selection
        menuLabel = Label(self, text="Select a neural net")
        menuLabel.grid(row=0, column=0)

        menuOptions = ["Classification-CNN", "Denoising-CNN"]
        variable = StringVar(self.master)
        variable.set("               ")

        self.w = OptionMenu(self, variable, *menuOptions, command = self.selectNN)
        self.w.grid(row = 0, column = 1)

    def selectNN(self, value):

        root = Tk()
        app = buildGUI(value, root)
        root.mainloop()
        exit()


if __name__ == '__main__':
    root = Tk()
    app = buildMenu(root)
    root.mainloop()



    