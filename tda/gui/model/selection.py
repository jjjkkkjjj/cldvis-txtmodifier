from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

import numpy as np

from .geometry import Rect, Polygon, Vertexes
from ..widgets.eveUtils import MoveActionState, PredictionMode

class SelectionManager(object):
    area: Vertexes
    def __init__(self):
        self._selectionImageArea = Rect(np.zeros(shape=(2, 2)))
        self._selectionTableArea = Polygon(np.zeros(shape=(0, 2)))

        self.predictionMode = PredictionMode.IMAGE
        self.moveActionState = MoveActionState.CREATE
        self._startPosition = QPoint(0, 0)

    @property
    def area(self) -> Vertexes:
        if self.predictionMode == PredictionMode.IMAGE:
            return self._selectionImageArea
        elif self.predictionMode == PredictionMode.TABLE:
            return self._selectionTableArea

    @property
    def width(self):
        if self.predictionMode == PredictionMode.IMAGE:
            return self._selectionImageArea.width
        elif self.predictionMode == PredictionMode.TABLE:
            return self._selectionTableArea.boundingRectWidth
    @property
    def height(self):
        if self.predictionMode == PredictionMode.IMAGE:
            return self._selectionImageArea.height
        elif self.predictionMode == PredictionMode.TABLE:
            return self._selectionTableArea.boundingRectHeight

    @property
    def parentQSize(self):
        return self.area.parentQSize
    @property
    def parentWidth(self):
        return self.area.parentWidth
    @property
    def parentHeight(self):
        return self.area.parentHeight

    def set_selectPos(self, pos):
        self.area.set_selectPos(pos)

    def mousePress(self, parentSize, pos):
        """
        :param parentSize: QSize, the parentQSize
        :param pos: QPoint, pressed position
        :return:
        """
        area: Vertexes = self.area
        # set parentQSize and position
        area.set_parentVals(parentQSize=parentSize)
        area.set_selectPos(pos)
        area.show()

        # TODO: chanege relative position
        self._startPosition = pos

        if self.predictionMode == PredictionMode.IMAGE:
            if area.isSelectedPoint:
                # if pressed position is edge
                # expand or shrink parentQSize
                self.moveActionState = MoveActionState.RESIZE
                # [tl, tr, br, bl] -> [br, bl, tl, tr]
                diagIndex = [2, 3, 0, 1]
                diagPos = self._selectionImageArea.qpoints[diagIndex[self._selectionImageArea.selectedPointIndex]]
                self._startPosition = diagPos
                return

            if self._selectionImageArea.isSelectedRect:
                # if pressed position is contained in parentQSize
                # move the parentQSize
                self.moveActionState = MoveActionState.MOVE

            else:
                # create new parentQSize
                self.moveActionState = MoveActionState.CREATE
                qrect = QRect(pos, pos)
                self._selectionImageArea.set_qrect(qrect)

        elif self.predictionMode == PredictionMode.TABLE:
            if self._selectionTableArea.isSelectedPolygon:
                # if pressed position is contained in parentQSize
                # move the parentQSize
                self.moveActionState = MoveActionState.MOVE

            else:
                # create new parentQSize
                self.moveActionState = MoveActionState.CREATE
                self._selectionTableArea.append(pos)


    def mouseMove(self, pos):
        """
        :param pos: QPoint, pressed position
        :return:
        """
        area = self.area
        if self.moveActionState == MoveActionState.MOVE:
            movedAmount = pos - self._startPosition
            area.move(movedAmount)
            self._startPosition = pos
            return

        if self.moveActionState == MoveActionState.CREATE or self.moveActionState == MoveActionState.RESIZE:
            if self.moveActionState.RESIZE:
                # for changing selected Point
                area.set_selectPos(pos)
            # clipping
            pos.setX(min(max(pos.x(), 0), self.parentWidth))
            pos.setY(min(max(pos.y(), 0), self.parentHeight))

        if self.predictionMode == PredictionMode.IMAGE:
            qrect = QRect(self._startPosition, pos).normalized()
            self._selectionImageArea.set_qrect(qrect)

        elif self.predictionMode == PredictionMode.TABLE:
            self._selectionTableArea.move_qpoint(-1, pos)

    def mouseRelease(self):
        if self.moveActionState.RESIZE:
            self._selectionImageArea.deselect()
        self._startPosition = QPoint(0, 0)