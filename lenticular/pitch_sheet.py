from PIL import Image, ImageDraw, ImageFont
import numpy as np
import math
from os import path

#TODO
#generate pitch segment labels
#generate page header

class PitchSheet:
    #low_pitch and high_pitch are the lower and upper bounds, and use LPI as units
    #page_dimensions uses inches as units (potentially reconfigurable to millimeters for ISO 216)
    #page_dpi is the dots per inch of the printer intended to be used. passed as a tuple for printers with non-square max dpi
    #page_resolution represents width and height of the dpi of the printer in use #???
    def __init__(self, low_pitch:float, high_pitch:float, page_dimensions:tuple, page_dpi:tuple):
        self.low_pitch = low_pitch
        self.high_pitch = high_pitch
        self.page_dimensions = page_dimensions
        self.page_dpi = page_dpi
        self.page_resolution = tuple(int(ele1 * ele2) for ele1, ele2 in zip(self.page_dimensions, self.page_dpi)) #???
    
    #generates one segment of the pitch sheet
    #size_in is a tuple providing the dimensions of the segment in inches
    #size_px is a tuple providing the dimensions in pixels
    def _generate_pitch_segment(self, size_in, size_px, lpi):
        ppl = self.page_dpi[0] / lpi #pixels per lenticule
        
        #generates a new image where a prerendered version of the segment is created
        #this is so that the lines can be drawn on exact pixel coordinates, then the image can be resized to the correct area
        lines = math.ceil(size_in[0] * lpi) #number of lines in this segment
        line_spacing = math.ceil(ppl)
        pre_seg_res = (line_spacing * lines, int(size_px[1]))
        seg = Image.new(mode = "RGB", size = pre_seg_res, color = (255, 255, 255))
        seg_draw = ImageDraw.Draw(seg)
        #this loop fills pre_seg image with lines
        for j in range(0, pre_seg_res[0], line_spacing):
            seg_draw.line([j, 0, j, pre_seg_res[1]], fill = (0, 0, 0), width = 1)
        #resize by ppl/line_spacing
        correction_res = (int(pre_seg_res[0] * (ppl/line_spacing)), int(size_px[1]))
        seg = seg.resize(correction_res, resample = Image.BICUBIC)
        seg = seg.crop((int(correction_res[0] - size_px[0]), 0, size_px[0] - (correction_res[0] - size_px[0]), size_px[1]))
        
        return seg
    
    #this function generates the image of the text labels showing the lpi of each pitch segment
    #fnt_path is an OS path (as in 'from os import path') to a truetype font to be used
    #fnt_size is a float representing the size of the font relative to the vertical size of the image generated, where 0.0 is infinitely small, and 1.0 fills the image vertically
    #size_in is a tuple providing the dimensions of the segment label in inches
    #size_px is a tuple providing the dimensions in pixels
    #lpi is the number that the function will render and place next to the segment
    #text renders aligned left, vertically centered in the box
    def _generate_segment_label(self, fnt_path, fnt_size, size_in, size_px, lpi):
        fnt_vert = size_px[1]/4.0 + fnt_size/2.0 #vertical offset of text
        fnt = ImageFont.truetype(fnt_path, int(size_px[1] * fnt_size)) #font for pitch segment labels
        lab = Image.new(mode = "RGB", size = (int(size_px[0]), int(size_px[1])), color = (255, 255, 255))
        lab_draw = ImageDraw.Draw(lab)
        lab_draw.text((0,fnt_vert), "{:0.2f}".format(lpi), font = fnt, fill=(0,0,0))
        return lab
    
    #this function generates the image of the text header at the top of the pitch sheet page
    def _generate_header_text(self):
        pass
    
    #this function generates the image for the printable pitch sheet and saves it to the specified directory
    #segments represents how many rows of pitch tests will print on the page
    #separation is the ratio of pitch test to gap between tests. values range from 0.0 (no white space) to 1.0 (only white space)
    #margins represents how much white space will be left on the outside of the page in inches. The tuple represents the space from the top, right, bottom, and left, respectively)
    #header is the space given to the information header in inches
    #num_width is the width of the segment labels in inches
    def generate_pitch_sheet(self, directory:str = "./pitch_sheet.png", segments:int = 11, separation:float = 0.2, margins:tuple = (0.25, 0.25, 0.25, 0.25), header_height:float = 1.0, num_width = 0.75):
        bg = Image.new(mode = "RGB", size = self.page_resolution, color = (255, 255, 255))
        available_horiz = self.page_dimensions[0] - margins[1] - margins[3] - num_width
        available_vert = self.page_dimensions[1] - margins[0] - margins[2] - header_height
        available_space = (available_horiz, available_vert)
        
        #loop generates the images for each pitch segment and their according lpi labels
        #and pastes it onto the original image.
        for i in range(segments):
            #segment positions in inches
            seg_horiz_pos = margins[3] + num_width
            seg_vert_pos = margins[0] + header_height + (i * (available_space[1] / segments))
            seg_pos = (seg_horiz_pos, seg_vert_pos)
            
            #label positions in inches
            lab_horiz_pos = margins[3]
            lab_vert_pos = margins[0] + header_height + (i * (available_space[1] / segments))
            lab_pos = (lab_horiz_pos, lab_vert_pos)
            
            #segment positions in pixels
            seg_horiz_pos_px = seg_pos[0] * self.page_dpi[0]
            seg_vert_pos_px = seg_pos[1] * self.page_dpi[1]
            seg_pos_px = (seg_horiz_pos_px, seg_vert_pos_px)
            
            #label positions in pixels
            lab_horiz_pos_px = lab_pos[0] * self.page_dpi[0]
            lab_vert_pos_px = lab_pos[1] * self.page_dpi[1]
            lab_pos_px = (lab_horiz_pos_px, lab_vert_pos_px)
            
            #segment dimensions in inches
            seg_horiz_space = available_space[0]
            seg_vert_space = (available_space[1] / segments) * (1.0 - separation)
            seg_space = (seg_horiz_space, seg_vert_space)
            
            #label dimensions in inches
            lab_horiz_space = num_width
            lab_vert_space =  seg_vert_space
            lab_space = (lab_horiz_space, lab_vert_space)
            
            #segment dimensions in pixels
            seg_horiz_space_px = seg_space[0] * self.page_dpi[0]
            seg_vert_space_px = seg_space[1] * self.page_dpi[1]
            seg_space_px = (seg_horiz_space_px, seg_vert_space_px)
            
            #label dimensions in pixels
            lab_horiz_space_px = lab_space[0] * self.page_dpi[0]
            lab_vert_space_px = lab_space[1] * self.page_dpi[1]
            lab_space_px = (lab_horiz_space_px, lab_vert_space_px)
            
            xp = [0, segments - 1]
            fp = [self.low_pitch, self.high_pitch]
            lpi = np.interp(i, xp, fp)
            
            seg = self._generate_pitch_segment(seg_space, seg_space_px, lpi)
            bg.paste(seg, (int(seg_pos_px[0]), int(seg_pos_px[1])))
            
            fnt_path = path.join(path.dirname(path.dirname(__file__)), "fonts/Roboto/Roboto-Regular.ttf")
            #lab_fnt = ImageFont.truetype("../fonts/Roboto/Roboto-Regular.ttf", int(lab_space_px[1])) #font for pitch segment labels
            lab = self._generate_segment_label(fnt_path, 0.35, lab_space, lab_space_px, lpi)
            bg.paste(lab, (int(lab_pos_px[0]), int(lab_pos_px[1])))
            
            draw = ImageDraw.Draw(bg)
            draw.rectangle([seg_pos_px[0], seg_pos_px[1], seg_pos_px[0] + seg.size[0], seg_pos_px[1] + seg.size[1]], outline = (0, 0, 0), width = 2)
        
        bg.save(directory)