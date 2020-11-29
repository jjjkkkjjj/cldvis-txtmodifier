from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

import numpy as np

class Vertexes(object):

    def __init__(self, points, area, offset):
        """
        :param points: 2(top-left, bottom-right) list of list(2d=(x,y)), Note that these points are in percentage
        :param area: QSize
        :param offset: QPoint
        """
        self.points_percent = np.array(points)
        self.area = area
        self.offset = offset

        self._selected_vertex_index = -1  # -1 if vertices are no selected

        # point radius
        self._point_r = 8

        # color
        self.green = QColor(0, 255, 0, int(255 * 0.8))
        self.red = QColor(255, 0, 0, int(255 * 0.8))
        self.light_green = QColor(0, 255, 0, int(255 * 0.4))
        self.transparency = QColor(0, 255, 0, int(255 * 0))

    @property
    def points_number(self):
        return self.points_percent.shape[0]

    @property
    def isSelectedPoint(self):
        return self._selected_vertex_index != -1
    @property
    def selectedPointIndex(self):
        if self.isSelectedPoint:
            return self._selected_vertex_index
        else:
            return None

    @property
    def selectedPoint(self):
        raise NotImplementedError()

    @property
    def parentWidth(self):
        return self.area.width()
    @property
    def parentHeight(self):
        return self.area.height()

    @property
    def offset_x(self):
        return self.offset.x()
    @property
    def offset_y(self):
        return self.offset.y()

    @property
    def x(self):
        return self.points_percent[:, 0]
    @property
    def y(self):
        return self.points_percent[:, 1]


    def paint(self, painter):
        ### draw edge point ###
        # pen
        pen = QPen(self.transparency)  # transparent
        pen.setWidth(0)

        # brush
        brush = QBrush(self.green, Qt.SolidPattern)
        # set
        painter.setPen(pen)
        painter.setBrush(brush)
        for qpoint in self.qpolygon:
            # drawEllipse(center, rx, ry)
            painter.drawEllipse(qpoint, self._point_r, self._point_r)

        # if selected
        if self.isSelectedPoint:
            # pen
            pen = QPen(self.transparency)  # transparent
            pen.setWidth(0)

            # brush
            brush = QBrush(self.red, Qt.SolidPattern)
            # set
            painter.setPen(pen)
            painter.setBrush(brush)
            painter.drawEllipse(self.selectedPoint, self._point_r, self._point_r)


class Rect(Vertexes):
    def __init__(self, points, area, offset):
        """
        :param points: 2(top-left, bottom-right) list of list(2d=(x,y)), Note that these points are in percentage
        :param area: QSize
        :param offset: QPoint
        """
        assert np.array(points) == (2, 2), "shape must be (2=(tl, br), 2=(x, y))"
        # append top-right and bottom-left
        points.insert(1, [points[0, 0], points[1, 1]])  # top-right
        points.insert(3, [points[1, 0], points[0, 1]])  # bottom-left

        super().__init__(points, area, offset)
        self.set_qrect(area, offset)

        self._isSelectedRect = False


    def gen_qrectPoints(self):
        yield self._qrect.topLeft()
        yield self._qrect.topRight()
        yield self._qrect.bottomRight()
        yield self._qrect.bottomLeft()

    @property
    def selectedPoint(self):
        if self.isSelectedPoint:
            return list(self.gen_qrectPoints())[self._selected_vertex_index]
        else:
            return None

    @property
    def isSelectedRect(self):
        return self._isSelectedRect

    def set_qrect(self, area=None, offset=None):
        if area:
            self.area = area
        if offset:
            self.offset = offset


        points = self.points_percent.copy()
        # note that points = (tl, tr, br, bl)
        points[:, 0] *= self.parentWidth
        points[:, 1] *= self.parentHeight

        scaled_qrect = QRect(QPoint(points[0, 0], points[0, 1]),
                             QPoint(points[2, 0], points[2, 1]))

        self._qrect = scaled_qrect.translated(self.offset)
        return self

    def set_selectPos(self, pos):
        """
        :param pos: QPoint or None
        :return:
        """
        # note that contains function returns true if passed pos includes vertex only
        if pos:
            # check whether to contain point first
            self._selected_vertex_index = -1
            for i, point in enumerate(self.gen_qrectPoints()):
                # QRect constructs a rectangle with the given topLeft corner and the given size.
                if QRect(point - QPoint(self._point_r / 2, self._point_r / 2),
                         QSize(self._point_r * 2, self._point_r * 2)).contains(pos):
                    self._selected_vertex_index = i

            self._isSelectedRect = self._qrect.contains(pos) or self.isSelectedPoint


        else:
            self._selected_vertex_index = -1
            self._isSelectedRect = False
        return self._isSelectedRect

    def paint(self, painter):
        ### draw polygon ###
        # pen
        pen = QPen(self.green)
        pen.setWidth(6)

        # brush
        if self.isSelectedRect:
            brush = QBrush(self.light_green, Qt.SolidPattern)
        else:
            # transparent
            brush = QBrush(self.transparency)
        # set
        painter.setPen(pen)
        painter.setBrush(brush)

        painter.drawRect(self._qrect)

        super().paint(painter)

    def duplicateMe(self):
        newpoints_percent = self.points_percent.copy()
        newpoints_percent[:, 0] += 10 / self.parentWidth
        newpoints_percent[:, 1] += 10 / self.parentHeight
        return Polygon(newpoints_percent[::2], self.area, self.offset)

