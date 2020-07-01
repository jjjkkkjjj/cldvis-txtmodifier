from PySide2.QtGui import *
import os

from .functions.config import Config

class Model(object):
    def __init__(self):
        self._imgIndex = -1
        self._imgPaths = None
        self._imgpixmap = None

        self.config = Config()

    @property
    def imgpath(self):
        if self._imgPaths is None:
            return None
        else:
            return self._imgPaths[self._imgIndex]


    def set_imgPaths(self, paths):
        """
        :param paths: list of str(path) or None
        :return:
        """
        self._imgPaths = paths
        if paths is None:
            self._imgIndex = -1
        else:
            self._imgIndex = 0

            self.config.last_opendir = os.path.dirname(self._imgPaths[0])

