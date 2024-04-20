from PyQt6.QtWidgets import QWidget, QFormLayout, QPushButton, QHBoxLayout, QVBoxLayout, QSlider, QCheckBox, QLabel
from PyQt6.QtCore import QSize
from PyQt6.QtCore import Qt

CLICKED_BUTTON_STYLE = '''
    background-color: #4e80ee;
    border-radius: 4px; 
    padding: 14px; 
    padding-top: 2px; 
    padding-bottom: 2px; 
    margin: 1px;
    margin-top: 1px;
    margin-bottom: 1px;
'''


class CVtools(QWidget):
    class __morph_tool(QWidget):
        def __init__(self, topWidget, func):
            super().__init__(topWidget)
            self.func = func

            # define layout
            self.layout = QHBoxLayout()

            # add kernel size define-slider
            self.slider = QSlider(Qt.Orientation.Horizontal)
            self.slider.setRange(0, 10)
            self.slider.setValue(0)
            self.slider.setFixedSize(QSize(200, 30))
            self.slider.valueChanged.connect(self.func)
            self.layout.addWidget(self.slider)

            self.setLayout(self.layout)
        
        def clear_morph(self):
            self.slider.setValue(0)

    class __CannyFilter(QWidget):
        def __init__(self, topWidget, engine):
            super().__init__(topWidget)
            self.engine = engine

            self.layout = QVBoxLayout()

            # add checkbox for Canny filter
            self.checkbox = QCheckBox('применять')
            self.checkbox.stateChanged.connect(self.engine.use_canny_filter)
            self.layout.addWidget(self.checkbox)

            self.setLayout(self.layout)
            self.engine.add_reset_action(self.clear_checkbox)

        def clear_checkbox(self):
            self.checkbox.setChecked(False)

    class __SobolevFilter(QWidget):
        def __init__(self, topModel, engine):
            super().__init__(topModel)
            self.engine = engine

            self.click_map = {
                '3': False,
                '5': False,
                '7': False
            }

            self.btn3 = QPushButton('3x3')
            self.btn3.clicked.connect(self.btn3_click)
            self.btn5 = QPushButton('5x5')
            self.btn5.clicked.connect(self.btn5_click)
            self.btn7 = QPushButton('7x7')
            self.btn7.clicked.connect(self.btn7_click)

            layout = QHBoxLayout()
            layout.addWidget(self.btn3)
            layout.addWidget(self.btn5)
            layout.addWidget(self.btn7)

            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)
            self.setLayout(layout)

        def btn3_click(self, event):
            self.click_map['3'] = not self.click_map['3']
            self.engine.sobolev_filter(3, self.click_map['3'])
            self.btn3.setStyleSheet(CLICKED_BUTTON_STYLE if self.click_map['3'] else None)
        
        def btn5_click(self, event):
            self.click_map['5'] = not self.click_map['5']
            self.engine.sobolev_filter(5, self.click_map['5'])
            self.btn5.setStyleSheet(CLICKED_BUTTON_STYLE if self.click_map['5'] else None)

        def btn7_click(self, event):
            self.click_map['7'] = not self.click_map['7']
            self.engine.sobolev_filter(7, self.click_map['7'])
            self.btn7.setStyleSheet(CLICKED_BUTTON_STYLE if self.click_map['7'] else None)

        def clear_sobol(self):
            self.btn3.setStyleSheet(None)
            self.btn5.setStyleSheet(None)
            self.btn7.setStyleSheet(None)


    def __init__(self, topModel, engine):
        super().__init__(topModel)
        self.engine = engine

        self.canny_detect = self.__CannyFilter(self, self.engine)
        self.sobolev = self.__SobolevFilter(self, self.engine)

        self.erosion_tool  = self.__morph_tool(self, self.engine.erosion_change)
        self.dilation_tool = self.__morph_tool(self, self.engine.dilation_change)
        self.opening_tool  = self.__morph_tool(self, self.engine.opening_change)
        self.closing_tool  = self.__morph_tool(self, self.engine.closing_change)

        self.layout = QFormLayout()
        self.layout.addRow('Canny filter: ', self.canny_detect)
        self.layout.addRow('Sobolev filter: ', self.sobolev)
        self.layout.addRow('Dilation: ', self.dilation_tool)
        self.layout.addRow('Closing: ', self.closing_tool)
        self.layout.addRow('Erosion: ', self.erosion_tool)
        self.layout.addRow('Opening: ', self.opening_tool)

        self.engine.add_reset_action(self.clear_styles)
        self.setLayout(self.layout)

    def clear_styles(self):
        self.erosion_tool.clear_morph()
        self.dilation_tool.clear_morph()
        self.opening_tool.clear_morph()
        self.closing_tool.clear_morph()

        self.sobolev.clear_sobol()
        self.engine.sobolev_filter(3, False)
        self.engine.sobolev_filter(5, False)
        self.engine.sobolev_filter(7, False)
