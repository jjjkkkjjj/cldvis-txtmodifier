from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

import numpy as np

class GeoBase(object):
    def __init__(self):
        self._isShow = False

        # color
        self.green = QColor(0, 255, 0, int(255 * 0.8))
        self.red = QColor(255, 0, 0, int(255 * 0.8))
        self.light_green = QColor(0, 255, 0, int(255 * 0.4))
        self.transparency = QColor(0, 255, 0, int(255 * 0))

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

        self._percent_points = np.array(percent_pts)
        self._parentQSize = parentQSize
        self._offsetQPoint = offsetQPoint
        self._moved_points = np.zeros(shape=(1, 2)) # for broadcast

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
            self._percent_points = percent_pts


    @property
    def percent_points(self):
        return self._percent_points + self._moved_points
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
            yield QPoint(x[i], y[i])

    def move(self, movedAmount):
        """
        :param movedAmount: QPoint, move amount. Note that this position is represented as absolute coordinates system in parent widget
        :return:
        """
        new_dx_percent = float(movedAmount.x()) / self.parentWidth
        new_dy_percent = float(movedAmount.y()) / self.parentHeight
        self._moved_points = np.array((new_dx_percent, new_dy_percent)).reshape((1, 2))
        #self._percent_points += np.array((new_dx_percent, new_dy_percent)).reshape((1, 2))

    def moved(self):
        """
        Must be called releaseEvent after moving
        :return:
        """
        self._percent_points += self._moved_points
        self._moved_points = np.zeros(shape=(1, 2)) # for broadcast