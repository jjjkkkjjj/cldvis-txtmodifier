from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

import numpy as np

from .geometry import Rect
from ..widgets.eveUtils import MoveActionState

class SelectionManager(object):
    def __init__(self):
        self._selectionArea = Rect(np.zeros(shape=(2, 2)))

        self.moveActionState = MoveActionState.CREATE
        self._startPosition = QPoint(0, 0)

    @property
    def area(self):
        return self._selectionArea

    @property
    def width(self):
        return self._selectionArea.width
    @property
    def height(self):
        return self._selectionArea.height

    @property
    def parentWidth(self):
        return self._selectionArea.parentWidth
    @property
    def parentHeight(self):
        return self._selectionArea.parentHeight

    def mousePress(self, parentSize, pos):
        """
        :param parentSize: QSize, the parentQSize
        :param pos: QPoint, pressed position
        :return:
        """
        # set parentQSize and position
        self._selectionArea.set_parentVals(parentQSize=parentSize)
        self._selectionArea.set_selectPos(pos)
        self._selectionArea.show()
        if self._selectionArea.isSelectedPoint:
            # if pressed position is edge
            # expand or shrink parentQSize
            self.moveActionState = MoveActionState.RESIZE

        elif self._selectionArea.isSelectedRect:
            # if pressed position is contained in parentQSize
            # move the parentQSize
            self.moveActionState = MoveActionState.MOVE

        else:
            # create new parentQSize
            self.moveActionState = MoveActionState.CREATE
            qrect = QRect(pos, pos)
            self._selectionArea.set_qrect(qrect)
        # TODO: chanege relative position
        self._startPosition = pos

    def mouseMove(self, pos):
        """
        :param pos: QPoint, pressed position
        :return:
        """
        if self.moveActionState == MoveActionState.MOVE:
            movedAmount = pos - self._startPosition
            self._selectionArea.move(movedAmount)
            self._startPosition = pos


        elif self.moveActionState == MoveActionState.CREATE or self.moveActionState == MoveActionState.RESIZE:
            # clipping
            pos.setX(min(max(pos.x(), 0), self.parentWidth))
            pos.setY(min(max(pos.y(), 0), self.parentHeight))

            qrect = QRect(self._startPosition, pos).normalized()
            self._selectionArea.set_qrect(qrect)

    def mouseRelease(self):
        self._startPosition = QPoint(0, 0)