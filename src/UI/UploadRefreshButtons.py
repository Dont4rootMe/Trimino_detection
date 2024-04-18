from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QFileDialog

class UploadRefreshButtons(QWidget):
    def __init__(self, topWidget, engine):
        super().__init__(topWidget)
        self.engine = engine

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        # uppload new user defined image
        self.upload_button = QPushButton('Upload img')
        self.upload_button.clicked.connect(self.uploadImage)
        self.layout.addWidget(self.upload_button)

        # reset button for canceling all prev actions on image
        self.reset_actions = QPushButton('Reset actions')
        self.reset_actions.clicked.connect(self.engine.reset)
        self.layout.addWidget(self.reset_actions)

        self.setMinimumWidth(150)
        self.setMaximumWidth(300)

    def uploadImage(self):
        file_input = QFileDialog()
        if file_input.exec():
            self.engine.upload_picture(file_input.selectedFiles()[0])

