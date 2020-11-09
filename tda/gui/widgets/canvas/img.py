from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from enum import Enum

from .rubber import Rubber, MoveActionState, PredictedRubber
from .polygon import Polygon, PolygonManager

class ImgWidget(QLabel):
    rubberCreated = Signal(tuple)
    def __init__(self, parent=None):
        super().__init__(parent)

        self.startPosition = None

        self.moveActionState = MoveActionState.CREATE
        self.mode = RubberMode.SELECTION

        self.rubberBand = Rubber(self)
        self.rubberPercentRect = (0., 0., 0., 0.)

        self.predictedRubberBand = PredictedRubber(self)

        self.polygons = PolygonManager(offset=(0, 0))

    @property
    def left_percent(self):
        return self.rubberPercentRect[0]
    @property
    def top_percent(self):
        return self.rubberPercentRect[1]
    @property
    def right_percent(self):
        return self.rubberPercentRect[2]
    @property
    def bottom_percent(self):
        return self.rubberPercentRect[3]

    def mousePressEvent(self, e: QMouseEvent):
        if self.mode == RubberMode.SELECTION:
            self.startPosition, self.moveActionState = self.rubberBand.press(e.pos())

    def mouseMoveEvent(self, e: QMouseEvent):
        endPosition = e.pos()
        if self.mode == RubberMode.SELECTION:
            if self.moveActionState == MoveActionState.MOVE:  # move
                movedPosition = endPosition - self.startPosition
                # clipping
                movedPosition.setX(min(max(movedPosition.x(), 0), self.geometry().width() - self.rubberBand.width()))
                movedPosition.setY(min(max(movedPosition.y(), 0), self.geometry().height() - self.rubberBand.height()))
                self.rubberBand.move(movedPosition)
            else:
                # clipping
                endPosition.setX(min(max(endPosition.x(), 0), self.geometry().width()))
                endPosition.setY(min(max(endPosition.y(), 0), self.geometry().height()))

                self.rubberBand.setGeometry(QRect(self.startPosition, endPosition).normalized())


    def mouseReleaseEvent(self, e: QMouseEvent):
        if self.mode == RubberMode.SELECTION:
            rect = self.rubberBand.geometry()
            self.rubberBand.setGeometry(rect)

            self.rubberPercentRect = (self.rubberBand.geometry().left()/self.width(), self.rubberBand.geometry().top()/self.height(),
                                      self.rubberBand.geometry().right()/self.width(), self.rubberBand.geometry().bottom()/self.height())

            self.startPosition = None
            self.rubberCreated.emit(self.rubberPercentRect)

    def setPixmap(self, pixmap: QPixmap):
        super().setPixmap(pixmap)

        newImgSize = pixmap.size()

        # to absolute
        tlX = int(self.left_percent * newImgSize.width())
        tlY = int(self.top_percent * newImgSize.height())
        brX = int(self.right_percent * newImgSize.width())
        brY = int(self.bottom_percent * newImgSize.height())

        newRect = QRect(tlX, tlY, brX - tlX, brY - tlY)

        if self.rubberBand.isHidden():
            self.predictedRubberBand.setGeometry(newRect)
        else:
            self.rubberBand.setGeometry(newRect)


    def refresh_rubberBand(self):
        self.rubberBand.hide()
        self.rubberBand = Rubber(self)

    def predictedRubber2rubber(self):
        self.rubberBand.show()
        self.predictedRubberBand = PredictedRubber(self)
        self.mode = RubberMode.SELECTION

    def rubber2predictedRubber(self, results):
        self.rubberBand.hide()

        from ....debug._utils import DEBUG
        if DEBUG:
            # for debug
            # to absolute
            self.rubberPercentRect = (355/9928.0, 337/7016.0, 2640/9928.0, 1787/7016.0)
            tlX = int(self.left_percent * self.pixmap().width())
            tlY = int(self.top_percent * self.pixmap().height())
            brX = int(self.right_percent * self.pixmap().width())
            brY = int(self.bottom_percent * self.pixmap().height())

            rect = QRect(tlX, tlY, brX - tlX, brY - tlY)
            self.predictedRubberBand.setGeometry(rect)
        else:
            self.predictedRubberBand.setGeometry(self.rubberBand.geometry())
        
        self.predictedRubberBand.show()

        """
        results: dict
            "info":
                "width": int
                "height": int
                "path": str
            "prediction": list of dict whose keys are 'text' and 'bbox'
                "text": str
                "bbox": list(4 points) of list(2d=(x, y))
        """

        self.polygons.set_offset(self.predictedRubberBand.geometry().topLeft())
        # create polygon instances, and then draw polygons
        for result in results["prediction"]:
            self.polygons.append(Polygon(result["bbox"]))

        self.mode = RubberMode.PREDICTION

        # draw polygons
        self.repaint()

    def paintEvent(self, event):
        if not self.pixmap() or self.mode == RubberMode.SELECTION:
            return super().paintEvent(event)

        # pen
        pen = QPen(QColor(0,0,0))
        pen.setWidth(3)

        # brush
        brush = QBrush(QColor(0, 255, 0, 0.4))

        # painter
        painter = QPainter(self)
        painter.setPen(pen)
        painter.setBrush(brush)

        newImgSize = self.pixmap().size()

        for polygon in self.polygons.qpolygons():
            painter.drawPolygon(polygon)

        return super().paintEvent(event)

class RubberMode(Enum):
    SELECTION = 0
    PREDICTION = 1