from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from .rubber import Rubber, MoveActionState

class ImgWidget(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.startPosition = None

        self.moveActionState = MoveActionState.CREATE

        self.rubberBand = Rubber(self)
        self.rubberPercentRect = (0., 0., 0., 0.)

    @property
    def left_percent(self):
        return self.rubberPercentRect[0]
    @property
    def top_percent(self):
        return self.rubberPercentRect[1]
    @property
    def right_percent(self):
        return self.rubberPercentRect[2]
    @property
    def bottom_percent(self):
        return self.rubberPercentRect[3]

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

        self.rubberPercentRect = (self.rubberBand.geometry().left()/self.width(), self.rubberBand.geometry().top()/self.height(),
                                  self.rubberBand.geometry().right()/self.width(), self.rubberBand.geometry().bottom()/self.height())

        self.startPosition = None

    def setPixmap(self, pixmap: QPixmap):
        super().setPixmap(pixmap)
        if self.rubberBand.isHidden():
            return

        newImgSize = pixmap.size()

        # to percent
        tlX = int(self.left_percent * newImgSize.width())
        tlY = int(self.top_percent * newImgSize.height())
        brX = int(self.right_percent * newImgSize.width())
        brY = int(self.bottom_percent * newImgSize.height())

        newRect = QRect(tlX, tlY, brX - tlX, brY - tlY)

        self.rubberBand.setGeometry(newRect)