from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

import numpy as np

from ..widgets.canvas.img import ContextActionType
from .geometry import Polygon
from .paint_utils import *

class AnnotationManager(object):
    def __init__(self):
        self._annotations = []
        self._selected_index = -1  # -1 if annotation is not selected
        # attr: offsetQPoint is QPoint!
        self.offsetQPoint = QPoint(0, 0)

    def set_parentVals(self, parentQSize=None, offsetQPoint=None):
        for annotation in self._annotations:
            annotation.set_parentVals(parentQSize, offsetQPoint)

    def set_selectPos(self, pos):
        # all of polygons are reset selected variable first
        for annotation in self._annotations:
            annotation.set_selectPos(None)

        for i, annotation in reversed(list(enumerate(self._annotations))):
            if annotation.set_selectPos(pos):
                self._selected_index = i
                return
        # All of polygons are not selected
        self._selected_index = -1

    @property
    def offset_x(self):
        return self.offsetQPoint.x()

    @property
    def offset_y(self):
        return self.offsetQPoint.y()

    @property
    def selected_annotation(self):
        if self.isExistSelectedAnnotation:
            return self._annotations[self._selected_index]
        else:
            return None

    @property
    def selected_annotationIndex(self):
        if self.isExistSelectedAnnotation:
            return self._selected_index
        else:
            return None

    @property
    def isExistSelectedAnnotation(self):
        return self._selected_index != -1

    @property
    def isExistSelectedPoint(self):
        if self.isExistSelectedAnnotation:
            return self.selected_annotation.isSelectedPoint
        else:
            return False

    def refresh(self):
        self._annotations = []

    def insert(self, index, annotation):
        self._annotations.insert(index, annotation)

    def append(self, annotation):
        self._annotations.append(annotation)

    def __len__(self):
        return len(self._annotations)

    def __setitem__(self, index, polygon):
        self._annotations[index] = polygon

    def __getitem__(self, index):
        if not isinstance(index, int):
            raise ValueError('index must be int, but got {}'.format(type(index).__name__))
        return self._annotations[index]

    def __delitem__(self, index):
        if not isinstance(index, int):
            raise ValueError('index must be int, but got {}'.format(type(index).__name__))
        del self._annotations[index]

    def __iter__(self):
        for annotation in self._annotations:
            yield annotation

    def show(self):
        for anno in self._annotations:
            anno.show()

    def hide(self):
        for anno in self._annotations:
            anno.hide()

    def qpolygons(self):
        """
        iterate for qpolygon for each annotation. Yield QPolygon class for each iteration
        :return:
        """
        for anno in self._annotations:
            yield anno.qpolygon

    def set_highlight(self, pos):
        pass

    def set_detectionResult(self, results, baseWidget, parentQSize, offsetQPoint):
        """
        :param results: dict, detection result by vision
        :param baseWidget: QWidget, the base widget for AnnotaionRubberBand
        :param parentQSize: Qsize, selected parentQSize
        :param offsetQPoint: QPoint, the topleft coordinates for selected parentQSize
        :return:
        """

        """
        results: dict
            "info":
                "width": int
                "height": int
                "path": str
            "prediction": list of dict whose keys are 'text' and 'bbox'
                "text": str
                "bbox": list(4 points) of list(2d=(x, y))
        """
        # create annotation instances, and then draw polygons
        self.offsetQPoint = offsetQPoint
        for result in results["prediction"]:
            self.append(Annotation(baseWidget, result["bbox"], result['text'], parentQSize, offsetQPoint))

    @property
    def enableStatus_contextAction(self):
        return {'isSelectedPolygon': self.isExistSelectedAnnotation,
                'isSelectedPoint': self.isExistSelectedPoint}

    def change_annotations(self, actionType):
        if actionType == ContextActionType.REMOVE_ANNOTATION:
            del self[self.selected_annotationIndex]
        elif actionType == ContextActionType.DUPLICATE_ANNOTATION:
            newanno = self.selected_annotation.duplicateMe()
            newanno.show()
            self.append(newanno)
        elif actionType == ContextActionType.REMOVE_POINT:
            pass
        elif actionType == ContextActionType.DUPLICATE_POINT:
            pass


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

        vbox = QVBoxLayout(self)
        self.label = QLabel(self)
        self.label.setText(self.text)
        font = self.font()
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setStyleSheet("QLabel { color : red; }")
        vbox.addWidget(self.label)
        self.setLayout(vbox)

        self.text_color = Color(border=black)
        self._isShowText = True

    @property
    def isShowText(self):
        return self._isShowText

    @isShowText.setter
    def isShowText(self, val):
        self._isShowText = val

        if val:
            self.label.setText(self.text)
        else:
            self.label.setText("")


    def paintEvent(self, event):
        # not drawing at all!!
        return