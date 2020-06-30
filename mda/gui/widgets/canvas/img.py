from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from enum import Enum

class ImgWidget(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.startPosition = None
        self.endPosition = None
        self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)

        self.zoomRBTopLeft = QRubberBand(QRubberBand.Rectangle, self)
        self.zoomRBTopRight = QRubberBand(QRubberBand.Rectangle, self)
        self.zoomRBButtomLeft = QRubberBand(QRubberBand.Rectangle, self)
        self.zoomRBButtomRight = QRubberBand(QRubberBand.Rectangle, self)

        pal = QPalette()
        pal.setBrush(QPalette.Highlight, QBrush(Qt.red))
        self.zoomRBTopLeft.setPalette(pal)
        self.zoomRBTopRight.setPalette(pal)
        self.zoomRBButtomLeft.setPalette(pal)
        self.zoomRBButtomRight.setPalette(pal)

        self.moveActionState = MoveActionState.CREATE

        self.zoomRange = 20

    def mousePressEvent(self, e: QMouseEvent):
        self.startPosition = e.pos()

        if self.rubberBand.geometry().contains(self.startPosition):
            if self.zoomRBTopLeft.geometry().contains(self.startPosition):
                self.startPosition = self.rubberBand.geometry().bottomRight()
                self.moveActionState = MoveActionState.ZOOM_FROM_BOTTOM_RIGHT  # means zoomimg
            elif self.zoomRBTopRight.geometry().contains(self.startPosition):
                self.startPosition = self.rubberBand.geometry().bottomLeft()
                self.moveActionState = MoveActionState.ZOOM_FROM_BOTTOM_LEFT  # means zoomimg
            elif self.zoomRBButtomLeft.geometry().contains(self.startPosition):
                self.startPosition = self.rubberBand.geometry().topRight()
                self.moveActionState = MoveActionState.ZOOM_FROM_TOP_RIGHT  # means zoomimg
            elif self.zoomRBButtomRight.geometry().contains(self.startPosition):
                self.startPosition = self.rubberBand.geometry().topLeft()
                self.moveActionState = MoveActionState.ZOOM_FROM_TOP_LEFT  # means zoomimg
            else:
                self.startPosition = self.startPosition - self.rubberBand.pos()
                self.moveActionState = MoveActionState.MOVE  # means moving
        else:  # create new rubberband
            self.rubberBand.setGeometry(QRect(self.startPosition, QSize()))
            self.rubberBand.show()

            self.moveActionState = MoveActionState.CREATE  # means creating new rubberband

        self.zoomRBTopLeft.hide()
        self.zoomRBTopRight.hide()
        self.zoomRBButtomLeft.hide()
        self.zoomRBButtomRight.hide()

    def mouseMoveEvent(self, e: QMouseEvent):
        endPosition = e.pos()
        if self.moveActionState == MoveActionState.MOVE:  # move
            self.rubberBand.move(endPosition - self.startPosition)
        else:
            self.rubberBand.setGeometry(QRect(self.startPosition, endPosition).normalized())

    def mouseReleaseEvent(self, e: QMouseEvent):
        rect = self.rubberBand.geometry()
        self.setRubberBandGeometry(rect)

        """
        var = Vars()
        if self.parent.checkBoxAllImage.isChecked():
            var.setAllRectangleValue(rect)
        else:
            var.setSingleRectangleValue(rect, self.moveActionState, self.startPosition, e.pos())
        """

        self.startPosition = None

    def setRubberBandGeometry(self, rect):
        self.rubberBand.setGeometry(rect)
        if min(rect.width(), rect.height()) < 80:
            self.zoomRange = min(rect.width(), rect.height()) * 0.25
        else:
            self.zoomRange = 20

        tlX, tlY = rect.topLeft().x(), rect.topLeft().y()
        brX, brY = rect.bottomRight().x(), rect.bottomRight().y()
        tr = rect.topRight()
        tr.setY(tlY + self.zoomRange)
        bl = rect.bottomLeft()
        bl.setX(tlX + self.zoomRange)
        # zoom range
        self.zoomRBTopLeft.setGeometry(QRect(tlX, tlY, self.zoomRange, self.zoomRange))
        self.zoomRBTopRight.setGeometry(QRect(QPoint(brX - self.zoomRange, tlY), tr))
        self.zoomRBButtomLeft.setGeometry(QRect(QPoint(tlX, brY - self.zoomRange), bl))
        self.zoomRBButtomRight.setGeometry(
            QRect(QPoint(brX - self.zoomRange, brY - self.zoomRange), rect.bottomRight()))

        self.rubberBand.show()
        self.zoomRBTopLeft.show()
        self.zoomRBTopRight.show()
        self.zoomRBButtomLeft.show()
        self.zoomRBButtomRight.show()

    def resetWidget(self):
        self.rubberBand.hide()
        self.zoomRBTopLeft.hide()
        self.zoomRBTopRight.hide()
        self.zoomRBButtomLeft.hide()
        self.zoomRBButtomRight.hide()

class MoveActionState(Enum):
    CREATE = 0
    ZOOM_FROM_BOTTOM_RIGHT = 1
    ZOOM_FROM_BOTTOM_LEFT = 2
    ZOOM_FROM_TOP_RIGHT = 3
    ZOOM_FROM_TOP_LEFT = 4
    MOVE = 5