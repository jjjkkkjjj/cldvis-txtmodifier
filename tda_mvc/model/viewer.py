from ..utils.modes import PredictionMode, MoveActionState
from ..utils.geometry import *
from .base import ModelAbstractMixin

class ViewerModelMixin(ModelAbstractMixin):
    def __init__(self):
        self.zoomvalue = 100

        # prediction mode
        self.predmode = PredictionMode.IMAGE
        # image mode
        self.rect_imagemode = Rect(points=np.zeros(shape=(2, 2)))
        # table mode
        self.poly_tablemode = Polygon(points=np.zeros(shape=(0, 2)), maximum_points_number=4)
        self.rect_imagemode.hide()
        self.poly_tablemode.hide()

        # start position. this is for moveEvent
        self._startPosition = QPoint(0, 0)

    ### Zoom ###
    @property
    def isZoomOutable(self):
        return self.zoomvalue >= 20 + 10
    @property
    def isZoomInable(self):
        return self.zoomvalue <= 190 - 10

    ### Image ###
    def mousePress_imagemode(self, pos, parentQSize):
        self._startPosition = pos

        self.rect_imagemode.set_parentVals(parentQSize=parentQSize)
        self.rect_imagemode.set_selectPos(pos)

        if self.rect_imagemode.isSelectedPoint:
            # if pressed position is edge
            # expand or shrink parentQSize
            self.moveActionState = MoveActionState.RESIZE
            # [tl, tr, br, bl] -> [br, bl, tl, tr]
            diagIndex = [2, 3, 0, 1]
            diagPos = self.rect_imagemode.qpoints[diagIndex[self.rect_imagemode.selectedPointIndex]]
            self._startPosition = diagPos
            return

        if self.rect_imagemode.isSelectedRect:
            # if pressed position is contained in parentQSize
            # move the parentQSize
            self.moveActionState = MoveActionState.MOVE

        else:
            # create new parentQSize
            self.moveActionState = MoveActionState.CREATE
            qrect = QRect(pos, pos)
            self.rect_imagemode.set_qrect(qrect)

    def mouseMoveClicked_imagemode(self, pos, parentQSize: QSize):
        if self.moveActionState == MoveActionState.MOVE:
            movedAmount = pos - self._startPosition
            self.rect_imagemode.move(movedAmount)
            self._startPosition = pos
            return

        # Note that moveActionState must be CREATE or RESIZE
        if self.moveActionState == MoveActionState.RESIZE:
            # for changing selected Point
            self.rect_imagemode.set_selectPos(pos)

        # clipping
        pos.setX(min(max(pos.x(), 0), parentQSize.width()))
        pos.setY(min(max(pos.y(), 0), parentQSize.height()))

        qrect = QRect(self._startPosition, pos).normalized()
        self.rect_imagemode.set_qrect(qrect)

    def mouseMoveNoButton_imagemode(self, pos):
        self.rect_imagemode.set_selectPos(pos)

    def mouseRelease_imagemode(self):
        if self.moveActionState == MoveActionState.RESIZE:
            self.rect_imagemode.deselect()
        self._startPosition = QPoint(0, 0)

    ### Table ###
    def mousePress_tablemode(self, pos, parentQSize):
        self._startPosition = pos

        self.poly_tablemode.set_parentVals(parentQSize=parentQSize)
        self.poly_tablemode.set_selectPos(pos)

        if self.poly_tablemode.isSelectedPoint:
            self.moveActionState = MoveActionState.RESIZE
            self._startPosition = self.poly_tablemode.selectedQPoint
            return

        if self.poly_tablemode.isSelectedPolygon:
            # if pressed position is contained in parentQSize
            # move the parentQSize
            self.moveActionState = MoveActionState.MOVE

        else:
            # create new parentQSize
            self.moveActionState = MoveActionState.CREATE
            self.poly_tablemode.append(pos)

    def mouseMoveClicked_tablemode(self, pos, parentQSize: QSize):
        if self.moveActionState == MoveActionState.MOVE:
            movedAmount = pos - self._startPosition
            self.poly_tablemode.move(movedAmount)
            self._startPosition = pos
            return

        # Note that moveActionState must be CREATE or RESIZE
        # clipping
        pos.setX(min(max(pos.x(), 0), parentQSize.width()))
        pos.setY(min(max(pos.y(), 0), parentQSize.height()))

        if self.moveActionState == MoveActionState.RESIZE:
            self.poly_tablemode.move_qpoint(self.poly_tablemode.selectedPointIndex, pos)
            # for changing selected Point
            self.poly_tablemode.set_selectPos(pos)
            return
        self.poly_tablemode.move_qpoint(-1, pos)

    def mouseMoveNoButton_tablemode(self, pos):
        self.poly_tablemode.set_selectPos(pos)
        """
        if self.areamode == AreaMode.SELECTION:
            self.selection.set_selectPos(e.pos())
        elif self.areamode == AreaMode.PREDICTION:
            self.annotation.set_selectPos(e.pos())
        """

    def mouseRelease_tablemode(self):
        self._startPosition = QPoint(0, 0)