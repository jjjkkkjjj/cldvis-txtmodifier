from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

from ..utils.modes import AreaMode, ShowingMode
from ..view.dialog import EditDialog
from .base import VCAbstractMixin

class CentralVCMixin(VCAbstractMixin):

    @property
    def imageView(self):
        return self.central.imageView

    def establish_connection(self):
        self.imageView.rightClicked.connect(lambda e: self.rightClicked(e))
        self.imageView.mouseReleased.connect(lambda e: self.mouseReleased(e))
        self.imageView.mousePressed.connect(lambda e: self.mousePressed(e))
        self.imageView.mouseMoved.connect(lambda e: self.mouseMoved(e))
        self.imageView.mouseDoubleClicked.connect(lambda e: self.mouseDoubleClicked(e))

    @property
    def predictedParentQSize(self):
        if self.model.showingmode == ShowingMode.SELECTED:
            return self.imageView.size()
        elif self.model.showingmode == ShowingMode.ENTIRE:
            return self.model.predictedAreaQSize
        return None

    def rightClicked(self, e: QContextMenuEvent):
        if not self.model.isPredicted:
            return

        contextMenu = self.imageView.contextMenu
        contextMenu.updateUI()
        action = contextMenu.exec_(self.imageView.mapToGlobal(e.pos()))
        if action == contextMenu.action_remove_annotation:
            self.model.annotations.remove_selectedAnnotation()
        elif action == contextMenu.action_duplicate_annotation:
            self.model.annotations.duplicate_selectedAnnotation()
        elif action == contextMenu.action_remove_point:
            self.model.annotations.remove_selectedAnnotationPoint()
        elif action == contextMenu.action_duplicate_point:
            self.model.annotations.duplicate_selectedAnnotationPoint()

        self.updateModel()
        self.updateAllUI()


    def mousePressed(self, e: QMouseEvent):
        if self.model.isPredicted:
            self.model.annotations.mousePress(e.pos(), self.predictedParentQSize)

        else:
            if self.model.areamode == AreaMode.RECTANGLE:
                self.model.mousePress_rectmode(e.pos(), self.imageView.size())

            elif self.model.areamode == AreaMode.QUADRANGLE:
                self.model.mousePress_quadmode(e.pos(), self.imageView.size())

        self.modelUpdateAftermouseEvent()

    def mouseMoved(self, e: QMouseEvent):
        pos = e.pos()
        if self.model.isPredicted:
            if e.buttons() == Qt.LeftButton:
                self.model.annotations.mouseMoveClicked(pos, self.predictedParentQSize)
            elif e.buttons() == Qt.NoButton:
                self.model.annotations.mouseMoveNoButton(pos)
                if self.model.annotations.isExistSelectedAnnotation:
                    self.rightdock.tableview.selectRow(self.model.annotations.selectedAnnotationIndex)
        else:
            if e.buttons() == Qt.LeftButton:
                # in clicking
                if self.model.areamode == AreaMode.RECTANGLE:
                    self.model.mouseMoveClicked_rectmode(pos, self.imageView.size())
                elif self.model.areamode == AreaMode.QUADRANGLE:
                    self.model.mouseMoveClicked_quadmode(pos, self.imageView.size())

            elif e.buttons() == Qt.NoButton:
                if self.model.areamode == AreaMode.RECTANGLE:
                    self.model.mouseMoveNoButton_rectmode(pos)
                elif self.model.areamode == AreaMode.QUADRANGLE:
                    self.model.mouseMoveNoButton_quadmode(pos)

        self.modelUpdateAftermouseEvent()

    def mouseReleased(self, e: QMouseEvent):
        if self.model.isPredicted:
            self.model.annotations.mouseRelease()

        else:
            if self.model.areamode == AreaMode.RECTANGLE:
                self.model.mouseRelease_rectmode()
            elif self.model.areamode == AreaMode.QUADRANGLE:
                self.model.mouseRelease_quadmode()

        self.modelUpdateAftermouseEvent()
        self.leftdock.updateUI()
        self.menu.updateUI()

    def mouseDoubleClicked(self, e: QMouseEvent):
        if not self.model.annotations.isExistSelectedAnnotation:
            return

        def edited(annotation, text):
            annotation.set_text(text)
            self.updateAllUI()

        def remove():
            self.model.annotations.remove_selectedAnnotation()
            self.updateModel()
            self.updateAllUI()

        editDialog = EditDialog(self.model.annotations.selectedAnnotation, self)
        editDialog.edited.connect(lambda anno, text: edited(anno, text))
        editDialog.removed.connect(remove)
        editDialog.exec_()

    def modelUpdateAftermouseEvent(self):
        if self.model.showingmode == ShowingMode.SELECTED:
            self.model.rectangle.hide()
            self.model.quadrangle.hide()
            self.imageView.setEnabled(False)

        elif self.model.showingmode == ShowingMode.ENTIRE:
            if self.model.areamode == AreaMode.RECTANGLE:
                self.model.rectangle.show()
                self.model.quadrangle.hide()
            elif self.model.areamode == AreaMode.QUADRANGLE:
                self.model.rectangle.hide()
                self.model.quadrangle.show()
            self.imageView.setEnabled(True)

        self.imageView.repaint()