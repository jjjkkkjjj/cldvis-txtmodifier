from PySide2.QtGui import *
from PySide2.QtCore import *

green = QColor(0, 255, 0, int(255 * 0.8))
red = QColor(255, 0, 0, int(255 * 0.8))
orange = QColor(255, 165, 0)
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
    def set_pen_brush(painter, pen_color, pen_width, brush_color, brush_pattern):
        pen = PaintMaster.pen(pen_color, pen_width)
        brush = PaintMaster.brush(brush_color, brush_pattern)
        # set
        painter.setPen(pen)
        painter.setBrush(brush)

class Color(object):
    def __init__(self, border=transparency, fill=transparency):
        self.border = border
        self.fill = fill
