from PySide2.QtGui import *
from PySide2.QtCore import *
import os, cv2, glob

from ..functions.config import Config
from ..functions.utils import reconstruct_coordinates


class InfoManager(object):
    def __init__(self):
        self._imgIndex = -1
        self._imgPaths = []
        self._imgpixmap = None

        self._areaPercentRect = None
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
    area
    """
    @property
    def areaPercentRect(self):
        return self._areaPercentRect

    @property
    def isExistAreaPercentRect(self):
        return self._areaPercentRect is not None

    def set_selectionArea(self, areaPercentRect):
        self._areaPercentRect = areaPercentRect

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


