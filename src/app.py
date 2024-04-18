import sys
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QFileDialog
from PyQt6.QtGui import QIcon

from engine import Engine
from UI.ImagePair import ImagePair
from UI.UploadRefreshButtons import UploadRefreshButtons
from Tools.ToolsPaletes import ToolsPaletes

class MainFrame(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image = None

        self.setWindowTitle('Поиск тримино')

        mainlayout = QVBoxLayout()
        self.setLayout(mainlayout)

        # create single instance of engine for programm
        engine = Engine()

        # main two columns of app
        innerlayout = QHBoxLayout()
        mainlayout.addItem(innerlayout)

        # adding visual palletes
        innerlayout.addWidget(ToolsPaletes(self, engine))
        innerlayout.addWidget(ImagePair(self, engine))

        # adding buttons to form
        mainlayout.addWidget(UploadRefreshButtons(self, engine))

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('imgs/app_imgs/logo.png'))
    window = MainFrame()
    app.exec()
