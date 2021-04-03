from PySide2.QtGui import *
import os
import numpy as np

def check_instance(name, val, cls, allow_none=True):
    if allow_none and val is None:
        return val

    if not isinstance(val, cls):
        if isinstance(cls, (list, tuple)):
            clsnames = [c.__name__ for c in cls]
            raise ValueError('Invalid argument: \'{}\' must be {}, but got {}'.format(name, clsnames, type(val).__name__))
        else:
            raise ValueError('Invalid argument: \'{}\' must be {}, but got {}'.format(name, cls.__name__, type(val).__name__))

    return val

def path_desktop():
    return os.path.join(os.path.expanduser('~'), 'Desktop')

def cvimg2qpixmap(cvimg: np.ndarray):
    """
    Convert opencv's image ndarray into QPixmap
    Parameters
    ----------
    cvimg: ndarray
        The image ndarray (BGR order) loaded by opencv

    Returns
    -------
    QPixmap
        The image QPixmap

    """
    height, width, channel = cvimg.shape
    bytesPerLine = 3 * width
    qImg = QImage(cvimg.data, width, height, bytesPerLine, QImage.Format_RGB888)
    return QPixmap(qImg)

def sort_clockwise(a):
    """
    Sort corners points (x1, y1, x2, y2, ... clockwise from topleft)
    :ref https://gist.github.com/flashlib/e8261539915426866ae910d55a3f9959
    :param a: ndarray, shape is (points nums, 2=(x,y))
    :return a: ndarray, shape is (points nums... clockwise from topleft, 2=(x,y))
    """

    # get centroids, shape=(1,2=(cx,cy))
    center = a.mean(axis=0).reshape((1, 2))

    sorted_inds = np.argsort(np.arctan2(a[:, 1]-center[:, 1], a[:, 0]-center[:, 0]))

    return np.take(a, sorted_inds, axis=0)