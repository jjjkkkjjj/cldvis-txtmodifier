from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import cv2, os

from .img import ImgWidget
from ..baseWidget import BaseWidget
from ...functions.utils import cvimg2qpixmap
from ..eveUtils import ShowingMode

class CanvasWidget(BaseWidget):
    selectionAreaCreated = Signal(tuple)
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
        self.selectionAreaCreated = self.img.selectionAreaCreated
        #self.img.selectionAreaCreated.connect(lambda areaPercentPolygon: self.set_selectionArea(areaPercentPolygon))


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
            self.img.setPixmap(pixmap.scaled(pixmap.parentQSize() * zoomvalue / 100., Qt.KeepAspectRatio, Qt.SmoothTransformation))
            """
            cvimg = cv2.imread(imgpath)
            h, w, c = cvimg.shape
            ratio = zoomvalue / 100.
            pixmap = cvimg2qpixmap(cv2.resize(cvimg, (int(w*ratio), int(h*ratio))))

            self.img.setPixmap(pixmap)

    def set_selectionArea(self, areaPercentRect):
        """
        :param areaPercentRect: tuple or None, if it's None, remove rubber band
        :return:
        """
        if areaPercentRect is None:
            # hide
            self.img.hide_selectionArea()
        self.enableChecking.emit()

    def switch_areaMode(self, areamode, showingmode):
        self.img.switch_areaMode(areamode, showingmode)

    def check_enable(self, isExistImg):
        self.setEnabled(isExistImg)