from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import Progressbar
import threading
import time
import os, shutil
import numpy as np

class backend:
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
        inputLabel = Label(self, text="Input Folder")
        inputLabel.grid(row=0, column=0)

        #Output
        outputLabel = Label(self, text="Output Folder")
        outputLabel.grid(row=1, column=0)

        #Backend
        self.process = backend(self.typeNeuralNet)

        #Progress bar
        self.progress = Progressbar(self, orient=HORIZONTAL,length=500,  mode='indeterminate')
        
        if (self.typeNeuralNet == "Classification-CNN"):
            #Input Folder
            self.inputDir = filedialog.askdirectory(title = "Select input directory")
            self.input = Label(self, text=self.inputDir)
            self.input.grid(row=0, column=1)

            #Output Folder
            self.outputDir = filedialog.askdirectory(title = "Select output directory")
            self.output = Label(self, text=self.outputDir)
            self.output.grid(row=1, column=1)
            
            # Percentage
            #percentageLabel = Label(self, text="Percentage accuracy")
            #percentageLabel.grid(row=2, column=0)
            #self.percentage = Entry(self)
            #self.percentage.grid(row=2, column=1)

            # Start 
            self.startButton = Button(self, text="Start", command=self.run )
            self.startButton.grid(row=3, column=0)

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
            self.display_output.grid(row=2, column = 0)

            self.start = Button(self, text="Start", command=self.run)
            self.start.grid(row=3, column=1)
    
    def run(self):
        def runInner():
            self.progress.grid(row=5,column=0)
            self.progress.start()
            (good, uncertain, bad ) = self.process.runModel(self.progress)
            messagebox.showinfo('Info', 'Process completed! \nThere are : \n-' +
                                        good + " good scans \n-" +
                                        bad  + " bad scans \n-" +
                                        uncertain + " uncertain scans \n")
            self.progress.grid_forget()
            self.ask_to_see_user()
            

        threading.Thread(target=runInner).start() 

        
    def ask_to_see_user(self):
        question = Tk()
        question.title("Option to see output")
        question.questionLabel = Label(question, text="Do you want to go to the output folder")
        question.questionLabel.pack()#grid(row=0, column =0)
        v = IntVar()
        for i, option in enumerate(["yes", "no"]):
            question.optionButton = Radiobutton(question, text=option, variable=v, value=i)
            question.optionButton.pack()#.grid(row=i+1, column =0)
        question.submitButton = Button(text="Submit", command=question.destroy)
        question.submitButton.pack()#.grid(row=3, column =0)
        question.mainloop()
        if v.get() == 0: 
            return None
        else:
            print("yes")

# TODO: borders, option in messagebox, more advanced options

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

        self.menu = OptionMenu(self, variable, *menuOptions, command = self.selectNN)
        self.menu.grid(row = 0, column = 1)

    def selectNN(self, value):

        root = Tk()
        app = buildGUI(value, root)
        root.mainloop()
        exit()


if __name__ == '__main__':
    root = Tk()
    app = buildMenu(root)
    root.mainloop()



    