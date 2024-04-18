from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import QSize

class ImageBoxAbstract(QLabel):
    def __init__(self, topWidget, engine):
        super().__init__(topWidget)
        self.engine = engine
        self.engine.add_refresh_action(self.actionOnRefreshReset())
        self.engine.add_reset_action(self.actionOnRefreshReset())

        self.setScaledContents(True)
        self.setFixedSize(QSize(380, 380))
        # self.setMaximumSize(QSize(650, 300))
        # self.setMinimumSize(QSize(300, 300))


class OriginalImage(ImageBoxAbstract):
    def __init__(self, topWidget, engine):
        super().__init__(topWidget, engine)

    def update_pic(self):
        if self.engine.original_pixmap_exist():
            self.setPixmap(self.engine.get_original_pixmap())

    def actionOnRefreshReset(self):
        return self.update_pic
    
class ModifiedImage(ImageBoxAbstract):
    def __init__(self, topWidget, engine):
        super().__init__(topWidget, engine)

    def update_pic(self):
        if self.engine.modified_pixmap_exist():
            self.setPixmap(self.engine.get_modified_pixmap())

    def actionOnRefreshReset(self):
        return self.update_pic