from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

import numpy as np

from .funcs import sort_clockwise
from .paint import *

class GeoBase(object):
    def __init__(self):
        self._isShow = False

    @property
    def isShow(self):
        return self._isShow

    def show(self):
        self._isShow = True

    def hide(self):
        self._isShow = False

class PercentVertexes(GeoBase):

    def __init__(self, percent_pts, parentQSize=QSize(0, 0), offsetQPoint=QPoint(0, 0)):
        """
        :param percent_pts: array-like, shape=(n, 2). Note that these points are in percentage
        :param parentQSize: QSize
        :param offsetQPoint: QPoint
        """
        super().__init__()
        percent_pts = np.array(percent_pts)
        self._percent_points = sort_clockwise(percent_pts) if percent_pts.size > 0 else percent_pts
        self._parentQSize = parentQSize
        self._offsetQPoint = offsetQPoint

    def set_parentVals(self, parentQSize=None, offsetQPoint=None):
        """
        :param parentQSize: QSize
        :param offsetQPoint: QPoint
        """
        if parentQSize:
            self._parentQSize = parentQSize
        if offsetQPoint:
            self._offsetQPoint = offsetQPoint


    def set_percent_points(self, percent_pts=None):
        """
        :param percent_pts: array-like, shape=(n, 2). Note that these points are in percentage
        """
        if percent_pts is not None:
            self._percent_points = sort_clockwise(percent_pts) if percent_pts.size > 0 else percent_pts

    def append_percent_pt(self, percent_pt):
        new_percent_pts = np.append(self._percent_points, percent_pt).reshape(-1, 2)
        self._percent_points = sort_clockwise(new_percent_pts)

    @property
    def points_number(self):
        return self._percent_points.shape[0]

    @property
    def percent_points(self):
        return self._percent_points
    @property
    def points_number(self):
        return self._percent_points.shape[0]

    @property
    def parentQSize(self):
        return self._parentQSize
    @property
    def parentWidth(self):
        return self.parentQSize.width()
    @property
    def parentHeight(self):
        return self.parentQSize.height()

    @property
    def offsetQPoint(self):
        """
        :return: offsetQPoint QPoint
        """
        return self._offsetQPoint
    @property
    def offset_x(self):
        return self.offsetQPoint.x()
    @property
    def offset_y(self):
        return self.offsetQPoint.y()

    @property
    def percent_x(self):
        return self.percent_points[:, 0]
    @property
    def percent_y(self):
        return self.percent_points[:, 1]

    @property
    def x(self):
        return self.percent_x * self.parentWidth
    @property
    def y(self):
        return self.percent_y * self.parentHeight

    @property
    def qpoints(self):
        """
        :return: tuple of QPoints
        """
        return tuple(self.gen_qpoints())

    def gen_qpoints(self):
        x, y = self.x, self.y
        for i in range(self.points_number):
            yield QPoint(x[i], y[i]) + self.offsetQPoint

    def move(self, movedAmount):
        """
        :param movedAmount: QPoint, move amount. Note that this position is represented as absolute coordinates system in parent widget
        :return:
        """
        new_dx_percent = float(movedAmount.x()) / self.parentWidth
        new_dy_percent = float(movedAmount.y()) / self.parentHeight
        self._percent_points += np.array((new_dx_percent, new_dy_percent)).reshape((1, 2))

    def move_percent_point(self, index, percent_pt):
        self._percent_points[index] = percent_pt

