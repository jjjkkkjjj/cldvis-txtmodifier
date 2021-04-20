from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import json, os, datetime, cv2
import pandas as pd

from .base import ModelAbstractMixin
from ..utils.geometry import Annotation, Polygon
from ..utils.paint import Color, NoColor, transparency, orange
from ..utils.modes import MoveActionState, AreaMode
from ..utils.funcs import qsize_from_quadrangle
from ..utils.parse_annotation import parse_annotations_forFile, parse_annotations_forVOC
from .tda import TDA

class AnnotationModelMixin(ModelAbstractMixin, QAbstractTableModel):

    def __init__(self):
        QAbstractTableModel.__init__(self, parent=None)

        self._header_labels = ['Text']

        self.results = {}
        self.annotations = AnnotationsManager()
        # prediction area
        self.predictedArea = Polygon(maximum_points_number=4)
        self.predictedArea.set_color(poly_default_color=Color(border=orange, fill=transparency),
                                     vertex_default_color=NoColor())

    @property
    def isPredicted(self):
        return len(self.results) > 0

    @property
    def predictedAreaQSize(self):
        return qsize_from_quadrangle(self.predictedArea.qpoints)
    @property
    def predictedAreaTopLeft(self):
        return self.predictedArea.qpoints[0]

    def data(self, index, role=None):
        if role == Qt.DisplayRole:
            anno: Annotation = self.annotations[index.row()]
            return anno.text

    def headerData(self, section, orientation, role=None):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self._header_labels[section]
        return super().headerData(section, orientation, role)

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.annotations)

    def columnCount(self, parent=None, *args, **kwargs):
        return 1

    def set_results(self, results, baseWidget, parentQSize, offsetQPoint):
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
        self.results = results
        self.annotations.set_results(results, baseWidget, parentQSize, offsetQPoint)

    def discard_annotations(self):
        self.results = {}
        self.annotations.clear()
        # prediction area
        self.predictedArea = Polygon(maximum_points_number=4)
        self.predictedArea.set_color(poly_default_color=Color(border=orange, fill=transparency),
                                     vertex_default_color=NoColor())
    def saveAsJson(self, path):
        with open(path, 'w') as f:
            json.dump(self.results, f)

    def saveAsCSV(self, path):
        table_list = parse_annotations_forFile(self)
        df = pd.DataFrame(table_list)
        df.to_csv(path, sep=',', header=False, index=False, encoding='utf-8')

    def saveAsEXCEL(self, path):
        table_list = parse_annotations_forFile(self)
        df = pd.DataFrame(table_list)
        df.to_excel(path, header=False, index=False, encoding='utf-8')

    def saveAsTSV(self, path):
        table_list = parse_annotations_forFile(self)
        df = pd.DataFrame(table_list)
        df.to_csv(path, sep='\t', header=False, index=False, encoding='utf-8')

    def saveAsPSV(self, path):
        table_list = parse_annotations_forFile(self)
        df = pd.DataFrame(table_list)
        df.to_csv(path, sep='|', header=False, index=False, encoding='utf-8')

    def saveAsVOC(self, path):
        # save image
        if self.areamode == AreaMode.RECTANGLE:
            self.saveSelectedImg_rectmode(self.imgpath)
        elif self.areamode == AreaMode.QUADRANGLE:
            self.saveSelectedImg_quadmode(self.imgpath)

        _, ext = os.path.splitext(self.selectedImgPath)
        cvimg = cv2.imread(self.selectedImgPath)

        dipath = os.path.dirname(path)
        imgname, _ = os.path.splitext(os.path.basename(path))
        imgpath = os.path.join(dipath, imgname + ext)
        cv2.imwrite(imgpath, cvimg)

        vocstr = parse_annotations_forVOC(self, imgpath)
        with open(path, 'wb') as f:
            f.write(vocstr)

    def saveInDefaultDirectory(self):
        filename = os.path.splitext(self.default_tdaname)[0]
        #now = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

        os.makedirs(self.export_tdaDir, exist_ok=True)
        os.makedirs(self.export_imageDir, exist_ok=True)
        os.makedirs(self.export_datasetDir, exist_ok=True)

        if os.path.exists(os.path.join(self.export_tdaDir, filename + '.tda')):
            return False

        # save tda
        tda = TDA(self)
        TDA.save(tda, os.path.join(self.export_tdaDir, filename + '.tda'))

        # save image
        if self.areamode == AreaMode.RECTANGLE:
            self.saveSelectedImg_rectmode(self.imgpath)
        elif self.areamode == AreaMode.QUADRANGLE:
            self.saveSelectedImg_quadmode(self.imgpath)

        _, ext = os.path.splitext(self.selectedImgPath)
        cvimg = cv2.imread(self.selectedImgPath)
        cv2.imwrite(os.path.join(self.export_imageDir, filename + ext), cvimg)

        # save dataset
        if self.config.export_datasetFormat == 'VOC':
            self.saveAsVOC(os.path.join(self.export_datasetDir, filename + '.xml'))

        return True

