#holds a series of images to be used by the interlacer to create interlaced images.
#contains the methods to generate multiple images using a user-provided depth map.

#from tkinter import Tk
from tkinter.filedialog import askopenfilenames, askopenfilename
from PIL import Image

class ImageCollection:
    def __init__(self):
        self.collection = []
    
    #uses the operating system to add multiple images at once
    def add_mult_images(self):
        pass
    
    #uses the operating system to add a single image
    def add_sing_image(self):
        pass