class Vertexes(PercentVertexes):

    def __init__(self, points=np.zeros(shape=(0, 2)), parentQSize=QSize(0, 0), offsetQPoint=QPoint(0, 0), maximum_points_number=None):
        """
        :param points: list(n) of list(2d=(x,y)), Note that these points are percent representation
        :param parentQSize: QSize, the parent widget's parentQSize
        :param offsetQPoint: QPoint, the _offsetQPoint coordinates to parent widget
        :param maximum_points_number: int or None
        """
        super().__init__(points, parentQSize, offsetQPoint)

        self._selected_vertex_index = -1  # -1 if vertices are no selected

        self.maximum_points_number = maximum_points_number
        _points = np.array(points)
        if self.maximum_points_number and _points.shape[0] > self.maximum_points_number:
            raise ValueError('points number: {} is over maximum_points_numner: {}'.format(_points.shape[0], self.maximum_points_number))

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

    @property
    def isAppendable(self):
        return self.maximum_points_number is None or self.points_number < self.maximum_points_number

    def append(self, qpt):
        if self.isAppendable:
            self.append_percent_pt(np.array((float(qpt.x()) / self.parentWidth, float(qpt.y()) / self.parentHeight)))

    def clear(self):
        self.set_percent_points(np.zeros(shape=(0, 2)))

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

    @property
    def isDrawablePoints(self):
        return self.points_number > 0

    def paint(self, painter):
        if not self.isShow:
            return

        if self.isDrawablePoints:
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
    def __init__(self, points=np.zeros(shape=(0, 2)), parentQSize=QSize(0, 0), offsetQPoint=QPoint(0, 0)):
        """
        :param points: list(2) of list(2d=(x,y)), (topleft, bottomright) Note that these points are percent representation
        :param parentQSize: QSize, the parent widget's parentQSize
        :param offsetQPoint: QPoint, the _offsetQPoint coordinates to parent widget
        :param maximum_points_number: int or None
        """
        _points = np.array(points)
        if _points.shape[1] != 2 or _points.shape[0] >= 3:
            raise ValueError("shape must be (0 or 1 or 2=(tl, br), 2=(x, y))")

        if _points.shape[0] > 0:
            # 1 or 2
            if _points.shape[0] == 1:# shape = (1, 2)
                _points = np.broadcast_to(_points, shape=(2, 2))
            _pts = _points.copy()
            # append top-right and bottom-left
            _points = np.insert(_points, 1, [_pts[0, 0], _pts[1, 1]], axis=0)  # top-right
            _points = np.insert(_points, 3, [_pts[1, 0], _pts[0, 1]], axis=0)  # bottom-left

        super().__init__(_points, parentQSize, offsetQPoint, maximum_points_number=4)

        self._isSelectedRect = False

        self.rect_default_color = Color(border=green, fill=transparency)
        self.rect_selected_color = Color(border=green, fill=light_green)

    @property
    def qrect(self):
        """
        :return: QRect
        """
        if self.points_number < 2:
            return None

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
        if pos and self.isDrawableRect:
            self._isSelectedRect = self.qrect.contains(pos) or self.isSelectedPoint
        else:
            self._isSelectedRect = False
        return self.isSelectedRect

    def set_percent_points(self, percent_pts=None):
        if percent_pts is None:
            return
        if percent_pts.shape[0] == 2:
            percent_pts = sort_clockwise(percent_pts)

            new_percent_pts = percent_pts.copy()
            # append top-right and bottom-left
            new_percent_pts = np.insert(new_percent_pts, 1, [percent_pts[0, 0], percent_pts[1, 1]], axis=0)  # top-right
            new_percent_pts = np.insert(new_percent_pts, 3, [percent_pts[1, 0], percent_pts[0, 1]], axis=0)  # bottom-left

            super().set_percent_points(new_percent_pts)

        elif percent_pts.shape[0] == 0 or percent_pts.shape[0] == 4:
            super().set_percent_points(percent_pts)

        else:
            raise ValueError('percent_pts\' shape must be (2, 2) or (4, 2), but got {}'.format(percent_pts.shape))

    def append(self, qpt):
        qrect = QRect(qpt, qpt)
        self.set_qrect(qrect)

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

    @property
    def isDrawableRect(self):
        return self.points_number == 4

    def paint(self, painter):
        if not self.isShow:
            return

        if self.isDrawableRect:
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
    def __init__(self, points=np.zeros(shape=(0, 2)), parentQSize=QSize(0, 0), offsetQPoint=QPoint(0, 0), maximum_points_number=None):
        """
        :param points: list(n) of list(2d=(x,y)), Note that these points are percent representation
        :param parentQSize: QSize, the parent widget's parentQSize
        :param offsetQPoint: QPoint, the _offsetQPoint coordinates to parent widget
        :param maximum_points_number: int or None
        """
        super().__init__(points, parentQSize, offsetQPoint, maximum_points_number)

        self._isSelectedPolygon = False

        self.poly_default_color = Color(border=green, fill=transparency)
        self.poly_selected_color = Color(border=green, fill=light_green)

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
        if pos and self.isDrawablePolygon:
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

    @property
    def isDrawablePolygon(self):
        return self.points_number >= 2

    def paint(self, painter):
        if not self.isShow:
            return

        if self.isDrawablePolygon:
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

