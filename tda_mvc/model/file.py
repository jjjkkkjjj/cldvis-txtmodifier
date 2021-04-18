import os, datetime, cv2

from .base import ModelAbstractMixin
from ..utils.modes import ShowingMode, AreaMode
from .tda import TDA

class FileModelMixin(ModelAbstractMixin):

    def __init__(self):
        self._imgIndex = -1
        self._imgPaths = []
        self.default_tdaname = ''

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

    @property
    def export_tdaDir(self):
        return os.path.join(self.config.export_datasetDir, 'tda')
    @property
    def export_imageDir(self):
        return os.path.join(self.config.export_datasetDir, 'image')
    @property
    def export_datasetDir(self):
        return os.path.join(self.config.export_datasetDir, 'dataset')
    @property
    def tdapath(self):
        return os.path.join(self.config.export_datasetDir, 'tda', self.default_tdaname)

    def _set_defaultsavename(self):
        self.default_tdaname = os.path.splitext(os.path.basename(self.imgpath))[0] + '.tda'

    def forward(self):
        if self.isExistForwardImg:
            self._imgIndex += 1
            self._set_defaultsavename()

    def back(self):
        if self.isExistBackImg:
            self._imgIndex += -1
            self._set_defaultsavename()

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
        self.config.lastOpenDir = os.path.dirname(self._imgPaths[0])
        self._set_defaultsavename()

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

        return True

    def get_default_tda(self):
        """
        Get tda file in default dataset directory
        Returns
        -------
            TDA or None
        """
        if not (os.path.exists(self.tdapath) and os.path.isfile(self.tdapath)):
            return None

        return TDA.load(self.tdapath)