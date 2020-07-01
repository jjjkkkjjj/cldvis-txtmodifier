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
        vbox = QVBoxLayout()

        self.scrollArea = QScrollArea(self)
        self.img = ImgWidget(self)

        self.img.setBackgroundRole(QPalette.Base)
        self.img.setScaledContents(True) # allow to stretch

        #self.scrollArea.setStyleSheet("margin:5px; border:1px solid rgb(0, 0, 0); ")
        self.scrollArea.setWidget(self.img)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setBackgroundRole(QPalette.Dark)
        vbox.addWidget(self.scrollArea)

        self.setLayout(vbox)


    def set_img(self, imgpath):
        """
        :param imgpath: str or None, if None is passed, show blank
        :return:
        """
        pixmap = QPixmap(imgpath)

        self.img.setPixmap(pixmap)
