import os, datetime, cv2

from .base import ModelAbstractMixin
from ..utils.modes import ShowingMode, AreaMode
from .tda import TDA

class FileModelMixin(ModelAbstractMixin):

    def __init__(self):
        self._imgIndex = -1
        self._imgPaths = []
        self.defaultsavename = ''

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
        if paths is None or len(paths) == 0:
            # self._imgIndex = -1
            return

        self._imgPaths = paths
        self._imgIndex = 0
        self.config.last_opendir = os.path.dirname(self._imgPaths[0])

    def saveInDefaultDirectory(self):
        filename = os.path.splitext(self.defaultsavename)[0]
        #now = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

        tdadirpath = os.path.join(self.config.export_datasetdir, 'tda')
        imgdirpath = os.path.join(self.config.export_datasetdir, 'image')
        datasetdirpath = os.path.join(self.config.export_datasetdir, 'dataset')

        os.makedirs(tdadirpath, exist_ok=True)
        os.makedirs(imgdirpath, exist_ok=True)
        os.makedirs(datasetdirpath, exist_ok=True)

        if os.path.exists(os.path.join(tdadirpath, filename + '.tda')):
            return False

        # save tda
        tda = TDA(self)
        TDA.save(tda, os.path.join(tdadirpath, filename + '.tda'))

        # save image
        if self.areamode == AreaMode.RECTANGLE:
            self.saveSelectedImg_rectmode(self.imgpath)
        elif self.areamode == AreaMode.QUADRANGLE:
            self.saveSelectedImg_quadmode(self.imgpath)

        _, ext = os.path.splitext(self.selectedImgPath)
        cvimg = cv2.imread(self.selectedImgPath)
        cv2.imwrite(os.path.join(imgdirpath, filename + ext), cvimg)

        return True