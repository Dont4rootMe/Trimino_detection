from PyQt6.QtWidgets import QDial, QWidget, QSlider, QHBoxLayout, QLabel, QVBoxLayout, QPushButton, QFormLayout
from PyQt6.QtCore import QSize
from PyQt6.QtCore import Qt


class TriangularFinder(QWidget):
    def __init__(self, topWidget, engine):
        super().__init__(topWidget)
        self.engine = engine

        # main layout of palette
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # button for getting all contours
        self.button_layout = QHBoxLayout()

        # spotting all dominos
        self.button_spot = QPushButton('Получить контуры')
        self.button_spot.clicked.connect(self.engine.get_contours)
        self.button_layout.addWidget(self.button_spot)

        # finding all triangulars
        self.button_spot = QPushButton('Определить треугольники')
        self.button_spot.clicked.connect(self.engine.spot_triangles)
        self.button_layout.addWidget(self.button_spot)

        # threshold of min countr length
        self.layout_treshold = QHBoxLayout()
        self.treshold_label = QLabel('Мин. площадь контура: ')
        self.layout_treshold.addWidget(self.treshold_label)
        
        self.treshhold_slider = QSlider(Qt.Orientation.Horizontal)
        self.treshhold_slider.setRange(1, 255)
        self.treshhold_slider.setValue(10)
        self.treshhold_slider.setFixedSize(QSize(200, 30))
        self.treshhold_slider.valueChanged.connect(self.engine.set_treshold_contours)
        self.layout_treshold.addWidget(self.treshhold_slider)


        # make settings for dot-recognition
        self.layout_dot_param = QHBoxLayout()
        self.dot_label = QLabel('Параметр поиска точек: ')
        self.layout_dot_param.addWidget(self.dot_label)
        
        self.dot_slider = QSlider(Qt.Orientation.Horizontal)
        self.dot_slider.setRange(5, 80)
        self.dot_slider.setValue(30)
        self.dot_slider.setFixedSize(QSize(200, 30))
        self.dot_slider.valueChanged.connect(self.engine.set_param_dots_bin)
        self.layout_dot_param.addWidget(self.dot_slider)

        # make settings for curv-index treshold
        self.layout_curv = QHBoxLayout()
        self.curv_label = QLabel('Порог индекса кривизны: ')
        self.layout_curv.addWidget(self.curv_label)
        
        self.curv_slider = QSlider(Qt.Orientation.Horizontal)
        self.curv_slider.setRange(1, 100)
        self.curv_slider.setValue(30)
        self.curv_slider.setFixedSize(QSize(200, 30))
        self.curv_slider.valueChanged.connect(self.engine.set_curv_ind)
        self.layout_curv.addWidget(self.curv_slider)

        self.layout.addItem(self.button_layout)
        self.layout.addItem(self.layout_treshold)
        self.layout.addItem(self.layout_dot_param)
        self.layout.addItem(self.layout_curv)
        self.setLayout(self.layout)

    def clear(self):
        self.treshhold_slider.setValue(10)
        self.dot_slider.setValue(30)
        self.curv_slider.setValue(30)