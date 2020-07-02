from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import cv2

from .img import ImgWidget
from ..baseWidget import BaseWidget
from ...functions.utils import cvimg2qpixmap

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


    def set_img(self, imgpath, zoomvalue):
        """
        :param imgpath: str or None, if None is passed, show blank
        :param zoomvalue: int, 20~200
        :return:
        """
        if imgpath is not None and imgpath != '':
            """
            # below code is not good resizing
            pixmap = QPixmap(imgpath)
            self.img.setPixmap(None)
            self.img.setPixmap(pixmap.scaled(pixmap.size() * zoomvalue / 100., Qt.KeepAspectRatio, Qt.SmoothTransformation))
            """
            cvimg = cv2.imread(imgpath)
            h, w, c = cvimg.shape
            ratio = zoomvalue / 100.
            pixmap = cvimg2qpixmap(cv2.resize(cvimg, (int(w*ratio), int(h*ratio))))
            self.img.set_ratio(ratio, QSize(w, h))
            self.img.setPixmap(pixmap)