class Polygon(Vertexes):
    def __init__(self, points, area, offset):
        """
        :param points: list of list(2d=(x,y)), Note that these points are in percentage
        :param area: QSize
        :param offset: QPoint
        """
        super().__init__(points, area, offset)
        self.set_qpolygon(area, offset)

        self._isSelectedPolygon = False

    @property
    def qpolygon(self):
        """
        return scaled qpolygon. In other words, return qpolygon to fit pixmap.
        :return:
        """
        return self._qpolygon


    @property
    def selectedPoint(self):
        if self.isSelectedPoint:
            return self._qpolygon.value(self._selected_vertex_index)
        else:
            return None

    @property
    def isSelectedPolygon(self):
        return self._isSelectedPolygon

    def set_selectPos(self, pos):
        """
        :param pos: QPoint or None
        :return:
        """
        # note that contains function returns true if passed pos includes vertex only
        if pos:
            # check whether to contain point first
            self._selected_vertex_index = -1
            for i, point in enumerate(self._qpolygon):
                # QRect constructs a rectangle with the given topLeft corner and the given size.
                if QRect(point - QPoint(self._point_r / 2, self._point_r / 2),
                         QSize(self._point_r * 2, self._point_r * 2)).contains(pos):
                    self._selected_vertex_index = i

            self._isSelectedPolygon = self._qpolygon.containsPoint(pos, Qt.OddEvenFill) or self.isSelectedPoint


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
        points[:, 0] *= self.parentWidth
        points[:, 1] *= self.parentHeight
        for i in range(self.points_number):
            scaled_qpolygon.append(QPoint(points[i, 0], points[i, 1]))

        self._qpolygon = scaled_qpolygon.translated(self.offset)
        return self


    def paint(self, painter):
        ### draw polygon ###
        # pen
        pen = QPen(self.green)
        pen.setWidth(6)

        # brush
        if self.isSelectedPolygon:
            brush = QBrush(self.light_green, Qt.SolidPattern)
        else:
            # transparent
            brush = QBrush(self.transparency)
        # set
        painter.setPen(pen)
        painter.setBrush(brush)

        painter.drawPolygon(self._qpolygon)

        super().paint(painter)

    def duplicateMe(self):
        newpoints_percent = self.points_percent.copy()
        newpoints_percent[:, 0] += 10 / self.parentWidth
        newpoints_percent[:, 1] += 10 / self.parentHeight
        return Polygon(newpoints_percent, self.area, self.offset)