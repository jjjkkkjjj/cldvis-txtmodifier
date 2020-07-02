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
            self.rubberBand.move(endPosition - self.startPosition)
        else:
            self.rubberBand.setGeometry(QRect(self.startPosition, endPosition).normalized())


    def mouseReleaseEvent(self, e: QMouseEvent):
        rect = self.rubberBand.geometry()
        self.rubberBand.setGeometry(rect)

        self.startPosition = None

