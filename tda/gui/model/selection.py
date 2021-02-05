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
    def width(self):
        return self._selectionArea.area.parentWidth
    @property
    def height(self):
        return self._selectionArea.area.parentHeight

    def mousePress(self, area, pos):
        """
        :param area: QSize, the parentSize
        :param pos: QPoint, pressed position
        :return:
        """
        # set parentSize and position
        self._selectionArea.set_qrect(area=area)
        self._selectionArea.set_selectPos(pos)

        if self._selectionArea.isSelectedPoint:
            # if pressed position is edge
            # expand or shrink parentSize
            self.moveActionState = MoveActionState.RESIZE

        elif self._selectionArea.isSelectedRect:
            # if pressed position is contained in parentSize
            # move the parentSize
            self.moveActionState = MoveActionState.MOVE
        else:
            # create new parentSize
            self.moveActionState = MoveActionState.CREATE
        self._startPosition = pos

    def mouseMove(self, pos):

        if self.moveActionState == MoveActionState.MOVE:
            movedAmount = pos - self._startPosition
            self._selectionArea.move(movedAmount)

        elif self.moveActionState == MoveActionState.CREATE or self.moveActionState == MoveActionState.RESIZE:

            QRect(self._startPosition, pos)