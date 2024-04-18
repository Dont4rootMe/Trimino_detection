from PyQt6.QtGui import QPixmap
from PIL import Image, ImageEnhance, ImageQt

from PIL import Image, ImageEnhance, ImageQt
import numpy as np
import cv2 as cv

class Engine:
    def __refresher__(func):
        def inner(self, *args, **kwargs):
            func(self, *args, **kwargs)
            self.refresh()
        return inner

    def __whipe_dict(self):
        self.actions = {
            'brightness': False,
            'contrast': False,
            'sharpness': False,
            'saturation': False,
            'color_enhancements': [1.0, 1.0, 1.0],
            'erosion': None,
            'dilation': None,
            'opening': None,
            'closing': None,
        }

    def __init__(self):
        self.img = None
        self.modified = None

        self.refresh_actions = []
        self.reset_actions = []

        self.__whipe_dict()

    def refresh(self):
        for act in self.refresh_actions:
            act()
    
    def reset(self):
        for act in self.reset_actions:
            act()
        
        self.__whipe_dict()

    def add_refresh_action(self, action):
        self.refresh_actions.append(action)

    def add_reset_action(self, action):
        self.reset_actions.append(action)

    def upload_picture(self, path):
        self.img = Image.open(path).copy()
        self.modified = Image.open(path).copy()
        self.reset()

    def original_pixmap_exist(self):
        return self.img is not None
    
    def modified_pixmap_exist(self):
        return self.modified is not None

    def get_original_pixmap(self):
        temp = self.img
        return QPixmap.fromImage(ImageQt.ImageQt(temp).copy())
    
    def get_modified_pixmap(self):
        temp = self.img
        if self.actions['brightness']:
            enhancer = ImageEnhance.Brightness(temp)
            temp = enhancer.enhance(self.actions['brightness'])
        if self.actions['contrast']:
            enhancer = ImageEnhance.Contrast(temp)
            temp = enhancer.enhance(self.actions['contrast'])
        if self.actions['sharpness']:
            enhancer = ImageEnhance.Sharpness(temp)
            temp = enhancer.enhance(self.actions['sharpness'])
        if self.actions['saturation']:
            enhancer = ImageEnhance.Color(temp)
            temp = enhancer.enhance(self.actions['saturation'])

        Matrix = np.array(temp).astype(float)
        Matrix[..., 0] *= self.actions['color_enhancements'][0]
        Matrix[..., 1] *= self.actions['color_enhancements'][1]
        Matrix[..., 2] *= self.actions['color_enhancements'][2]
        temp = Image.fromarray(Matrix.astype(np.uint8))

        if self.actions['erosion'] is not None:
            Matrix = np.array(temp).astype(float)
            temp = cv.erode(Matrix, self.actions['erosion'], iterations=1)
            temp = Image.fromarray(temp.astype(np.uint8))

        if self.actions['dilation'] is not None:
            Matrix = np.array(temp).astype(float)
            temp = cv.dilate(Matrix, self.actions['dilation'], iterations=1)
            temp = Image.fromarray(temp.astype(np.uint8))

        if self.actions['opening'] is not None:
            Matrix = np.array(temp).astype(float)
            temp = cv.morphologyEx(
                Matrix, cv.MORPH_OPEN, self.actions['opening'])
            temp = Image.fromarray(temp.astype(np.uint8))

        if self.actions['closing'] is not None:
            Matrix = np.array(temp).astype(float)
            temp = cv.morphologyEx(
                Matrix, cv.MORPH_CLOSE, self.actions['closing'])
            temp = Image.fromarray(temp.astype(np.uint8))

        self.modified = QPixmap.fromImage(ImageQt.ImageQt(temp).copy())
        return self.modified
    

    @__refresher__
    def change_brightness(self, brightness):
        k = (brightness - 127) / 128 + 1.0
        self.actions['brightness'] = k

    @__refresher__
    def change_contrast(self, contrast):
        k = (contrast - 127) / 128 + 1.0
        self.actions['contrast'] = k

    @__refresher__
    def change_sharpness(self, sharpness):
        k = ((sharpness - 127) / 128) * 8 + 1.0
        self.actions['sharpness'] = k

    @__refresher__
    def change_saturation(self, saturation):
        k = ((saturation - 127) / 128) + 1.0
        self.actions['saturation'] = k

    @__refresher__
    def enhance_red(self, red):
        k = (red - 300) / 300 + 1.0
        self.actions['color_enhancements'][0] = k

    @__refresher__
    def enhance_green(self, green):
        k = (green - 300) / 300 + 1.0
        self.actions['color_enhancements'][1] = k

    @__refresher__
    def enhance_blue(self, blue):
        k = (blue - 300) / 300 + 1.0
        self.actions['color_enhancements'][2] = k

    @__refresher__
    def erosion_change(self, erosion):
        if erosion == 0:
            self.actions['erosion'] = None
            return
        kernel = np.ones(erosion, np.uint8)
        self.actions['erosion'] = kernel

    @__refresher__
    def dilation_change(self, dilation):
        if dilation == 0:
            self.actions['dilation'] = None
            return
        kernel = np.ones(dilation, np.uint8)
        self.actions['dilation'] = kernel

    @__refresher__
    def opening_change(self, opening):
        if opening == 0:
            self.actions['opening'] = None
            return
        kernel = np.ones(opening, np.uint8)
        self.actions['opening'] = kernel

    @__refresher__
    def closing_change(self, closing):
        if closing == 0:
            self.actions['closing'] = None
            return
        kernel = np.ones(closing, np.uint8)
        self.actions['closing'] = kernel