class AnnotationsManager(object):
    def __init__(self):
        # -1 if annotation is not selected
        self._selectedIndex = -1

        self._startPosition = QPoint(0, 0)

        self._annotations = []

        self.moveActionState = MoveActionState.CREATE

    def __iter__(self):
        """
        Note that this property returns generator, not list
        """
        for anno in self._annotations:
            yield anno

    def __getitem__(self, index):
        return self._annotations[index]

    def __len__(self):
        return len(self._annotations)

    def append(self, anno):
        self._annotations += [anno]

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

    def set_results(self, results, baseWidget, parentQSize, offsetQPoint):
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

        self._annotations = []
        self._info = results['info']
        for result in results['prediction']:
            anno = Annotation(baseWidget, result["bbox"], result['text'], parentQSize, offsetQPoint)
            self._annotations += [anno]
            anno.show()

    def to_dict(self):
        ret = {}
        ret['info'] = self._info
        ret['prediction'] = []
        for anno in self._annotations:
            pred = {}
            pred['text'] = anno.text
            pred['bbox'] = anno.percent_points
            ret['prediction'] += [pred]
        return ret

    def clear(self):
        for i in reversed(range(len(self._annotations))):
            self._annotations[i].clear()
            del self._annotations[i]
        self._selectedIndex = -1
        self._startPosition = QPoint(0, 0)
        self._annotations = []
        self.moveActionState = MoveActionState.CREATE

    def paint(self, painter, isShow):
        if isShow:
            for anno in self._annotations:
                anno.paint(painter)
                anno.show()
        else:
            for anno in self._annotations:
                anno.paint(painter)
                anno.hide()

    def show(self):
        for anno in self._annotations:
            anno.show()

    def hide(self):
        for anno in self._annotations:
            anno.hide()

    def set_parentVals(self, parentQSize=None, offsetQPoint=None):
        for anno in self._annotations:
            anno.set_parentVals(parentQSize, offsetQPoint)

    def set_selectPos(self, pos):
        for anno in self._annotations:
            anno.set_selectPos(None)

        for i, anno in reversed(list(enumerate(self._annotations))):
            if anno.set_selectPos(pos):
                self._selectedIndex = i
                return
        # All of polygons are not selected
        self._selectedIndex = -1

    def remove_selectedAnnotation(self):
        if self.isExistSelectedAnnotation:
            del self._annotations[self.selectedAnnotationIndex]
            self._selectedIndex = -1

    def duplicate_selectedAnnotation(self):
        if self.isExistSelectedAnnotation:
            newanno = self.selectedAnnotation.duplicateMe()
            newanno.show()
            self.append(newanno)

    def remove_selectedAnnotationPoint(self):
        if self.isExistSelectedAnnotationPoint:
            anno: Annotation = self.selectedAnnotation
            if anno.points_number > 3:
                anno.remove_point(anno.selectedPointIndex)
            else:
                self.remove_selectedAnnotation()

    def duplicate_selectedAnnotationPoint(self):
        if self.isExistSelectedAnnotationPoint:
            anno: Annotation = self.selectedAnnotation
            anno.duplicate_point(anno.selectedPointIndex)

    def mousePress(self, pos, parentQSize):
        self._startPosition = pos
        self.set_parentVals(parentQSize)
        self.set_selectPos(pos)

        if self.isExistSelectedAnnotationPoint:
            self.moveActionState = MoveActionState.RESIZE
            self._startPosition = self.selectedAnnotation.selectedQPoint
            return

        if self.isExistSelectedAnnotation:
            # if pressed position is contained in parentQSize
            # move the parentQSize
            self.moveActionState = MoveActionState.MOVE

    def mouseMoveClicked(self, pos, parentQSize: QSize):
        if not self.isExistSelectedAnnotation:
            return

        anno: Annotation = self.selectedAnnotation
        if self.moveActionState == MoveActionState.MOVE:
            movedAmount = pos - self._startPosition
            anno.move(movedAmount)
            self._startPosition = pos
            return

        offsetted_pos = pos - anno.offsetQPoint
        # clipping
        offsetted_pos.setX(min(max(offsetted_pos.x(), 0), parentQSize.width()))
        offsetted_pos.setY(min(max(offsetted_pos.y(), 0), parentQSize.height()))

        if self.moveActionState == MoveActionState.RESIZE:
            anno.move_qpoint(anno.selectedPointIndex, offsetted_pos)


    def mouseMoveNoButton(self, pos):
        self.set_selectPos(pos)

    def mouseRelease(self):
        self._startPosition = QPoint(0, 0)