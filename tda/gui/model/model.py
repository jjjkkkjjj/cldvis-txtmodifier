from PySide2.QtGui import *
from PySide2.QtCore import *
import os, cv2, glob

from ..functions.config import Config
from ..functions.utils import reconstruct_coordinates
from .polygon import Polygon
from ..widgets.canvas.img import ContextActionType

class Info(object):
    def __init__(self):
        self._imgIndex = -1
        self._imgPaths = []
        self._imgpixmap = None

        self._rubberPercentRect = None
        self.config = Config()

    """
    image
    """
    @property
    def imgpath(self):
        if not self.isExistImg:
            return None
        else:
            return self._imgPaths[self._imgIndex]
    @property
    def isExistImg(self):
        return len(self._imgPaths) > 0
    @property
    def isExistForwardImg(self):
        if self.isExistImg:
            return self._imgIndex != len(self._imgPaths) - 1
        else:
            return False
    @property
    def isExistBackImg(self):
        if self.isExistImg:
            return self._imgIndex != 0
        else:
            return False

    def forward(self):
        if self.isExistForwardImg:
            self._imgIndex += 1
    def back(self):
        if self.isExistBackImg:
            self._imgIndex += -1

    def set_imgPaths(self, paths):
        """
        :param paths: list of str(path) or None
        :return:
        """
        if paths is None:
            pass
            #self._imgIndex = -1
        else:
            self._imgPaths = paths

            self._imgIndex = 0

            self.config.last_opendir = os.path.dirname(self._imgPaths[0])

    """
    rubber
    """
    @property
    def rubberPercentRect(self):
        return self._rubberPercentRect

    @property
    def isExistRubberPercentRect(self):
        return self._rubberPercentRect is not None

    def set_rubberPercentRect(self, rubberPercentRect):
        self._rubberPercentRect = rubberPercentRect

    """
    gcp
    """
    @property
    def credentialJsonpath(self):
        return self.config.credentialJsonpath

    @property
    def isExistCredPath(self):
        return self.config.credentialJsonpath is not None

    def set_credentialJsonpath(self, path):
        self.config.credentialJsonpath = path

    def save_tmpimg(self, imgpath, tableRect, directory=os.path.join('..', '.tda', 'tmp')):
        img = cv2.imread(imgpath)
        h, w, _ = img.shape

        xmin, ymin, xmax, ymax = reconstruct_coordinates(tableRect, w, h)

        filename, ext = os.path.splitext(os.path.basename(imgpath))
        apex = '_x{}X{}y{}Y{}'.format(xmin, xmax, ymin, ymax)
        savepath = os.path.abspath(os.path.join(directory, filename + apex + '.jpg'))

        cv2.imwrite(savepath, img[ymin:ymax, xmin:xmax])
        return savepath

    def remove_tmpimg(self, directory=os.path.join('..', '.tda', 'tmp')):
        files = glob.glob(os.path.join(directory, '*.jpg'))
        for f in files:
            os.remove(f)


class Annotation(object):
    def __init__(self):
        self._polygons = []
        self._selected_index = -1  # -1 if polygon is not selected
        # attr: offset is QPoint!
        self.offset = QPoint(0, 0)

    def set_qpolygons(self, area=None, offset=None):
        for i, polygon in enumerate(self._polygons):
            self._polygons[i] = polygon.set_qpolygon(area, offset)

    def set_selectPos(self, pos):
        # all of polygons are reset selected variable first
        for polygon in self._polygons:
            polygon.set_selectPos(None)

        for i, polygon in reversed(list(enumerate(self._polygons))):
            if polygon.set_selectPos(pos):
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
    def selected_polygon(self):
        if self.isExistSelectedPolygon:
            return self._polygons[self._selected_index]
        else:
            return None

    @property
    def selected_polygonIndex(self):
        if self.isExistSelectedPolygon:
            return self._selected_index
        else:
            return None

    @property
    def isExistSelectedPolygon(self):
        return self._selected_index != -1

    @property
    def isExistSelectedPoint(self):
        if self.isExistSelectedPolygon:
            return self.selected_polygon.isSelectedPoint
        else:
            return False

    def refresh(self):
        self._polygons = []

    def insert(self, index, polygon):
        self._polygons.insert(index, polygon)

    def append(self, polygon):
        self._polygons.append(polygon)

    def __len__(self):
        return len(self._polygons)

    def __setitem__(self, index, polygon):
        self._polygons[index] = polygon

    def __getitem__(self, index):
        if not isinstance(index, int):
            raise ValueError('index must be int, but got {}'.format(type(index).__name__))
        return self._polygons[index]

    def __delitem__(self, index):
        if not isinstance(index, int):
            raise ValueError('index must be int, but got {}'.format(type(index).__name__))
        del self._polygons[index]

    def __iter__(self):
        for polygon in self._polygons:
            yield polygon

    def qpolygons(self):
        """
        iterate for qpolygon for each polygon. Yield QPolygon class for each iteration
        :return:
        """
        for polygon in self._polygons:
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
            self.append(Polygon(result["bbox"], result['text'], area, offset))

    @property
    def enableStatus_contextAction(self):
        return {'isSelectedPolygon': self.isExistSelectedPolygon,
                'isSelectedPoint': self.isExistSelectedPoint}

    def change_polygons(self, actionType):
        if actionType == ContextActionType.REMOVE_POLYGON:
            del self[self.selected_polygonIndex]
        elif actionType == ContextActionType.DUPLICATE_POLYGON:
            self.append(self.selected_polygon.duplicateMe())
        elif actionType == ContextActionType.REMOVE_POINT:
            pass
        elif actionType == ContextActionType.DUPLICATE_POINT:
            pass
