from PyQt6.QtWidgets import QToolBox, QWidget, QVBoxLayout

from Tools.ColorDials import ColorDials
from Tools.CVtools import CVtools
from Tools.DefaultPalette import DefaultPalette
# from Tools.DefaultPalette import DefaultPalette
# from Tools.CountObjects import CountObjects


class ToolsPaletes(QWidget):
    def __init__(self, topWidget, engine):
        super().__init__(topWidget)
        self.engine = engine

        layout = QVBoxLayout()
        tlbx = QToolBox()

        tlbx.addItem(ColorDials(self, engine), 'Точечные операции')
        tlbx.addItem(CVtools(self, engine), 'Морфологические операции')
        # tlbx.addItem(CountObjects(self, engine), 'Подсчет объектов')
        tlbx.addItem(DefaultPalette(self, engine), 'demo изображения')

        layout.addWidget(tlbx)

        self.setMinimumWidth(400)
        self.setMinimumHeight(400)
        self.setLayout(layout)
