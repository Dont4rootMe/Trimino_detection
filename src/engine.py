from PyQt6.QtGui import QPixmap
from PIL import Image, ImageEnhance, ImageQt

from PIL import Image, ImageEnhance, ImageQt
import numpy as np
import cv2 as cv

def get_center(contour):
    moments = cv.moments(contour)
    if moments['m00'] != 0.0:
        x = int(moments['m10']/moments['m00'])
        y = int(moments['m01']/moments['m00'])
        return (x, y)


class Engine:
    def __refresher__(clear_contours=True):
        def __decorator__(func):
            def inner(self, *args, **kwargs):
                if clear_contours:
                    self.contours_detected = None
                    self.triangle_contours = None
                    self.convexes = None

                func(self, *args, **kwargs)
                self.refresh()
            return inner
        
        return __decorator__

    def __whipe_dict(self):
        self.actions = {
            'brightness': False,
            'contrast': False,
            'sharpness': False,
            'saturation': False,
            'color_enhancements': [1.0, 1.0, 1.0],
            'binarize': 128,
            'invert_binarize': False,
            'canny': False,
            'sobolev': {3: False, 5: False, 7: False},
            'erosion': None,
            'dilation': None,
            'opening': None,
            'closing': None,
            'min_dist': 1,
            'param_dots_bin': 30,
            'curv_ind': 2.0
        }

        self.min_contour_len = 500
        self.contours_detected = None
        self.triangle_contours = None
        self.convexes = None

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
        def __get_point_count(convex, domain, center):
            mask = (cv.fillPoly(np.zeros_like(self.img), [convex], 1) > 0)#[:, :, 0]
            working_dom = domain.copy() 
            mask = mask[:, :, 0]
            working_dom[~mask] = 0

            working_dom[mask] -= working_dom[center[1], center[0]]
            working_smoothed = np.linalg.norm(working_dom, axis=-1).astype(np.uint8)
            _, working_smoothed = cv.threshold(working_smoothed, self.actions['param_dots_bin'], 100, cv.THRESH_BINARY)
            working_smoothed = cv.GaussianBlur(working_smoothed, (5,5), 1)

            contours, hierarchy = cv.findContours(working_smoothed, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
            curv_indx = []
            for cnt in contours:
                area = cv.contourArea(cnt)
                perimeter = cv.arcLength(cnt, closed=True)
                if area > 1e-5 and perimeter > 1e-5:
                    curv_indx.append(abs(perimeter**2 / area - 4 * np.pi))
            
            return sum(map(lambda x: x <= self.actions['curv_ind'], curv_indx))
        
        temp = self.img
        z = np.zeros_like(temp)[:, :, 0]
        if self.triangle_contours is not None:
            temp = np.array(temp).astype(np.uint8)
            temp = cv.drawContours(temp, self.triangle_contours, -1, (255, 0, 0), 2)

            for cnt, (convex1, convex2, convex3) in zip(self.triangle_contours, self.convexes):
                domain = np.array(self.img).copy().astype(np.int16)
                center = get_center(cnt)
                counts = []
                for conv in [convex1, convex2, convex3]:
                    counts.append(str(__get_point_count(conv, domain, center)))
                    # z += k
                    # counts.append(str(c_len))
                    # z = cv.drawContours(z.astype(np.uint8), contours, -1, 255, 2)
                    # for c in circles:
                    #     z = cv.circle(z.astype(np.uint8), (int(c[0]), int(c[1])), int(c[2]), 255, 3)

                    # k = __get_point_count(conv, domain, center)


                x, y = get_center(cnt)
                temp = cv.putText(temp, f'{x=}, {y=}', (x, y), cv.FONT_HERSHEY_SIMPLEX,  
                    0.4, (255, 255, 255), 1, cv.LINE_AA) 
                temp = cv.putText(temp, f'{", ".join(sorted(counts))}', (x, y+12), cv.FONT_HERSHEY_SIMPLEX,  
                    0.4, (255, 255, 255), 1, cv.LINE_AA) 

            

            temp = Image.fromarray(temp.astype(np.uint8))
            # temp = Image.fromarray(z.astype(np.uint8))
            # from matplotlib import pyplot as plt
            # plt.imshow(temp)
            # plt.show()

        return QPixmap.fromImage(ImageQt.ImageQt(temp).copy())
    
    def get_modified_pixmap(self):
        temp = self.img

        # apply pixel-wise operations
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

        # apply color enhancements methods
        Matrix = np.array(temp).astype(float)
        Matrix[..., 0] *= self.actions['color_enhancements'][0]
        Matrix[..., 1] *= self.actions['color_enhancements'][1]
        Matrix[..., 2] *= self.actions['color_enhancements'][2]
        temp = Image.fromarray(Matrix.astype(np.uint8))

        # binariaze and invert binarization
        Matrix = np.array(temp).astype(np.float32)
        Matrix = cv.cvtColor(Matrix, cv.COLOR_BGR2GRAY)
        ret, temp = cv.threshold(
            Matrix, self.actions['binarize'], 255, cv.THRESH_BINARY)
        # if it is neccessery invert colors
        if self.actions['invert_binarize']:
            temp = 255 - temp
        temp = Image.fromarray(temp.astype(np.uint8))

        # adding Canny filters
        temp = np.array(temp).astype(np.uint8)
        if self.actions['canny']:
            temp = cv.Canny(temp, 100, 200)
        temp = Image.fromarray(temp.astype(np.uint8))

        # adding Sobolev filters
        temp = np.array(temp).astype(float)
        sobolev_sum = np.zeros_like(temp)
        sobolev_is_used = False
        for key, state in self.actions['sobolev'].items():
            if state:
                dx = cv.convertScaleAbs(cv.Sobel(temp, -1, 1, 0, ksize=key, borderType=cv.BORDER_DEFAULT))
                dy = cv.convertScaleAbs(cv.Sobel(temp, -1, 0, 1, ksize=key, borderType=cv.BORDER_DEFAULT))
                sobolev_sum += dx + dy
                sobolev_is_used = True
        temp = sobolev_sum if sobolev_is_used else temp
        temp = Image.fromarray(temp.astype(np.uint8))

        # applying porphological operations
        if self.actions['dilation'] is not None:
            Matrix = np.array(temp).astype(float)
            temp = cv.dilate(Matrix, self.actions['dilation'], iterations=1)
            temp = Image.fromarray(temp.astype(np.uint8))

        if self.actions['closing'] is not None:
            Matrix = np.array(temp).astype(float)
            temp = cv.morphologyEx(
                Matrix, cv.MORPH_CLOSE, self.actions['closing'])
            temp = Image.fromarray(temp.astype(np.uint8))

        if self.actions['erosion'] is not None:
            Matrix = np.array(temp).astype(float)
            temp = cv.erode(Matrix, self.actions['erosion'], iterations=1)
            temp = Image.fromarray(temp.astype(np.uint8))

        if self.actions['opening'] is not None:
            Matrix = np.array(temp).astype(float)
            temp = cv.morphologyEx(
                Matrix, cv.MORPH_OPEN, self.actions['opening'])
            temp = Image.fromarray(temp.astype(np.uint8))

        if self.contours_detected is not None:
            temp = np.array(temp).astype(float)
            under_lengthed_contours = [cnt for cnt, area in zip(*self.contours_detected) if area <= self.min_contour_len]
            if under_lengthed_contours:
                mask = np.zeros_like(temp).astype(np.int8)
                mask = cv.drawContours(mask, under_lengthed_contours, -1, (255), -1)
                temp -= 1.5 * mask
            temp = Image.fromarray(temp.astype(np.uint8))

        self.modified = temp.copy()
        return QPixmap.fromImage(ImageQt.ImageQt(temp).copy())


    @__refresher__(True)
    def change_brightness(self, brightness):
        k = (brightness - 127) / 128 + 1.0
        self.actions['brightness'] = k

    @__refresher__(True)
    def change_contrast(self, contrast):
        k = (contrast - 127) / 128 + 1.0
        self.actions['contrast'] = k

    @__refresher__(True)
    def change_sharpness(self, sharpness):
        k = ((sharpness - 127) / 128) * 8 + 1.0
        self.actions['sharpness'] = k

    @__refresher__(True)
    def change_saturation(self, saturation):
        k = ((saturation - 127) / 128) + 1.0
        self.actions['saturation'] = k

    @__refresher__(True)
    def enhance_red(self, red):
        k = (red - 300) / 300 + 1.0
        self.actions['color_enhancements'][0] = k

    @__refresher__(True)
    def enhance_green(self, green):
        k = (green - 300) / 300 + 1.0
        self.actions['color_enhancements'][1] = k

    @__refresher__(True)
    def enhance_blue(self, blue):
        k = (blue - 300) / 300 + 1.0
        self.actions['color_enhancements'][2] = k

    @__refresher__(True)
    def binarize(self, bin):
        self.actions['binarize'] = bin

    @__refresher__(True)
    def invert_binarize(self, val):
        self.actions['invert_binarize'] = val

    @__refresher__(True)
    def use_canny_filter(self, val):
        self.actions['canny'] = val

    @__refresher__(True)
    def sobolev_filter(self, kernel, activate):
        self.actions['sobolev'][kernel] = activate

    @__refresher__(True)
    def erosion_change(self, erosion):
        if erosion == 0:
            self.actions['erosion'] = None
            return
        kernel = np.ones((erosion, erosion), np.uint8)
        self.actions['erosion'] = kernel

    @__refresher__(True)
    def dilation_change(self, dilation):
        if dilation == 0:
            self.actions['dilation'] = None
            return
        kernel = np.ones((dilation, dilation), np.uint8)
        self.actions['dilation'] = kernel

    @__refresher__(True)
    def opening_change(self, opening):
        if opening == 0:
            self.actions['opening'] = None
            return
        kernel = np.ones((opening, opening), np.uint8)
        self.actions['opening'] = kernel

    @__refresher__(True)
    def closing_change(self, closing):
        if closing == 0:
            self.actions['closing'] = None
            return
        kernel = np.ones((closing, closing), np.uint8)
        self.actions['closing'] = kernel

    @__refresher__(False)
    def get_contours(self, event):
        matrix = np.array(self.modified).astype(np.uint8)
        contours, hierarchy = cv.findContours(matrix, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        areas = [cv.contourArea(cnt) for cnt in contours]
        self.contours_detected = (contours, areas)

    @__refresher__(False)
    def set_treshold_contours(self, min_len):
        self.min_contour_len = min_len


    @__refresher__(False)
    def spot_triangles(self, event):
        def __get_mask(main_corn, corn_1, corn_2, center):
            # get vectors for angle lines
            vec1 = corn_1 - main_corn
            vec2 = corn_2 - main_corn

            # get projections of mass center to lines
            p1 = main_corn + vec1 * np.dot(center - main_corn, vec1) / (np.linalg.norm(vec1) ** 2)
            p2 = main_corn + vec2 * np.dot(center - main_corn, vec2) / (np.linalg.norm(vec2) ** 2)

            return np.array([main_corn, p1.astype(int), center, p2.astype(int)])
            
        if self.contours_detected is None:
            return None
        
        contours = [cnt for cnt, area in zip(*self.contours_detected) if area >= self.min_contour_len]
        triangle_contours = []
        convexes = []

        

        for cnt in contours:
            approx = cv.approxPolyDP(cnt, 0.07 * cv.arcLength(cnt, True), True)
            if len(approx) == 3:
                center = get_center(cnt)
                corn1 = approx[0][0]
                corn2 = approx[1][0]
                corn3 = approx[2][0]

                convex1 = __get_mask(corn1, corn2, corn3, center)
                convex2 = __get_mask(corn2, corn1, corn3, center)
                convex3 = __get_mask(corn3, corn1, corn2, center)

                convexes.append([convex1, convex2, convex3])
                triangle_contours.append(cnt)
                
        self.triangle_contours = triangle_contours
        self.convexes = convexes

    @__refresher__(False)
    def set_param_dots_bin(self, val):
        self.actions['param_dots_bin'] = val
        
    @__refresher__(False)
    def set_curv_ind(self, val):
        self.actions['curv_ind'] = (val / 100) * 480 / 99 + 15 / 99

    # @__refresher__(False)
    # def set_min_rad(self, val):
    #     self.actions['min_rad'] = val

    # @__refresher__(False)
    # def set_max_rad(self, val):
    #     self.actions['max_rad'] = val