class Annotation(Polygon):
    def __init__(self, baseWidget, points, text, parentQSize, offsetQPoint):
        """
        :param baseWidget: QWidget, the base widget for AnnotaionRubberBand
        :param points: list of list(2d=(x,y)), Note that these points are in percentage
        :param text: str
        :param parentQSize: QSize
        :param offsetQPoint: QPoint
        """
        super().__init__(points, parentQSize, offsetQPoint)
        self.baseWidget = baseWidget
        self.text = text

        self.band = AnnotaionRubberBand(self.text, QRubberBand.Rectangle, parent=baseWidget)
        self.band.setGeometry(self.qpolygon.boundingRect())

        self.vertex_default_color = Color(fill=green)
        self.poly_default_color = Color(border=green, fill=light_green)
        self.vertex_selected_color = Color(fill=red)
        self.poly_selected_color = Color(border=green, fill=transparency)

        self.text_color = Color(border=black)

    def show(self):
        super().show()
        self.band.show()

    def hide(self):
        super().hide()
        self.band.hide()

    def set_percent_points(self, percent_pts=None):
        super().set_percent_points(percent_pts)
        self.band.setGeometry(self.qpolygon.boundingRect())

    def set_parentVals(self, parentQSize=None, offsetQPoint=None):
        super().set_parentVals(parentQSize, offsetQPoint)
        self.band.setGeometry(self.qpolygon.boundingRect())

    def set_selectPos(self, pos):
        if super().set_selectPos(pos):
            # selected
            self.band.isShowText = False
        else:
            self.band.isShowText = True
        return self.isSelectedPolygon

    def duplicateMe(self):
        newpoints_percent = self.percent_points.copy()
        newpoints_percent[:, 0] += 10.0 / self.parentWidth
        newpoints_percent[:, 1] += 10.0 / self.parentHeight
        return Annotation(self.baseWidget, newpoints_percent, self.text, self.parentQSize, self.offsetQPoint)

    def paint(self, painter):
        if not self.isShow:
            return

        # draw area first
        super().paint(painter)

        """
        # draw text is too slow. so do in rubberband instead
        if self.isSelectedPolygon:
            return
        else:
            # draw annotated text later
            PaintMaster.set_pen_brush(painter, self.text_color)

            rect = self.qpolygon.boundingRect()
            factor = rect.width() / painter.fontMetrics().width(self.text + '   ')
            font = painter.font()
            font.setPointSizeF(font.pointSizeF()*factor)
            painter.setFont(font)

            painter.drawText(self.qpolygon.boundingRect(), Qt.AlignCenter, self.text)
            #painter.drawText(QFontMetrics(painter.font()).size(Qt.TextSingleLine, self.text).width(), self.text)
        """

class AnnotaionRubberBand(QRubberBand):
    def __init__(self, text, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.text = text

        self.text_color = Color(border=red)
        self._isShowText = True

    @property
    def isShowText(self):
        return self._isShowText

    @isShowText.setter
    def isShowText(self, val):
        self._isShowText = val

        self.update()

    def paintEvent(self, event):
        if not self.isShowText:
            return
        # draw annotated text
        painter = QPainter(self)
        PaintMaster.set_pen_brush(painter, self.text_color)

        rect = self.rect()
        factor = rect.width() / painter.fontMetrics().width(self.text + '   ')
        font = painter.font()
        font.setPointSizeF(font.pointSizeF() * factor)
        painter.setFont(font)

        painter.drawText(self.rect(), Qt.AlignCenter, self.text)

        # not drawing background at all!!
        # a.k.a. not calling super
        return
