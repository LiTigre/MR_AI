from tkinter import *
from tkinter import ttk

from PIL import Image, ImageTk

class ImageViewer():
    def __init__(self, master):

        self.master = master
        self.photos=[]
        self.load_images()

        self.image_num=0

        ## click photo on button to change image
        self.btn = Button(self.master, image=self.photos[self.image_num], command=self.next_image)
        #self.btn.grid(row=2)
        self.btn2 =Button(self.master, text="Exit", bg="orange", command=self.master.quit)
        #self.btn2.grid(row=1)


    def next_image(self):
        self.image_num += 1
        if self.image_num >= len(self.photos):
            self.image_num=0

        ## pipe the next image to be displayed to the button
        self.btn["image"]=self.photos[self.image_num]

    def load_images(self):
        """ copy data images to a list that is an instance variable"""

        ## put the images in an instance object (self.) so they aren't destroyed
        ## when the function exits and can be used anywhere in the class

        image = Image.open("test.jpg")
        # We need to keep a reference to the image!

        
        self.photos.append(ImageTk.PhotoImage(image))

  
  
#root=Tk()
#CI=imageViewer(root)
#root.mainloop()