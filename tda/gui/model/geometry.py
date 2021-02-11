from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

import numpy as np

from .percent_geometry import PercentVertexes

class Vertexes(PercentVertexes):

    def __init__(self, points, parentQSize=QSize(0, 0), offsetQPoint=QPoint(0, 0)):
        """
        :param points: list(n) of list(2d=(x,y)), Note that these points are percent representation
        :param parentQSize: QSize, the parent widget's parentQSize
        :param offsetQPoint: QPoint, the _offsetQPoint coordinates to parent widget
        """
        super().__init__(points, parentQSize, offsetQPoint)

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
        if self.isSelectedPoint:
            return self.qpoints[self._selected_vertex_index]
        else:
            return None

    def deselect(self):
        self._selected_vertex_index = -1

    def set_selectPos(self, pos):
        # note that contains function returns true if passed pos includes vertex only
        if pos:
            # check whether to contain point first
            self._selected_vertex_index = -1
            for i, point in enumerate(self.qpoints):
                # QRect constructs a rectangle with the given topLeft corner and the given parentQSize.
                if QRect(point - QPoint(self._point_r / 2, self._point_r / 2),
                         QSize(self._point_r * 2, self._point_r * 2)).contains(pos):
                    self._selected_vertex_index = i
        else:
            self._selected_vertex_index = -1

        return self.isSelectedPoint

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


class Rect(Vertexes):
    def __init__(self, points, parentQSize=QSize(0, 0), offsetQPoint=QPoint(0, 0)):
        """
        :param points: list(n) of list(2d=(x,y)), Note that these points are percent representation
        :param parentQSize: QSize, the parent widget's parentQSize
        :param offsetQPoint: QPoint, the _offsetQPoint coordinates to parent widget
        """
        _points = np.array(points)
        assert _points.shape == (2, 2), "shape must be (2=(tl, br), 2=(x, y))"
        # append top-right and bottom-left
        _points = np.insert(_points, 1, [points[0, 0], points[1, 1]], axis=0) # top-right
        _points = np.insert(_points, 3, [points[1, 0], points[0, 1]], axis=0)  # bottom-left

        super().__init__(_points, parentQSize, offsetQPoint)

        self._isSelectedRect = False

    @property
    def qrect(self):
        """
        :return: QRect
        """
        # note that order is (tl, tr, br, bl)
        qpoints = self.qpoints
        return QRect(qpoints[0], qpoints[2])

    def set_qrect(self, qrect):
        qpts = qrect.topLeft(), qrect.topRight(), qrect.bottomRight(),  qrect.bottomLeft()
        new_percent_pts = np.array(tuple((float(qpt.x())/self.parentWidth, float(qpt.y())/self.parentHeight) for qpt in qpts))
        self.set_percent_points(new_percent_pts)

    @property
    def width(self):
        return self.qrect.width()
    @property
    def height(self):
        return self.qrect.height()
    @property
    def qsize(self):
        return self.qrect.size()
    @property
    def topLeft(self):
        return self.qpoints[0]
    @property
    def topRight(self):
        return self.qpoints[1]
    @property
    def bottomRight(self):
        return self.qpoints[2]
    @property
    def bottomLeft(self):
        return self.qpoints[3]

    @property
    def isSelectedRect(self):
        return self._isSelectedRect

    def _update_percent_pts(self):
        if self.parentWidth > 0 and self.parentHeight > 0:
            new_percent_pts = np.array(tuple(
                (float(pt.x()) / self.parentWidth, float(pt.y()) / self.parentHeight) for pt in self.gen_qpoints()))
            self.set_percent_points(new_percent_pts)

    def set_parentVals(self, parentQSize=None, offsetQPoint=None):
        super().set_parentVals(parentQSize, offsetQPoint)
        if parentQSize is not None or offsetQPoint is not None:
            self._update_percent_pts()


    def set_selectPos(self, pos):
        """
        :param pos: QPoint or None
        :return:
        """
        super().set_selectPos(pos)
        self._isSelectedRect = self.qrect.contains(pos) or self.isSelectedPoint
        return self.isSelectedRect


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

        painter.drawRect(self.qrect)

        super().paint(painter)

    def move(self, movedAmount):
        # check moved rect is with in parent
        tl, _, br, _ = self.qpoints
        new_tl, new_br = tl + movedAmount, br + movedAmount

        revertAmount = QPoint(0, 0)
        revertAmount -= QPoint(min(new_tl.x(), 0), min(new_tl.y(), 0))
        revertAmount -= QPoint(max(new_br.x()-self.parentWidth, 0), max(new_br.y()-self.parentHeight, 0))

        super().move(movedAmount + revertAmount)


    def duplicateMe(self):
        newpoints_percent = self.percent_points.copy()
        # slightly moved
        newpoints_percent[:, 0] += 10 / self.parentWidth
        newpoints_percent[:, 1] += 10 / self.parentHeight
        return Rect(newpoints_percent[::2], self.parentQSize, self.offsetQPoint)

class Polygon(Vertexes):
    def __init__(self, points, parentQSize=QSize(0, 0), offsetQPoint=QPoint(0, 0)):
        """
        :param points: list(n) of list(2d=(x,y)), Note that these points are percent representation
        :param parentQSize: QSize, the parent widget's parentQSize
        :param offsetQPoint: QPoint, the _offsetQPoint coordinates to parent widget
        """
        super().__init__(points, parentQSize, offsetQPoint)
        self.set_qpolygon(parentQSize, offsetQPoint)

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
                # QRect constructs a rectangle with the given topLeft corner and the given parentQSize.
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
        newpoints_percent = self._percent_points.copy()
        newpoints_percent[:, 0] += 10 / self.parentWidth
        newpoints_percent[:, 1] += 10 / self.parentHeight
        return Polygon(newpoints_percent, self.parentSize, self.offset)