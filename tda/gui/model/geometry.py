from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

import numpy as np

from .percent_geometry import PercentVertexes
from .paint_utils import *

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
        self.vertex_r = 8
        self.vertex_default_color = Color(border=transparency, fill=green, borderSize=0)
        self.vertex_selected_color = Color(border=transparency, fill=red, borderSize=0)


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
    def selectedQPoint(self):
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
                if QRect(point - QPoint(self.vertex_r / 2, self.vertex_r / 2),
                         QSize(self.vertex_r * 2, self.vertex_r * 2)).contains(pos):
                    self._selected_vertex_index = i
        else:
            self._selected_vertex_index = -1

        return self.isSelectedPoint

    def set_color(self, vertex_default_color=None, vertex_selected_color=None):
        """
        :param vertex_default_color: Color, default color
        :param vertex_selected_color: Color, the color if selected
        :return:
        """
        if vertex_default_color:
            self.vertex_default_color = vertex_default_color
        else:
            self.vertex_default_color = Color(border=transparency, fill=green, borderSize=0)

        if vertex_selected_color:
            self.vertex_selected_color = vertex_selected_color
        else:
            self.vertex_selected_color = Color(border=transparency, fill=red, borderSize=0)


    def paint(self, painter):
        if not self.isShow:
            return
        ### draw edge point ###
        PaintMaster.set_pen_brush(painter, self.vertex_default_color)
        for qpoint in self.gen_qpoints():
            # drawEllipse(center, rx, ry)
            painter.drawEllipse(qpoint, self.vertex_r, self.vertex_r)

        # if selected
        if self.isSelectedPoint:
            PaintMaster.set_pen_brush(painter, self.vertex_selected_color)
            painter.drawEllipse(self.selectedQPoint, self.vertex_r, self.vertex_r)

    def move_qpoint(self, index, qpt):
        percent_pt = np.array((float(qpt.x()) / self.parentWidth, float(qpt.y()) / self.parentHeight))
        self.move_percent_point(index, percent_pt)

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

        self.rect_default_color = Color(border=green, fill=transparency)
        self.rect_selected_color = Color(border=green, fill=light_green)

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


    def set_selectPos(self, pos):
        """
        :param pos: QPoint or None
        :return:
        """
        super().set_selectPos(pos)
        if pos:
            self._isSelectedRect = self.qrect.contains(pos) or self.isSelectedPoint
        else:
            self._isSelectedRect = False
        return self.isSelectedRect

    def set_color(self, rect_default_color=None, rect_selected_color=None, **kwargs):
        """
        :param vertex_default_color: Color, default color
        :param vertex_selected_color: Color, the color if selected
        :param rect_default_color: QColor, default color
        :param rect_selected_color: QColor, the color if selected
        :return:
        """
        super().set_color(**kwargs)
        if rect_default_color:
            self.rect_default_color = rect_default_color
        else:
            self.rect_default_color = Color(border=green, fill=transparency)

        if rect_selected_color:
            self.rect_selected_color = rect_selected_color
        else:
            self.rect_selected_color = Color(border=green, fill=light_green)


    def paint(self, painter):
        if not self.isShow:
            return
        ### draw annotation ###
        if self.isSelectedRect:
            PaintMaster.set_pen_brush(painter, self.rect_selected_color)
        else:
            PaintMaster.set_pen_brush(painter, self.rect_default_color)

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
    def __init__(self, points, parentQSize=QSize(0, 0), offsetQPoint=QPoint(0, 0), maximum_points_number=None):
        """
        :param points: list(n) of list(2d=(x,y)), Note that these points are percent representation
        :param parentQSize: QSize, the parent widget's parentQSize
        :param offsetQPoint: QPoint, the _offsetQPoint coordinates to parent widget
        :param maximum_points_number: int or None
        """
        super().__init__(points, parentQSize, offsetQPoint)

        self._isSelectedPolygon = False
        self.maximum_points_number =maximum_points_number

        self.poly_default_color = Color(border=green, fill=transparency)
        self.poly_selected_color = Color(border=green, fill=light_green)

    @property
    def isAppendable(self):
        return self.maximum_points_number is None or self.points_number < self.maximum_points_number

    @property
    def qpolygon(self):
        """
        return scaled qpolygon. In other words, return qpolygon to fit pixmap.
        :return:
        """
        qpolygon = QPolygon()
        for qpt in self.gen_qpoints():
            qpolygon.append(qpt)
        return qpolygon

    def set_qpolygon(self, qpolygon):
        new_percent_pts = np.array(tuple((float(qpt.x()) / self.parentWidth, float(qpt.y()) / self.parentHeight) for qpt in qpolygon))
        self.set_percent_points(new_percent_pts)

    def append(self, qpt):
        if self.isAppendable:
            self.append_percent_pt(np.array((float(qpt.x()) / self.parentWidth, float(qpt.y()) / self.parentHeight)))

    @property
    def boundingRectWidth(self):
        return self.qpolygon.boundingRect().width()
    @property
    def boundingRectHeight(self):
        return self.qpolygon.boundingRect().height()

    @property
    def selectedQPoint(self):
        if self.isSelectedPoint:
            return self.qpoints[self._selected_vertex_index]
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
        super().set_selectPos(pos)
        if pos:
            self._isSelectedPolygon = self.qpolygon.containsPoint(pos, Qt.OddEvenFill) or self.isSelectedPoint
        else:
            self._isSelectedPolygon = False
        return self.isSelectedPolygon

    def set_color(self, poly_default_color=None, poly_selected_color=None, **kwargs):
        """
        :param vertex_default_color: Color, default color
        :param vertex_selected_color: Color, the color if selected
        :param poly_default_color: QColor, default color
        :param poly_selected_color: QColor, the color if selected
        :return:
        """
        super().set_color(**kwargs)
        if poly_default_color:
            self.poly_default_color = poly_default_color
        else:
            self.poly_default_color = Color(border=green, fill=transparency)

        if poly_selected_color:
            self.poly_selected_color = poly_selected_color
        else:
            self.poly_selected_color = Color(border=green, fill=light_green)


    def paint(self, painter):
        if not self.isShow:
            return

        ### draw annotation ###
        if self.isSelectedPolygon:
            PaintMaster.set_pen_brush(painter, self.poly_selected_color)
        else:
            PaintMaster.set_pen_brush(painter, self.poly_default_color)

        painter.drawPolygon(self.qpolygon)

        super().paint(painter)

    def duplicateMe(self):
        newpoints_percent = self._percent_points.copy()
        newpoints_percent[:, 0] += 10 / self.parentWidth
        newpoints_percent[:, 1] += 10 / self.parentHeight
        return Polygon(newpoints_percent, self.parentQSize, self.offsetQPoint)