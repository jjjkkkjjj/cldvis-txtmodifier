import cv2, os, shutil

from ..utils.modes import PredictionMode, MoveActionState, ShowingMode, AreaMode
from ..utils.geometry import *
from ..utils.funcs import qsize_from_quadrangle
from .base import ModelAbstractMixin

class ViewerModelMixin(ModelAbstractMixin):
    def __init__(self):
        self.zoomvalue = 100

        # prediction mode
        self.predmode = PredictionMode.IMAGE

        # showing mode
        self.showingmode = ShowingMode.ENTIRE

        # area mode
        self.areamode = AreaMode.RECTANGLE

        self.moveActionState = MoveActionState.CREATE

        # image mode
        self.rectangle = Rect()
        # table mode
        self.quadrangle = Polygon(maximum_points_number=4)
        self.rectangle.hide()
        self.quadrangle.hide()

        # start position. this is for moveEvent
        self._startPosition = QPoint(0, 0)

        self.selectedRectImgPath = None
        self.selectedQuadImgPath = None

    def discard_area(self):
        # image mode
        self.rectangle = Rect()
        # table mode
        self.quadrangle = Polygon(maximum_points_number=4)
        self.rectangle.hide()
        self.quadrangle.hide()

        # start position. this is for moveEvent
        self._startPosition = QPoint(0, 0)

        self.selectedRectImgPath = None
        self.selectedQuadImgPath = None

    ### Zoom ###
    @property
    def isZoomOutable(self):
        return self.zoomvalue >= 20 + 10
    @property
    def isZoomInable(self):
        return self.zoomvalue <= 190 - 10

    @property
    def isExistArea(self):
        if self.areamode == AreaMode.RECTANGLE:
            return self.rectangle.isDrawableRect
        elif self.areamode == AreaMode.QUADRANGLE:
            return self.quadrangle.isDrawablePolygon
        return False
    @property
    def isPredictable(self):
        # Slightly different from isExistArea!
        if self.areamode == AreaMode.RECTANGLE:
            return self.rectangle.isDrawableRect
        elif self.areamode == AreaMode.QUADRANGLE:
            return self.quadrangle.points_number == 4
        return False
    @property
    def isRectPredictable(self):
        return self.rectangle.isDrawableRect
    @property
    def isQuadPredictable(self):
        return self.quadrangle.points_number == 4

    @property
    def selectedImgPath(self):
        if self.areamode == AreaMode.RECTANGLE:
            return self.selectedRectImgPath
        elif self.areamode == AreaMode.QUADRANGLE:
            return self.selectedQuadImgPath
        return None

    @property
    def areaQPolygon(self):
        if self.areamode == AreaMode.RECTANGLE:
            return self.rectangle.qpolygon
        elif self.areamode == AreaMode.QUADRANGLE:
            return self.quadrangle.qpolygon
        return None
    @property
    def areaQSize(self):
        if self.areamode == AreaMode.RECTANGLE:
            return self.rectangle.qsize
        elif self.areamode == AreaMode.QUADRANGLE:
            return qsize_from_quadrangle(self.quadrangle.qpoints)
        return None
    @property
    def areaTopLeft(self):
        if self.areamode == AreaMode.RECTANGLE:
            return self.rectangle.topLeft
        elif self.areamode == AreaMode.QUADRANGLE:
            return self.quadrangle.qpoints[0]
        return None
    @property
    def areaPercentPts(self):
        if self.areamode == AreaMode.RECTANGLE:
            return self.rectangle.percent_points
        elif self.areamode == AreaMode.QUADRANGLE:
            return self.quadrangle.percent_points
        return None
    @property
    def areaParentQSize(self):
        if self.areamode == AreaMode.RECTANGLE:
            return self.rectangle.parentQSize
        elif self.areamode == AreaMode.QUADRANGLE:
            return self.quadrangle.parentQSize
        return None
    @property
    def areaOffsetQPoint(self):
        if self.areamode == AreaMode.RECTANGLE:
            return self.rectangle.offsetQPoint
        elif self.areamode == AreaMode.QUADRANGLE:
            return self.quadrangle.offsetQPoint
        return None

    ### rect ###
    def mousePress_rectmode(self, pos, parentQSize):
        self._startPosition = pos

        self.rectangle.set_parentVals(parentQSize=parentQSize)
        self.rectangle.set_selectPos(pos)

        if self.rectangle.isSelectedPoint:
            # if pressed position is edge
            # expand or shrink parentQSize
            self.moveActionState = MoveActionState.RESIZE
            # [tl, tr, br, bl] -> [br, bl, tl, tr]
            diagIndex = [2, 3, 0, 1]
            diagPos = self.rectangle.qpoints[diagIndex[self.rectangle.selectedPointIndex]]
            self._startPosition = diagPos
            return

        if self.rectangle.isSelectedRect:
            # if pressed position is contained in parentQSize
            # move the parentQSize
            self.moveActionState = MoveActionState.MOVE

        else:
            # create new parentQSize
            self.moveActionState = MoveActionState.CREATE
            self.rectangle.append(pos)

    def mouseMoveClicked_rectmode(self, pos, parentQSize: QSize):
        if self.moveActionState == MoveActionState.MOVE:
            movedAmount = pos - self._startPosition
            self.rectangle.move(movedAmount)
            self._startPosition = pos
            return

        # Note that moveActionState must be CREATE or RESIZE
        if self.moveActionState == MoveActionState.RESIZE:
            # for changing selected Point
            self.rectangle.set_selectPos(pos)

        # clipping
        pos.setX(min(max(pos.x(), 0), parentQSize.width()))
        pos.setY(min(max(pos.y(), 0), parentQSize.height()))

        qrect = QRect(self._startPosition, pos).normalized()
        self.rectangle.set_qrect(qrect)

    def mouseMoveNoButton_rectmode(self, pos):
        self.rectangle.set_selectPos(pos)

    def mouseRelease_rectmode(self):
        if self.moveActionState == MoveActionState.RESIZE:
            self.rectangle.deselect()
        self._startPosition = QPoint(0, 0)

    def saveSelectedImg_rectmode(self, imgpath):
        if not self.rectangle.isDrawableRect:
            self.selectedRectImgPath = None
            return

        img = cv2.imread(imgpath)
        h, w, _ = img.shape
        x, y = (self.rectangle.percent_x * w).astype(int), (self.rectangle.percent_y * h).astype(int)

        xmin, xmax, ymin, ymax = x.min(), x.max(), y.min(), y.max()

        filename, ext = os.path.splitext(os.path.basename(imgpath))
        apex = '_x{}X{}y{}Y{}'.format(xmin, xmax, ymin, ymax)
        savepath = os.path.abspath(os.path.join(self.config.selectedImgDir, filename + apex + '.jpg'))

        cv2.imwrite(savepath, img[ymin:ymax, xmin:xmax])
        self.selectedRectImgPath = savepath

    ### quad ###
    def mousePress_quadmode(self, pos, parentQSize):
        self._startPosition = pos

        self.quadrangle.set_parentVals(parentQSize=parentQSize)
        self.quadrangle.set_selectPos(pos)

        if self.quadrangle.isSelectedPoint:
            self.moveActionState = MoveActionState.RESIZE
            self._startPosition = self.quadrangle.selectedQPoint
            return

        if self.quadrangle.isSelectedPolygon:
            # if pressed position is contained in parentQSize
            # move the parentQSize
            self.moveActionState = MoveActionState.MOVE

        else:
            # create new parentQSize
            self.moveActionState = MoveActionState.CREATE
            self.quadrangle.append(pos)

    def mouseMoveClicked_quadmode(self, pos, parentQSize: QSize):
        if self.moveActionState == MoveActionState.MOVE:
            movedAmount = pos - self._startPosition
            self.quadrangle.move(movedAmount)
            self._startPosition = pos
            return

        # Note that moveActionState must be CREATE or RESIZE
        # clipping
        pos.setX(min(max(pos.x(), 0), parentQSize.width()))
        pos.setY(min(max(pos.y(), 0), parentQSize.height()))

        if self.moveActionState == MoveActionState.RESIZE:
            self.quadrangle.move_qpoint(self.quadrangle.selectedPointIndex, pos)
            return

        self.quadrangle.move_qpoint(-1, pos)

    def mouseMoveNoButton_quadmode(self, pos):
        self.quadrangle.set_selectPos(pos)
        """
        if self.areamode == AreaMode.SELECTION:
            self.selection.set_selectPos(e.pos())
        elif self.areamode == AreaMode.PREDICTION:
            self.annotation.set_selectPos(e.pos())
        """

    def mouseRelease_quadmode(self):
        self._startPosition = QPoint(0, 0)

    def saveSelectedImg_quadmode(self, imgpath):
        if self.quadrangle.points_number < 4:
            self.selectedQuadImgPath = None
            return

        img = cv2.imread(imgpath)
        h, w, _ = img.shape
        x, y = (self.quadrangle.percent_x * w).astype(int), (self.quadrangle.percent_y * h).astype(int)
        tl, tr, br, bl = tuple(QPoint(x[i], y[i]) for i in range(x.size))

        retqsize = qsize_from_quadrangle((tl, tr, br, bl))

        # affine transform
        src = np.array(((tl.x(), tl.y()), (tr.x(), tr.y()), (bl.x(), bl.y())), dtype=np.float32)
        dst = np.array(((0, 0), (retqsize.width(), 0), (0, retqsize.height())), dtype=np.float32)
        warp_mat = cv2.getAffineTransform(src, dst)
        img_cropped = cv2.warpAffine(img, warp_mat, (retqsize.width(), retqsize.height()))

        # savepath
        filename, ext = os.path.splitext(os.path.basename(imgpath))
        apex = '_tlx{}tly{}trx{}try{}brx{}bry{}blx{}bly{}'.format(tl.x(), tl.y(), tr.x(), tr.y(),
                                                                  br.x(), br.y(), bl.x(), bl.y())
        savepath = os.path.abspath(os.path.join(self.config.selectedImgDir, filename + apex + '.jpg'))

        cv2.imwrite(savepath, img_cropped)
        self.selectedQuadImgPath = savepath


    def clearTmpImg(self):
        # remove all tmp images
        shutil.rmtree(self.config.selectedImgDir)
        os.makedirs(self.config.selectedImgDir)