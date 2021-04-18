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
    Sort corners points (x1, y1, x2, y2, ... clockwise from topleft), shape = (*, 2)
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

    QSize
        The shown image's size

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
    originalImgQSize = QSize(int(w * ratio), int(h * ratio))

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
    return pixmap, originalImgQSize


def parse_annotations(model):
    from ..model import Model
    model: Model
    polys = np.array([anno.pts for anno in model.annotations], dtype=int)
    texts = np.array([anno.text for anno in model.annotations])

    ret = []
    while polys.shape[0] > 0:
        # target_poly: shape = (1, points_num, 2=(x, y))
        # target_text: shape = (1,)
        target_poly = polys[:1]
        target_text = texts[:1]

        # polys: shape = (cand_num, points_num, 2=(x, y))
        # texts: shape = (cand_num,)
        polys = polys[1:]
        texts = texts[1:]

        # extract the values with top-left y within the error for target_poly's one
        # shape = (cand_num,)
        line_bindices = np.abs(polys[:, 0, 1] - target_poly[:, 0, 1]) < model.config.export_sameRowY

        # line_polys: shape = (column_num, points_num, 2=(x,y))
        # line_texts: shape = (column_num,)
        line_polys = np.concatenate((target_poly, polys[line_bindices]), axis=0)
        line_texts = np.concatenate((target_text, texts[line_bindices]), axis=0)

        polys = polys[np.logical_not(line_bindices)]
        texts = texts[np.logical_not(line_bindices)]
        if polys.shape[0] == 0:
            break

        # sort top-left x with ascending order
        tlx_indices = np.argsort(line_polys[:, 0, 0])
        line_polys = np.take(line_polys, tlx_indices, axis=0)
        line_texts = np.take(line_texts, tlx_indices, axis=0)

        row = []
        while line_polys.shape[0] > 0:

            column_text = line_texts[0]

            # extract the values with top-left x(min) within the error for target_poly's maximum x
            concat_index = 1
            for r_index in range(1, line_polys.shape[0]):
                left_poly_maxX = line_polys[r_index - 1, :, 0].max()
                right_poly_minX = line_polys[r_index, :, 0].min()
                if np.abs(left_poly_maxX - right_poly_minX) < model.config.export_sameColX:
                    concat_index = r_index + 1
                    column_text += line_texts[r_index]
                else:
                    break

            # update
            line_polys = line_polys[concat_index:]
            line_texts = line_texts[concat_index:]

            row += [column_text]
        ret += [row]

    return ret


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