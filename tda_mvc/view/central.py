from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import os, cv2

from ..utils.funcs import check_instance, cvimg2qpixmap
from ..model import Model

class ImageView(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)

        # mouseMoveEvent will be fired on pressing any button
        self.setMouseTracking(True)

class CentralView(QWidget):
    ### Attributes ###
    # label
    label_filename: QLabel

    # image
    scrollArea: QScrollArea
    imageView: ImageView

    # model
    model: Model

    def __init__(self, model: Model, parent=None):
        super().__init__(parent=parent)

        self.model = check_instance('model', model, Model)
        self.initUI()
        self.updateUI()

    def initUI(self):
        vbox = QVBoxLayout()

        # filename label
        self.label_filename = QLabel(self)
        self.label_filename.setText('Filename:')
        vbox.addWidget(self.label_filename)

        # image
        self.scrollArea = QScrollArea(self)
        self.imageView = ImageView(self)

        self.imageView.setBackgroundRole(QPalette.Base)
        # self.img.setScaledContents(True) # allow to stretch

        # self.scrollArea.setStyleSheet("margin:5px; border:1px solid rgb(0, 0, 0); ")
        self.scrollArea.setWidget(self.imageView)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setBackgroundRole(QPalette.Dark)
        vbox.addWidget(self.scrollArea)

        self.setLayout(vbox)

    def updateUI(self):
        if not self.model.isExistImg:
            return

        self.label_filename.setText('Filename: {}'.format(os.path.basename(self.model.imgpath)))

        """
        # below code is not good resizing
        pixmap = QPixmap(imgpath)
        self.img.setPixmap(None)
        self.img.setPixmap(pixmap.scaled(pixmap.parentQSize() * zoomvalue / 100., Qt.KeepAspectRatio, Qt.SmoothTransformation))
        """
        cvimg = cv2.imread(self.model.imgpath)
        h, w, c = cvimg.shape
        ratio = self.model.zoomvalue / 100.
        pixmap = cvimg2qpixmap(cv2.resize(cvimg, (int(w * ratio), int(h * ratio))))

        self.imageView.setPixmap(pixmap)




