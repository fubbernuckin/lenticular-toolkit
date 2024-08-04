#haven't decided how I want to do things here

#broadly:
#function to generate interlaced image from multiple input images
#function to generate multiple input images from starting image and bump map

from PIL import Image, ImageDraw

from image_collection import ImageCollection

class Interlacer:
    def __init__(self, page_dimensions:tuple, lpi:float):
        pass
    
    #generates one interlaced image using the images from an image collection
    def interlace_from_collection(self, images:ImageCollection):
        pass