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
        self._selected_index = -1 # -1 if polygon is not selected
        # attr: offset is QPoint!
        self.offset = QPoint(offset[0], offset[1])

    def set_qpolygons(self, area=None, offset=None):
        for i, polygon in enumerate(self._polygons):
            self._polygons[i] = polygon.set_qpolygon(area, offset)

    def set_select(self, pos):
        # all of polygons are reset selected variable first
        for polygon in self._polygons:
            polygon.set_select(None)

        for i, polygon in reversed(list(enumerate(self._polygons))):
            if polygon.set_select(pos):
                self._selected_index = i
                return
        # All of polygons are not selected
        self._selected_index = -1

    @property
    def offset_x(self):
        return self.offset.x()
    @property
    def offset_y(self):
        return self.offset.y()

    @property
    def selected_polygon(self):
        if self.isExistSelectedPolygon:
            return self._polygons[self._selected_index]
        else:
            return None
    @property
    def isExistSelectedPolygon(self):
        return self._selected_index != -1
    @property
    def isExistSelectedPoint(self):
        if self.isExistSelectedPolygon:
            return self.selected_polygon.isSelectedPoint
        else:
            return False

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
        self.set_qpolygon(area, offset)
        self._selected_vertex_index = -1 # -1 if vertices are no selected
        self._isSelectedPolygon = False

        self._point_r = 8

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
    @property
    def isSelectedPoint(self):
        return self._selected_vertex_index != -1
    @property
    def selectedPoint(self):
        if self.isSelectedPoint:
            return self._qpolygon.value(self._selected_vertex_index)
        else:
            return None
    @property
    def isSelectedPolygon(self):
        return self._isSelectedPolygon
    
    
    def set_select(self, pos):
        """
        :param pos: QPoint or None
        :return:
        """
        # note that contains function returns true if passed pos includes vertex only
        if pos:
            self._isSelectedPolygon = self._qpolygon.containsPoint(pos, Qt.OddEvenFill)
            self._selected_vertex_index = -1
            if self.isSelectedPolygon:
                for i, point in enumerate(self._qpolygon):
                    # QRect constructs a rectangle with the given topLeft corner and the given size.
                    if QRect(point - QPoint(self._point_r / 2, self._point_r / 2),
                             QSize(self._point_r * 2, self._point_r * 2)).contains(pos):
                        self._selected_vertex_index = i
        else:
            self._selected_vertex_index = -1
            self._isSelectedPolygon = False
        return self._isSelectedPolygon

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

        self._qpolygon = scaled_qpolygon.translated(self.offset)
        return self

    @property
    def x(self):
        return self.points_percent[:, 0]
    @property
    def y(self):
        return self.points_percent[:, 1]
    
    def paint(self, painter):
        green = QColor(0, 255, 0, int(255 * 0.8))
        red = QColor(255, 0, 0, int(255 * 0.8))
        light_green = QColor(0, 255, 0, int(255 * 0.4))
        transparency = QColor(0, 255, 0, int(255 * 0))
        ### draw polygon ###
        # pen
        pen = QPen(green)
        pen.setWidth(6)

        # brush
        if self.isSelectedPolygon:
            brush = QBrush(light_green, Qt.SolidPattern)
        else:
            # transparent
            brush = QBrush(transparency)
        # set
        painter.setPen(pen)
        painter.setBrush(brush)

        painter.drawPolygon(self._qpolygon)

        ### draw edge point ###
        # pen
        pen = QPen(transparency) # transparent
        pen.setWidth(0)

        # brush
        brush = QBrush(green, Qt.SolidPattern)
        # set
        painter.setPen(pen)
        painter.setBrush(brush)
        for qpoint in self.qpolygon:
            # drawEllipse(center, rx, ry)
            painter.drawEllipse(qpoint, self._point_r, self._point_r)

        # if selected
        if self.isSelectedPoint:
            # pen
            pen = QPen(transparency)  # transparent
            pen.setWidth(0)

            # brush
            brush = QBrush(red, Qt.SolidPattern)
            # set
            painter.setPen(pen)
            painter.setBrush(brush)
            painter.drawEllipse(self.selectedPoint, self._point_r, self._point_r)