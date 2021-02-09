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

    def __init__(self, percent_pts, parentSize=QSize(0, 0), offset=QPoint(0, 0)):
        """
        :param percent_pts: array-like, shape=(n, 2). Note that these points are in percentage
        :param parentSize: QSize
        :param offset: QPoint
        """
        super().__init__()

        self.percent_points = np.array(percent_pts)
        self.parentSize = parentSize
        self.offset = offset

    @property
    def points_number(self):
        return self.percent_points.shape[0]

    @property
    def parentWidth(self):
        return self.parentSize.width()
    @property
    def parentHeight(self):
        return self.parentSize.height()

    @property
    def offset_x(self):
        return self.offset.x()
    @property
    def offset_y(self):
        return self.offset.y()

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

    def gen_qpoints(self):
        x, y = self.x, self.y
        for i in range(self.points_number):
            yield QPoint(x[i], y[i])