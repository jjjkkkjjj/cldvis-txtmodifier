from PySide2.QtGui import *
from PySide2.QtCore import *

black = QColor(0, 0, 0)
green = QColor(0, 255, 0, int(255 * 0.8))
red = QColor(255, 0, 0, int(255 * 0.8))
orange = QColor(255, 165, 0)
purple = QColor(255, 0, 255)
light_orange = QColor(255, 165, 0, int(255 * 0.4))
light_green = QColor(0, 255, 0, int(255 * 0.4))
transparency = QColor(0, 255, 0, int(255 * 0))

class PaintMaster(object):

    @staticmethod
    def pen(color, width=0):
        pen = QPen(color)
        pen.setWidth(width)
        return pen

    @staticmethod
    def brush(color, pattern=Qt.SolidPattern):
        brush = QBrush(color, pattern)
        return brush

    @staticmethod
    def set_pen_brush(painter, color):
        pen = PaintMaster.pen(color.border, color.borderSize)
        brush = PaintMaster.brush(color.fill, color.fill_pattern)
        # set
        painter.setPen(pen)
        painter.setBrush(brush)

class Color(object):
    def __init__(self, border=transparency, fill=transparency, borderSize=3, fill_pattern=Qt.SolidPattern):
        self.border = border
        self.fill = fill
        self.borderSize = borderSize
        self.fill_pattern = fill_pattern

class NoColor(Color):
    def __init__(self):
        super().__init__(border=transparency, fill=transparency)