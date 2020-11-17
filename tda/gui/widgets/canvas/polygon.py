from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

import numpy as np

class PolygonManager(object):
    def __init__(self, offset):
        """
        :param offset: list(2d=(x,y)), is top-left coordinates of selected rectangle
        """
        super().__init__()

        self._polygons = []
        # attr: offset is QPoint!
        self.offset = QPoint(offset[0], offset[1])

    def set_qpolygons(self, area=None, offset=None):
        for polygon in self._polygons:
            polygon.set_qpolygon(area, offset)

    @property
    def offset_x(self):
        return self.offset.x()
    @property
    def offset_y(self):
        return self.offset.y()

    def refresh(self):
        self._polygons = []

    def insert(self, index, polygon):
        self._polygons.insert(index, polygon)

    def append(self, polygon):
        self._polygons.append(polygon)

    def __len__(self):
        return len(self._polygons)

    def __setitem__(self, index, polygon):
        self._polygons[index] = polygon

    def __getitem__(self, index):
        if not isinstance(index, int):
            raise ValueError('index must be int, but got {}'.format(type(index).__name__))
        return self._polygons[index]

    def __delitem__(self, index):
        if not isinstance(index, int):
            raise ValueError('index must be int, but got {}'.format(type(index).__name__))
        del self._polygons[index]

    def __iter__(self):
        for polygon in self._polygons:
            yield polygon

    def qpolygons(self):
        """
        iterate for qpolygon for each polygon. Yield QPolygon class for each iteration
        :return:
        """
        for polygon in self._polygons:
            yield polygon.qpolygon

    def set_highlight(self, pos):
        pass


class Polygon(object):
    def __init__(self, points, area, offset):
        """
        :param points: list of list(2d=(x,y)), Note that these points are in percentage
        :param area: QSize
        :param offset: QPoint
        """
        self.points_percent = np.array(points) # shape = (*, 2)
        self._qpolygon = self.set_qpolygon(area, offset)

    @property
    def points_number(self):
        return self.points_percent.shape[0]

    @property
    def qpolygon(self):
        """
        return scaled qpolygon. In other words, return qpolygon to fit pixmap.
        :return:
        """
        return self._qpolygon

    @property
    def width(self):
        return self.area.width()
    @property
    def height(self):
        return self.area.height()
    @property
    def offset_x(self):
        return self.offset.x()
    @property
    def offset_y(self):
        return self.offset.y()


    def set_qpolygon(self, area=None, offset=None):
        if area:
            self.area = area
        if offset:
            self.offset = offset

        scaled_qpolygon = QPolygon()
        points = self.points_percent.copy()
        points[:, 0] *= self.width
        points[:, 1] *= self.height
        for i in range(self.points_number):
            scaled_qpolygon.append(QPoint(points[i, 0], points[i, 1]))

        return scaled_qpolygon.translated(self.offset)

    @property
    def x(self):
        return self.points_percent[:, 0]
    @property
    def y(self):
        return self.points_percent[:, 1]
    
    def paint(self, painter):
        pass