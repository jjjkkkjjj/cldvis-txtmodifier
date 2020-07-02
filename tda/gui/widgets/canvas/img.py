from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from .rubber import Rubber, MoveActionState

class ImgWidget(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.startPosition = None
        self.endPosition = None

        self.moveActionState = MoveActionState.CREATE

        self.rubberBand = Rubber(self)


    def mousePressEvent(self, e: QMouseEvent):
        self.startPosition, self.moveActionState = self.rubberBand.press(e.pos())

    def mouseMoveEvent(self, e: QMouseEvent):
        endPosition = e.pos()
        if self.moveActionState == MoveActionState.MOVE:  # move
            movedPosition = endPosition - self.startPosition
            # clipping
            movedPosition.setX(min(max(movedPosition.x(), 0), self.geometry().width() - self.rubberBand.width()))
            movedPosition.setY(min(max(movedPosition.y(), 0), self.geometry().height() - self.rubberBand.height()))
            self.rubberBand.move(movedPosition)
        else:
            # clipping
            endPosition.setX(min(max(endPosition.x(), 0), self.geometry().width()))
            endPosition.setY(min(max(endPosition.y(), 0), self.geometry().height()))

            self.rubberBand.setGeometry(QRect(self.startPosition, endPosition).normalized())


    def mouseReleaseEvent(self, e: QMouseEvent):
        rect = self.rubberBand.geometry()
        self.rubberBand.setGeometry(rect)

        self.startPosition = None

    def set_ratio(self, ratio, prevImgSize):
        if self.rubberBand.isHidden():
            return

        # to percent
        tlX_percent = float(self.rubberBand.geometry().topLeft().x()) / prevImgSize.width()
        tlY_percent = float(self.rubberBand.geometry().topLeft().y()) / prevImgSize.height()
        brX_percent = float(self.rubberBand.geometry().bottomRight().x()) / prevImgSize.width()
        brY_percent = float(self.rubberBand.geometry().bottomRight().y()) / prevImgSize.height()

        newImgSize = prevImgSize * ratio

        newRect = QRect(QPoint(int(tlX_percent * newImgSize.width()), int(tlY_percent * newImgSize.height())),
                        QPoint(int(brX_percent * newImgSize.width()), int(brY_percent * newImgSize.height())))

        self.rubberBand.setGeometry(newRect)