from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import os, cv2

from ..utils.funcs import check_instance, cvimg2qpixmap
from ..utils.modes import PredictionMode, MoveActionState, ShowingMode
from ..utils.geometry import *
from ..model import Model

class ImageView(QLabel):
    ### Signal ###
    areaChanged = Signal()

    # model
    model: Model
    def __init__(self, model: Model, parent=None):
        super().__init__(parent)

        self.model = check_instance('model', model, Model)

        self.moveActionState = MoveActionState.CREATE

        # mouseMoveEvent will be fired on pressing any button
        self.setMouseTracking(True)


    def updateUI(self):
        if self.model.predmode == PredictionMode.IMAGE:
            self.model.rect_imagemode.show()
            self.model.poly_tablemode.hide()
        elif self.model.predmode == PredictionMode.TABLE:
            self.model.rect_imagemode.hide()
            self.model.poly_tablemode.show()
        self.repaint()

    def mousePressEvent(self, e: QMouseEvent):
        # Note that this method is called earlier than contextMenuEvent
        if self.model.predmode == PredictionMode.IMAGE:
            self.model.mousePress_imagemode(e.pos(), self.size())

        elif self.model.predmode == PredictionMode.TABLE:
            self.model.mousePress_tablemode(e.pos(), self.size())

        self.updateUI()

    def mouseMoveEvent(self, e: QMouseEvent):
        # Note that this method is called earlier than contextMenuEvent
        if isinstance(e, QContextMenuEvent):
            return

        pos = e.pos()
        if e.buttons() == Qt.LeftButton:
            # in clicking
            if self.model.predmode == PredictionMode.IMAGE:
                self.model.mouseMoveClicked_imagemode(pos, self.size())
            elif self.model.predmode == PredictionMode.TABLE:
                self.model.mouseMoveClicked_tablemode(pos, self.size())

        elif e.buttons() == Qt.NoButton:
            if self.model.predmode == PredictionMode.IMAGE:
                self.model.mouseMoveNoButton_imagemode(pos)
            elif self.model.predmode == PredictionMode.TABLE:
                self.model.mouseMoveNoButton_tablemode(pos)

        self.updateUI()

    def mouseReleaseEvent(self, e: QMouseEvent):
        if self.model.predmode == PredictionMode.IMAGE:
            self.model.mouseRelease_imagemode()
        elif self.model.predmode == PredictionMode.TABLE:
            self.model.mouseRelease_tablemode()

        self.updateUI()
        self.areaChanged.emit()

    def paintEvent(self, event):
        if not self.pixmap():
            return super().paintEvent(event)

        # painter
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.pixmap())

        # pen
        pen = QPen(QColor(255, 0, 0))
        pen.setWidth(3)

        # set
        painter.setPen(pen)

        if self.model.predmode == PredictionMode.IMAGE:
            self.model.rect_imagemode.paint(painter)
        elif self.model.predmode == PredictionMode.TABLE:
            self.model.poly_tablemode.paint(painter)

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
        self.imageView = ImageView(self.model, self)

        self.imageView.setBackgroundRole(QPalette.Base)
        # self.img.setScaledContents(True) # allow to stretch

        # self.scrollArea.setStyleSheet("margin:5px; border:1px solid rgb(0, 0, 0); ")
        self.scrollArea.setWidget(self.imageView)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setBackgroundRole(QPalette.Dark)
        vbox.addWidget(self.scrollArea)

        self.setLayout(vbox)

    def updateUI(self):
        self.imageView.updateUI()

        # check enable
        self.label_filename.setEnabled(self.model.isExistImg)
        self.imageView.setEnabled(self.model.isExistImg)

        if not self.model.isExistImg:
            return

        # set image
        self.label_filename.setText('Filename: {}'.format(os.path.basename(self.model.imgpath)))

        """
        # below code is not good resizing
        pixmap = QPixmap(imgpath)
        self.img.setPixmap(None)
        self.img.setPixmap(pixmap.scaled(pixmap.parentQSize() * zoomvalue / 100., Qt.KeepAspectRatio, Qt.SmoothTransformation))
        """
        if self.model.showingmode == ShowingMode.ENTIRE:
            cvimg = cv2.imread(self.model.imgpath)
        elif self.model.showingmode == ShowingMode.SELECTED:
            cvimg = cv2.imread(self.model.selectedImgPath)
        h, w, c = cvimg.shape
        ratio = self.model.zoomvalue / 100.
        pixmap = cvimg2qpixmap(cv2.resize(cvimg, (int(w * ratio), int(h * ratio))))
        self.imageView.setPixmap(pixmap)

        # set parentSize
        if self.model.predmode == PredictionMode.IMAGE:
            self.model.rect_imagemode.set_parentVals(parentQSize=pixmap.size())
        elif self.model.predmode == PredictionMode.TABLE:
            self.model.poly_tablemode.set_parentVals(parentQSize=pixmap.size())
