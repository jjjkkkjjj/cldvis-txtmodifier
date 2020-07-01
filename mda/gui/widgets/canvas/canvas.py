from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from .img import ImgWidget
from ..baseWidget import BaseWidget

class CanvasWidget(BaseWidget):
    def __init__(self, mainWidget):
        super().__init__(mainWidget)

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


    def set_img(self, imgpath):
        """
        :param imgpath: str or None, if None is passed, show blank
        :return:
        """
        pass
