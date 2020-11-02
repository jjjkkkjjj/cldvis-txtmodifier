from PySide2.QtGui import *
import os

def path_desktop():
    return os.path.join(os.path.expanduser('~'), 'Desktop')

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

def cvimg2qpixmap(cvimg):
    height, width, channel = cvimg.shape
    bytesPerLine = 3 * width
    qImg = QImage(cvimg.data, width, height, bytesPerLine, QImage.Format_RGB888)
    return QPixmap(qImg)

def reconstruct_coordinates(percentRect, w, h):
    """
    :param percentRect: tuple-like, (xmin, ymin, xmax, ymax)
    :param w: int, width
    :param h: int, height
    :return:
    """
    xmin, ymin, xmax, ymax = percentRect
    xmin, xmax = int(xmin * w), int(xmax * w)
    ymin, ymax = int(ymin * h), int(ymax * h)
    return xmin, ymin, xmax, ymax