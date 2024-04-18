from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QSize
from PyQt6.QtCore import Qt

import os


class SmartImageBox(QLabel):
    def __init__(self, topWidget, engine, imagePath):
        super().__init__(topWidget)
        self.engine = engine

        self.imagePath = imagePath

        self.setPixmap(QPixmap(imagePath))
        self.setScaledContents(True)
        self.setMaximumSize(QSize(75, 75))
        self.setMinimumSize(QSize(30, 30))

        self.setStyleSheet(
            "border: 3px solid white; border-radius: 5px; margin-right: 5px")

    def mousePressEvent(self, event):
        self.engine.upload_picture(self.imagePath)


class DefaultPalette(QWidget):
    def __init__(self, topWidget, engine):
        super().__init__(topWidget)
        self.engine = engine

        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()

        group_comment = QLabel('Примеры изображений:')
        layout.addWidget(group_comment)

        image_rows = [QHBoxLayout(), QHBoxLayout(), QHBoxLayout()]

        k = -1
        for i, rel_path in enumerate(sorted([*os.listdir('imgs/test')])):
            if rel_path[0] == '.':
                continue
            k += 1
            path = os.path.join('imgs/test', rel_path)
            image_rows[k // 3].addWidget(SmartImageBox(self, engine, path))

        layout.addItem(image_rows[0])
        image_rows[0].addStretch()
        layout.addItem(image_rows[1])
        image_rows[1].addStretch()
        layout.addItem(image_rows[2])
        image_rows[2].addStretch()
