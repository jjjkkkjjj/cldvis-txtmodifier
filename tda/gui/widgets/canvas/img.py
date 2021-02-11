from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from ..eveUtils import *
from .contextMenu import ImgContextMenu


class ImgWidget(QLabel):
    selectionAreaCreated = Signal(tuple)
    contextActionSelected = Signal(object)
    painting = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.moveActionState = MoveActionState.CREATE
        self.mode = AreaMode.SELECTION

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
        if self.mode == AreaMode.PREDICTION:
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
        if self.mode == AreaMode.SELECTION:
            self.selection.mousePress(self.size(), e.pos())
        elif self.mode == AreaMode.PREDICTION:
            if e.button() == Qt.RightButton:
                pass
        self.repaint()

    def mouseMoveEvent(self, e: QMouseEvent):
        # Note that this method is called earlier than contextMenuEvent
        if isinstance(e, QContextMenuEvent):
            return

        if e.buttons() == Qt.LeftButton:
            if self.mode == AreaMode.SELECTION:
                self.selection.mouseMove(e.pos())

        elif e.buttons() == Qt.NoButton:
            if self.mode == AreaMode.SELECTION:
                self.selection.set_selectPos(e.pos())
            elif self.mode == AreaMode.PREDICTION:
                self.annotation.set_selectPos(e.pos())
        self.repaint()

    def mouseReleaseEvent(self, e: QMouseEvent):
        if self.mode == AreaMode.SELECTION:
            self.selection.mouseRelease()
            self.selectionAreaCreated.emit(self.selection.area.percent_points)
        self.repaint()


    def hide_selectionArea(self):
        self.selection.area.hide()
        self.repaint()

    def switch_areaMode(self, mode):
        self.mode = mode

        if mode == AreaMode.SELECTION:
            return

        elif mode == AreaMode.PREDICTION:
            from ....debug._utils import DEBUG
            if DEBUG:
                # for debug
                # to absolute
                from ...model.geometry import Rect
                import numpy as np
                points = np.array((355/9928.0, 337/7016.0, 2640/9928.0, 1787/7016.0)).reshape(2, 2)
                rect = Rect(points=points, parentQSize=self.pixmap().size())

                self.selection._selectionArea = rect

            self.selection.area.show()


    def paintEvent(self, event):
        if not self.pixmap():
            return super().paintEvent(event)


        # painter
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.pixmap())

        ### draw rubberband parentQSize ###
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

