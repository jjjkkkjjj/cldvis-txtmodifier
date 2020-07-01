
class Model(object):
    def __init__(self):
        self._imgIndex = -1
        self._imgPaths = None

    @property
    def imgpath(self):
        if self._imgIndex < 0:
            return None
        else:
            return self._imgPaths[self._imgIndex]


    def set_imgPaths(self, paths):
        self._imgPaths = paths
        if paths is None:
            self._imgIndex = -1
        else:
            self._imgIndex = 0