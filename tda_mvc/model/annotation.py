from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from .base import ModelAbstractMixin
from ..utils.geometry import Annotation, Polygon
from ..utils.paint import Color, NoColor, transparency, orange

class AnnotationModelMixin(ModelAbstractMixin):
    def __init__(self):
        # -1 if annotation is not selected
        self._selectedIndex = -1

        self._annotations = []
        # prediction area
        self.predictedArea = Polygon(maximum_points_number=4)
        self.predictedArea.set_color(poly_default_color=Color(border=orange, fill=transparency),
                                     vertex_default_color=NoColor())

    @property
    def selectedAnnotation(self):
        if self.isExistSelectedAnnotation:
            return self._annotations[self._selectedIndex]
        else:
            return None

    @property
    def selectedAnnotationIndex(self):
        if self.isExistSelectedAnnotation:
            return self._selectedIndex
        else:
            return None

    @property
    def isExistSelectedAnnotation(self):
        return self._selectedIndex != -1

    @property
    def isExistSelectedAnnotationPoint(self):
        if self.isExistSelectedAnnotation:
            return self.selectedAnnotation.isSelectedPoint
        else:
            return False

    @property
    def annotations(self):
        """
        Note that this property returns generator, not list
        """
        for anno in self._annotations:
            yield anno

    def set_annotations(self, results, baseWidget, areaQPolygon, parentQSize, offsetQPoint):
        """
        :param results: dict, detection result by vision
            "info":
                "width": int
                "height": int
                "path": str
            "prediction": list of dict whose keys are 'text' and 'bbox'
                "text": str
                "bbox": list(4 points) of list(2d=(x, y))
        :param baseWidget: QWidget, the base widget for AnnotaionRubberBand
        :param areaQPolygon: QPolygon, the selected area's qpolygon
        :param parentQSize: Qsize, selected parentQSize
        :param offsetQPoint: QPoint, the topleft coordinates for selected parentQSize
        :return:
        """

        # Note that the selected area is no offset
        self.predictedArea.set_parentVals(parentQSize)
        self.predictedArea.set_qpolygon(areaQPolygon)
        self.predictedArea.show()

        self._annotations = []
        for result in results['prediction']:
            anno = Annotation(baseWidget, result["bbox"], result['text'], parentQSize, offsetQPoint)
            self._annotations += [anno]
            anno.show()

    def paint_annotations(self, painter, isShow):
        self.predictedArea.paint(painter)

        if isShow:
            for anno in self._annotations:
                anno.paint(painter)
                anno.show()
        else:
            for anno in self._annotations:
                anno.paint(painter)
                anno.hide()

    def show_annotations(self):
        for anno in self._annotations:
            anno.show()

    def hide_annotations(self):
        for anno in self._annotations:
            anno.hide()

    def set_parentVals_annotations(self, parentQSize, offsetQPoint):
        for anno in self._annotations:
            anno.set_parentVals(parentQSize, offsetQPoint)