from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from .img import ImgWidget

class CanvasWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.rubbers = []

        self.initUI()

    def initUI(self):
        self.setStyleSheet("margin:5px; border:1px solid rgb(0, 0, 0); ")
        vbox = QVBoxLayout()

        #self.scrollArea = QScrollArea(self)
        self.img = ImgWidget(self)
        #self.scrollArea.setWidget(self.img)
        vbox.addWidget(self.img)

        self.setLayout(vbox)
