from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import cv2, os

from .img import ImgWidget
from ..baseWidget import BaseWidget
from ...functions.utils import cvimg2qpixmap

class CanvasWidget(BaseWidget):
    rubberCreated = Signal(tuple)
    enableChecking = Signal()
    def __init__(self, mainWidgetController):
        super().__init__(mainWidgetController)

        self.rubbers = []

        self.initUI()
        self.establish_connection()

    def initUI(self):
        vbox = QVBoxLayout()

        self.label_filename = QLabel(self)
        self.label_filename.setText('Filename:')
        vbox.addWidget(self.label_filename)

        self.scrollArea = QScrollArea(self)
        self.img = ImgWidget(self)

        self.img.setBackgroundRole(QPalette.Base)
        #self.img.setScaledContents(True) # allow to stretch

        #self.scrollArea.setStyleSheet("margin:5px; border:1px solid rgb(0, 0, 0); ")
        self.scrollArea.setWidget(self.img)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setBackgroundRole(QPalette.Dark)
        vbox.addWidget(self.scrollArea)

        self.setLayout(vbox)

    def establish_connection(self):
        self.rubberCreated = self.img.rubberCreated
        #self.img.rubberCreated.connect(lambda rubberPercentRect: self.set_rubber(rubberPercentRect))


    def set_img(self, imgpath, zoomvalue):
        """
        :param imgpath: str or None, if None is passed, show blank
        :param zoomvalue: int, 20~200
        :return:
        """
        if imgpath is not None and imgpath != '':

            self.label_filename.setText('Filename: {}'.format(os.path.basename(imgpath)))

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

            self.img.setPixmap(pixmap)

    def set_rubber(self, rubberPercentRect):
        """
        :param rubberPercentRect: tuple or None, if it's None, remove rubber band
        :return:
        """
        if rubberPercentRect is None:
            # remove
            self.img.refresh_rubberBand()
        self.enableChecking.emit()

    def set_predictedRubber(self):
        self.img.rubber2predictedRubber()

    def check_enable(self, isExistImg):
        self.setEnabled(isExistImg)