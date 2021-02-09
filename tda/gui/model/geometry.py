from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

import numpy as np

from .percent_geometry import PercentVertexes

class Vertexes(PercentVertexes):

    def __init__(self, points, parentSize=QSize(0, 0), offset=QPoint(0, 0)):
        """
        :param points: list(n) of list(2d=(x,y)), Note that these points are percent representation
        :param parentSize: QSize, the parent widget's size
        :param offset: QPoint, the offset coordinates to parent widget
        """
        super().__init__(points, parentSize, offset)

        self._selected_vertex_index = -1  # -1 if vertices are no selected

        # point radius
        self._point_r = 8


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


    def paint(self, painter):
        if not self.isShow:
            return
        ### draw edge point ###
        # pen
        pen = QPen(self.transparency)  # transparent
        pen.setWidth(0)

        # brush
        brush = QBrush(self.green, Qt.SolidPattern)
        # set
        painter.setPen(pen)
        painter.setBrush(brush)
        for qpoint in self.gen_qpoints():
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

    def move(self, movedAmount):
        """
        :param movedAmount: QPoint, move amount. Note that this position is represented as absolute coordinates system in parent widget
        :return:
        """
        new_dx_percent = movedAmount.x() / self.parentWidth
        new_dy_percent = movedAmount.y() / self.parentHeight
        self.percent_points += np.array(((new_dx_percent, new_dy_percent)))


class Rect(Vertexes):
    def __init__(self, points, parentSize=QSize(0, 0), offset=QPoint(0, 0)):
        """
        :param points: list(n) of list(2d=(x,y)), Note that these points are percent representation
        :param parentSize: QSize, the parent widget's size
        :param offset: QPoint, the offset coordinates to parent widget
        """
        _points = np.array(points)
        assert _points.shape == (2, 2), "shape must be (2=(tl, br), 2=(x, y))"
        # append top-right and bottom-left
        _points = np.insert(_points, 1, [points[0, 0], points[1, 1]], axis=0) # top-right
        _points = np.insert(_points, 3, [points[1, 0], points[0, 1]], axis=0)  # bottom-left

        super().__init__(_points, parentSize, offset)
        self.set_qrect(parentSize, offset)

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

    def set_qrect(self, parentSize=None, offset=None):
        """
        :param parentSize: QSize, the parent widget's size
        :param offset: QPoint, the offset coordinates to parent widget
        """
        if parentSize:
            self.parentSize = parentSize
        if offset:
            self.offset = offset


        points = self.percent_points.copy()
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
                # QRect constructs a rectangle with the given topLeft corner and the given parentSize.
                if QRect(point - QPoint(self._point_r / 2, self._point_r / 2),
                         QSize(self._point_r * 2, self._point_r * 2)).contains(pos):
                    self._selected_vertex_index = i

            self._isSelectedRect = self._qrect.contains(pos) or self.isSelectedPoint


        else:
            self._selected_vertex_index = -1
            self._isSelectedRect = False
        return self._isSelectedRect

    def paint(self, painter):
        if not self.isShow:
            return
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
        newpoints_percent = self.percent_points.copy()
        # slightly moved
        newpoints_percent[:, 0] += 10 / self.parentWidth
        newpoints_percent[:, 1] += 10 / self.parentHeight
        return Polygon(newpoints_percent[::2], self.parentSize, self.offset)

class Polygon(Vertexes):
    def __init__(self, points, parentSize=QSize(0, 0), offset=QPoint(0, 0)):
        """
        :param points: list(n) of list(2d=(x,y)), Note that these points are percent representation
        :param parentSize: QSize, the parent widget's size
        :param offset: QPoint, the offset coordinates to parent widget
        """
        super().__init__(points, parentSize, offset)
        self.set_qpolygon(parentSize, offset)

        self._isSelectedPolygon = False

    @classmethod
    def fromQPolygon(cls):
        return cls()

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
                # QRect constructs a rectangle with the given topLeft corner and the given parentSize.
                if QRect(point - QPoint(self._point_r / 2, self._point_r / 2),
                         QSize(self._point_r * 2, self._point_r * 2)).contains(pos):
                    self._selected_vertex_index = i

            self._isSelectedPolygon = self._qpolygon.containsPoint(pos, Qt.OddEvenFill) or self.isSelectedPoint


        else:
            self._selected_vertex_index = -1
            self._isSelectedPolygon = False
        return self._isSelectedPolygon

    def set_qpolygon(self, parentSize=None, offset=None):
        if parentSize:
            self.parentSize = parentSize
        if offset:
            self.offset = offset

        qpolygon = QPolygon()

        for qpoint in self.gen_qpoints():
            qpolygon.append(qpoint)

        self._qpolygon = qpolygon.translated(self.offset)
        return self


    def paint(self, painter):
        if not self.isShow:
            return

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
        newpoints_percent = self.percent_points.copy()
        newpoints_percent[:, 0] += 10 / self.parentWidth
        newpoints_percent[:, 1] += 10 / self.parentHeight
        return Polygon(newpoints_percent, self.parentSize, self.offset)