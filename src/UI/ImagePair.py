from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFileDialog, QPushButton
from PyQt6.QtCore import QSize

from UI.ImageBox import OriginalImage, ModifiedImage

class ImagePair(QWidget):
    def __init__(self, topWidget, engine):
        super().__init__(topWidget)
        self.engine = engine

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.setFixedSize(QSize(1080, 500))

        self.OriginalImage = OriginalImage(self, engine)
        self.layout.addWidget(self.OriginalImage)
        self.ModifiedImage = ModifiedImage(self, engine)
        self.layout.addWidget(self.ModifiedImage)
