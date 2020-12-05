from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

import numpy as np

from ..widgets.canvas.img import ContextActionType
from .geometry import Polygon

class AnnotationManager(object):
    def __init__(self):
        self._annotations = []
        self._selected_index = -1  # -1 if polygon is not selected
        # attr: offset is QPoint!
        self.offset = QPoint(0, 0)

    def set_qpolygons(self, area=None, offset=None):
        for i, annotation in enumerate(self._annotations):
            self._annotations[i] = annotation.set_qpolygon(area, offset)

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
        return self.offset.x()

    @property
    def offset_y(self):
        return self.offset.y()

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

    def insert(self, index, polygon):
        self._annotations.insert(index, polygon)

    def append(self, polygon):
        self._annotations.append(polygon)

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
        iterate for qpolygon for each polygon. Yield QPolygon class for each iteration
        :return:
        """
        for polygon in self._annotations:
            yield polygon.qpolygon

    def set_highlight(self, pos):
        pass

    def set_detectionResult(self, results, area, offset):
        """
        :param results: dict, detection result by vision
        :param area: Qsize, selected area
        :param offset: QPoint, the topleft coordinates for selected area
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
        # create polygon instances, and then draw polygons
        self.offset = offset
        for result in results["prediction"]:
            self.append(Annotation(result["bbox"], result['text'], area, offset))

    @property
    def enableStatus_contextAction(self):
        return {'isSelectedPolygon': self.isExistSelectedAnnotation,
                'isSelectedPoint': self.isExistSelectedPoint}

    def change_annotations(self, actionType):
        if actionType == ContextActionType.REMOVE_ANNOTATION:
            del self[self.selected_annotationIndex]
        elif actionType == ContextActionType.DUPLICATE_ANNOTATION:
            self.append(self.selected_annotation.duplicateMe())
        elif actionType == ContextActionType.REMOVE_POINT:
            pass
        elif actionType == ContextActionType.DUPLICATE_POINT:
            pass


class Annotation(Polygon):
    def __init__(self, points, text, area, offset):
        """
        :param points: list of list(2d=(x,y)), Note that these points are in percentage
        :param text: str
        :param area: QSize
        :param offset: QPoint
        """
        super().__init__(points, area, offset)
        self.text = text

    def duplicateMe(self):
        newpoints_percent = self.points_percent.copy()
        newpoints_percent[:, 0] += 10 / self.width
        newpoints_percent[:, 1] += 10 / self.height
        return Annotation(newpoints_percent, self.area, self.offset)