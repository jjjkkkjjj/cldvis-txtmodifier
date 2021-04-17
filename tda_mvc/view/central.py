from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import os, cv2

from ..utils.funcs import check_instance, get_pixmap, create_action, add_actions
from ..utils.modes import AreaMode, MoveActionState, ShowingMode
from ..utils.geometry import *
from ..utils.paint import Color, NoColor, transparency, orange
from ..model import Model

class ImageView(QLabel):
    ### Signal ###
    rightClicked = Signal(QContextMenuEvent)
    mousePressed = Signal(QMouseEvent)
    mouseMoved = Signal(QMouseEvent)
    mouseReleased = Signal(QMouseEvent)
    mouseDoubleClicked = Signal(QMouseEvent)

    # model
    model: Model
    def __init__(self, model: Model, parent=None):
        super().__init__(parent)

        self.model = check_instance('model', model, Model)

        self.moveActionState = MoveActionState.CREATE

        # context menu
        self.contextMenu = ImgContextMenu(self.model, self)

        # mouseMoveEvent will be fired on pressing any button
        self.setMouseTracking(True)

    def contextMenuEvent(self, e):
        self.rightClicked.emit(e)

    def mousePressEvent(self, e: QMouseEvent):
        # Note that this method is called earlier than contextMenuEvent
        self.mousePressed.emit(e)

    def mouseMoveEvent(self, e: QMouseEvent):
        # Note that this method is called earlier than contextMenuEvent
        if isinstance(e, QContextMenuEvent):
            return
        self.mouseMoved.emit(e)

    def mouseReleaseEvent(self, e: QMouseEvent):
        self.mouseReleased.emit(e)

    def mouseDoubleClickEvent(self, e: QMouseEvent):
        self.mouseDoubleClicked.emit(e)

    def paintEvent(self, event):
        if not self.pixmap():
            return super().paintEvent(event)

        # painter
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.pixmap())

        # pen
        pen = QPen(QColor(255, 0, 0))
        pen.setWidth(3)

        # set
        painter.setPen(pen)

        if not self.model.isPredicted:
            if self.model.areamode == AreaMode.RECTANGLE:
                self.model.rectangle.paint(painter)
            elif self.model.areamode == AreaMode.QUADRANGLE:
                self.model.quadrangle.paint(painter)
            return

        # predicted
        self.model.predictedArea.paint(painter)
        if self.model.showingmode == ShowingMode.SELECTED:
            self.model.annotations.paint(painter, True)
            return

        # predicted and Entire mode
        if self.model.areamode == AreaMode.RECTANGLE:
            self.model.annotations.paint(painter, True)
        elif self.model.areamode == AreaMode.QUADRANGLE:
            self.model.annotations.paint(painter, False)


class CentralView(QWidget):
    ### Attributes ###
    # label
    label_filename: QLabel

    # image
    scrollArea: QScrollArea
    imageView: ImageView

    # model
    model: Model

    def __init__(self, model: Model, parent=None):
        super().__init__(parent=parent)

        self.model = check_instance('model', model, Model)
        self.initUI()
        self.updateUI()

    def initUI(self):
        vbox = QVBoxLayout()

        # filename label
        self.label_filename = QLabel(self)
        self.label_filename.setText('Filename:')
        vbox.addWidget(self.label_filename)

        # image
        self.scrollArea = QScrollArea(self)
        self.imageView = ImageView(self.model, self)

        self.imageView.setBackgroundRole(QPalette.Base)
        # self.img.setScaledContents(True) # allow to stretch

        # self.scrollArea.setStyleSheet("margin:5px; border:1px solid rgb(0, 0, 0); ")
        self.scrollArea.setWidget(self.imageView)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setBackgroundRole(QPalette.Dark)
        vbox.addWidget(self.scrollArea)

        self.setLayout(vbox)

    def updateUI(self):
        # check enable
        self.label_filename.setEnabled(self.model.isExistImg)
        self.imageView.setEnabled(self.model.isExistImg)

        if self.model.isExistImg:
            # set the filename of the shown image
            self.label_filename.setText('Filename: {}'.format(os.path.basename(self.model.imgpath)))

            # set the image
            pixmap, _ = get_pixmap(self.model, self.scrollArea.size())

            self.imageView.setPixmap(pixmap)

        self.imageView.repaint()
        
class ImgContextMenu(QMenu):
    # model
    model: Model

    def __init__(self, model, parent=None):
        super().__init__(parent)

        self.model = check_instance('model', model, Model)
        self.initUI()
        self.updateUI()

    def initUI(self):
        # annotation
        self.action_remove_annotation = create_action(self, "&Remove Annotation", slot=None,
                                                    tip="remove selected annotation")
        self.action_duplicate_annotation = create_action(self, "&Duplicate Annotation", slot=None,
                                                       tip="duplicate selected annotation")

        # point
        self.action_remove_point = create_action(self, "&Remove Point", slot=None,
                                                    tip="remove selected point")
        self.action_duplicate_point = create_action(self, "&Duplicate Point", slot=None,
                                                       tip="duplicate selected point")

        add_actions(self, (self.action_remove_annotation, self.action_duplicate_annotation, None,
                            self.action_remove_point, self.action_duplicate_point))

    def updateUI(self):
        # annotation
        self.action_remove_annotation.setEnabled(self.model.annotations.isExistSelectedAnnotation)
        self.action_duplicate_annotation.setEnabled(self.model.annotations.isExistSelectedAnnotation)

        # point
        self.action_remove_point.setEnabled(self.model.annotations.isExistSelectedAnnotationPoint)
        self.action_duplicate_point.setEnabled(self.model.annotations.isExistSelectedAnnotationPoint)