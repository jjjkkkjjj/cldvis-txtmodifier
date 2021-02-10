from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from .rubber import Rubber, PredictedRubber
from ..eveUtils import *
from .contextMenu import ImgContextMenu


class ImgWidget(QLabel):
    rubberCreated = Signal(tuple)
    contextActionSelected = Signal(object)
    painting = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.moveActionState = MoveActionState.CREATE
        self.mode = RubberMode.SELECTION

        # mouseMoveEvent will be fired without any button pressed
        self.setMouseTracking(True)

    @property
    def annotation(self):
        from ...mainWC import MainWindowController
        return MainWindowController.annotation
    @property
    def selection(self):
        from ...mainWC import MainWindowController
        return MainWindowController.selection

    def contextMenuEvent(self, e):
        if self.mode == RubberMode.PREDICTION:
            contextMenu = ImgContextMenu(self)
            contextMenu.setEnabled_action(**self.annotation.enableStatus_contextAction)

            action = contextMenu.exec_(self.mapToGlobal(e.pos()))
            if action == contextMenu.action_remove_annotation:
                self.contextActionSelected.emit(ContextActionType.REMOVE_ANNOTATION)
            elif action == contextMenu.action_duplicate_annotation:
                self.contextActionSelected.emit(ContextActionType.DUPLICATE_ANNOTATION)
            elif action == contextMenu.action_remove_point:
                self.contextActionSelected.emit(ContextActionType.REMOVE_POINT)
            elif action == contextMenu.action_duplicate_point:
                self.contextActionSelected.emit(ContextActionType.DUPLICATE_POINT)


    def mousePressEvent(self, e: QMouseEvent):
        # Note that this method is called earlier than contextMenuEvent
        if self.mode == RubberMode.SELECTION:
            self.selection.mousePress(self.size(), e.pos())
        elif self.mode == RubberMode.PREDICTION:
            if e.button() == Qt.RightButton:
                pass
        self.repaint()

    def mouseMoveEvent(self, e: QMouseEvent):
        # Note that this method is called earlier than contextMenuEvent
        if isinstance(e, QContextMenuEvent):
            return

        if e.buttons() == Qt.LeftButton:
            if self.mode == RubberMode.SELECTION:
                self.selection.mouseMove(e.pos())

        elif e.buttons() == Qt.NoButton:
            if self.mode == RubberMode.PREDICTION:
                self.annotation.set_selectPos(e.pos())
        self.repaint()



    def mouseReleaseEvent(self, e: QMouseEvent):
        if self.mode == RubberMode.SELECTION:
            self.selection.mouseRelease()
        self.repaint()

    def setPixmap(self, pixmap: QPixmap):
        super().setPixmap(pixmap)

        """
        newImgSize = pixmap.size()
        
        # to absolute
        tlX = int(self.left_percent * newImgSize.width())
        tlY = int(self.top_percent * newImgSize.height())
        brX = int(self.right_percent * newImgSize.width())
        brY = int(self.bottom_percent * newImgSize.height())

        newRect = QRect(tlX, tlY, brX - tlX, brY - tlY)

        if self.mode == RubberMode.SELECTION:
            self.rubberBand.setGeometry(newRect)

        elif self.mode == RubberMode.PREDICTION:
            self.predictedRubberBand.setGeometry(newRect)
            offset = newRect.topLeft()
            self.set_qpolygons(newRect.size(), offset)
        """

    def refresh_rubberBand(self):
        self.rubberBand.hide()
        self.rubberBand = Rubber(self)

    def predictedRubber2rubber(self):
        self.rubberBand.show()
        self.predictedRubberBand = PredictedRubber(self)
        self.mode = RubberMode.SELECTION

    def rubber2predictedRubber(self):
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

        self.mode = RubberMode.PREDICTION


    def paintEvent(self, event):
        if not self.pixmap():
            return super().paintEvent(event)


        # painter
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.pixmap())

        ### draw rubberband parentSize ###
        # TODO: rubberband to paint
        #self.predictedRubberBand.hide()

        # pen
        pen = QPen(QColor(255, 0, 0))
        pen.setWidth(3)

        # brush
        #brush = QBrush(QColor(255, 0, 0, int(255*0.4)), Qt.FDiagPattern)

        # set
        painter.setPen(pen)
        #painter.setBrush(brush)

        #painter.drawRect(self.predictedRubberBand.geometry())

        # emit to mixin method
        self.painting.emit(painter)

