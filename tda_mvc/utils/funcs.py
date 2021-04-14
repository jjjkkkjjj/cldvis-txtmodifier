from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import os, cv2
import numpy as np

from .modes import ShowingMode

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

def qsize_from_quadrangle(qpoints):
    """
    Get qsize from quadrangle
    Parameters
    ----------
    qpoints: list(4) of QPoints
        The quadrangle QPoints
    Returns
    -------

    """
    assert len(qpoints) == 4, "must have 4 qpoints, but got {}".format(len(qpoints))
    tl, tr, br, bl = qpoints
    hmax = int(max((bl - tl).y(), (br - tr).y()))
    wmax = int(max((tr - tl).x(), (br - bl).x()))
    return QSize(wmax, hmax)

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

def get_pixmap(model, parentQSize=None):
    """
    Get pixmap from the current status
    Parameters
    ----------
    model: Model

    parentQSize: QSize (Optional)
        The parent widget size. if the returned pixmap's size is smaller than this size,
        the one will be padded in gray

    Returns
    -------
    QPixmap
        The current pixmap to set the imageView

    """
    from ..model import Model
    model: Model

    if model.showingmode == ShowingMode.ENTIRE:
        cvimg = cv2.imread(model.imgpath)
    elif model.showingmode == ShowingMode.SELECTED:
        cvimg = cv2.imread(model.selectedImgPath)

    h, w, c = cvimg.shape
    ratio = model.zoomvalue / 100.
    cvimg = cv2.resize(cvimg, (int(w * ratio), int(h * ratio)))

    if parentQSize is not None:
        h, w, c = cvimg.shape
        padded_w = parentQSize.width() - w
        if padded_w > 0:
            # light gray color = BGR=166
            padded_img = np.ones(shape=(h, padded_w, c), dtype=np.uint8) * 166
            cvimg = np.concatenate((cvimg, padded_img), axis=1)

        h, w, c = cvimg.shape
        padded_h = parentQSize.height() - h
        if padded_h > 0:
            # light gray color = BGR=166
            padded_img = np.ones(shape=(padded_h, w, c), dtype=np.uint8) * 166
            cvimg = np.concatenate((cvimg, padded_img), axis=0)

    pixmap = cvimg2qpixmap(cvimg)
    return pixmap


def add_actions(target, actions):
    for action in actions:
        if action is None:
            target.addSeparator()
        else:
            target.addAction(action)

def create_action(self, text, slot=None, shortcut=None,
                  icon=None, tip=None, checkable=False, ):
    action = QAction(text, self)
    if icon is not None:
        action.setIcon(QIcon(":/%s.png" % icon))
    if shortcut is not None:
        action.setShortcut(shortcut)
    if tip is not None:
        action.setToolTip(tip)
        action.setStatusTip(tip)
    if slot is not None:
        action.triggered.connect(slot)
    if checkable:
        action.setCheckable(True)
    return action