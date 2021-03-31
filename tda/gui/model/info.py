from PySide2.QtGui import *
from PySide2.QtCore import *
import os, cv2, glob
import numpy as np

from ..functions.config import Config
from ..functions.utils import reconstruct_minmaxcoordinates, reconstruct_polycoordinates
from ..widgets.eveUtils import PredictionMode

class InfoManager(object):
    def __init__(self):
        self._imgIndex = -1
        self._imgPaths = []
        self._imgpixmap = None

        self._areaPercentPolygon = None
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
    parentQSize
    """
    @property
    def areaPercentPolygon(self):
        return self._areaPercentPolygon

    @property
    def isExistAreaPercentRect(self):
        return self._areaPercentPolygon is not None

    def set_selectionArea(self, areaPercentRect):
        self._areaPercentPolygon = areaPercentRect

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

    def save_tmpimg(self, imgpath, areaPercentPolygon, mode, directory=os.path.join('.tda', 'tmp')):
        img = cv2.imread(imgpath)
        h, w, _ = img.shape

        if mode == PredictionMode.IMAGE:
            xmin, ymin, xmax, ymax = reconstruct_minmaxcoordinates(areaPercentPolygon, w, h)

            filename, ext = os.path.splitext(os.path.basename(imgpath))
            apex = '_x{}X{}y{}Y{}'.format(xmin, xmax, ymin, ymax)
            savepath = os.path.abspath(os.path.join(directory, filename + apex + '.jpg'))

            cv2.imwrite(savepath, img[ymin:ymax, xmin:xmax])
        elif mode == PredictionMode.TABLE:
            tl, tr, br, bl = reconstruct_polycoordinates(areaPercentPolygon, w, h).astype(np.float32)
            hmax = int(max((bl - tl)[1], (br - tr)[1]))
            wmax = int(max((tr - tl)[0], (br - bl)[0]))

            # affine transform
            src = np.vstack((tl, tr, bl))
            dst = np.array(((0, 0), (wmax, 0), (0, hmax)), dtype=np.float32)
            warp_mat = cv2.getAffineTransform(src, dst)
            img_cropped = cv2.warpAffine(img, warp_mat, (wmax, hmax))

            # savepath
            areaPoly = np.vstack((tl, tr, br, bl)).flatten().astype(int)
            filename, ext = os.path.splitext(os.path.basename(imgpath))
            apex = '_tlx{}tly{}trx{}try{}brx{}bry{}blx{}bly{}'.format(*areaPoly)
            savepath = os.path.abspath(os.path.join(directory, filename + apex + '.jpg'))

            cv2.imwrite(savepath, img_cropped)
        return savepath

    def remove_tmpimg(self, directory=os.path.join('..', '.tda', 'tmp')):
        files = glob.glob(os.path.join(directory, '*.jpg'))
        for f in files:
            os.remove(f)


