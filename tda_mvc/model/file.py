import os

from .base import ModelAbstractMixin

class FileModelMixin(ModelAbstractMixin):

    def __init__(self):
        self._imgIndex = -1
        self._imgPaths = []

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
            # self._imgIndex = -1
            return

        self._imgPaths = paths
        self._imgIndex = 0
        self.config.last_opendir = os.path.dirname(self._imgPaths[0])