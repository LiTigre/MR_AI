from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import Progressbar

import threading
import time
import os, shutil, webbrowser
import numpy as np

import backend
import imageViewer


class buildGUI(Frame):
    def __init__(self, typeNeuralNet, master = None):
        Frame.__init__(self, master)
        self.master = master
        self.typeNeuralNet = typeNeuralNet
        self.init_gui()
    
    def init_gui(self):
        self.master.title(self.typeNeuralNet)
        self.pack(fill=BOTH, expand=1)

        #Tabs
        self.tabControl = ttk.Notebook(self.master)
        self.mainTab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.mainTab, text='Main')
        self.tabControl.pack(expand=1, fill='both')
        if (self.typeNeuralNet == "Classification-CNN"):
            self.advancedOptionsTab(self.tabControl)

            #Input
            inputLabel = Label(self.mainTab, text="Input Folder")
            inputLabel.grid(row=0, column=0)

            #Output
            outputLabel = Label(self.mainTab, text="Output Folder")
            outputLabel.grid(row=1, column=0)

            #Backend
            self.process = backend.Backend(self.typeNeuralNet)

            #Progress bar
            self.progress = Progressbar(self.mainTab, orient=HORIZONTAL,length=500,  mode='indeterminate')

            #Input Folder
            self.inputDir = filedialog.askdirectory(title = "Select input directory")
            self.input = Label(self.mainTab, text=self.inputDir)
            self.input.grid(row=0, column=1)

            #Output Folder
            self.outputDir = filedialog.askdirectory(title = "Select output directory")
            self.output = Label(self.mainTab, text=self.outputDir)
            self.output.grid(row=1, column=1)
            

            # Start 
            self.startButton = Button(self.mainTab, text="Start", command=self.run )
            self.startButton.grid(row=3, column=0)

        if (self.typeNeuralNet == "Self-classification"):

            # TODO: counter
            # TODO: disable button once counter at 0


            # TODO: Image viewer
            self.imageViewer = imageViewer.ImageViewer(self.mainTab)
            self.imageViewer.btn.grid(row = 1)

            # TODO: Buttons
            self.blurryButton = Button(self.mainTab, text="Blurry", command= self.mainTab.quit )
            self.blurryButton.grid(row=5, column=0)

            self.notBlurryButton = Button(self.mainTab, text="Not Blurry", command=self.mainTab.quit )
            self.notBlurryButton.grid(row=5, column=1)

            # TODO: Dynamic display

            


    
    def run(self):
        def runInner():
            self.progress.grid(row=5,column=0)
            self.progress.start()
            (good, uncertain, bad ) = self.process.runModel(self.progress)
            if messagebox.askyesno('Process completed!',  'There are : \n-' +
                                        good + " good scans \n-" +
                                        bad  + " bad scans \n-" +
                                        uncertain + " uncertain scans \n\n" +
                                        "Do you want to go to the output directory?", icon = messagebox.INFO):
                                            webbrowser.open(self.outputDir)                     
            self.progress.grid_forget()
            

        threading.Thread(target=runInner).start() 

    def advancedOptionsTab(self, tabControl):

        self.advancedOptionsTab = ttk.Frame(tabControl)
        tabControl.add(self.advancedOptionsTab,text="Advanced Options")
        tabControl.pack(expand=1, fill='both')
        percentageLabel = Label(self.advancedOptionsTab, text="Percentage accuracy")
        percentageLabel.grid(row=0, column=0)
        self.percentage = Entry(self.advancedOptionsTab)
        self.percentage.grid(row=0, column=1)
        

class buildMenu(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.master = master
        self.init_gui()

    def init_gui(self):
        self.master.title('MR-AI')
        self.pack(fill=BOTH, expand=1)

        #Neural net selection
        menuLabel = Label(self, text="Select a mode")
        menuLabel.grid(row=0, column=0)

        menuOptions = ["Classification-CNN", "Self-classification"]
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



    