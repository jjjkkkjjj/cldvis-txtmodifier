from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

from ..utils.modes import PredictionMode, ShowingMode
from .base import VCAbstractMixin

class CentralVCMixin(VCAbstractMixin):

    @property
    def imageView(self):
        return self.central.imageView

    def establish_connection(self):
        self.imageView.mouseReleased.connect(lambda e: self.mouseReleased(e))
        self.imageView.mousePressed.connect(lambda e: self.mousePressed(e))
        self.imageView.mouseMoved.connect(lambda e: self.mouseMoved(e))

    def mouseReleased(self, e: QMouseEvent):
        if self.model.predmode == PredictionMode.IMAGE:
            self.model.mouseRelease_imagemode()
        elif self.model.predmode == PredictionMode.DOCUMENT:
            self.model.mouseRelease_tablemode()

        self.modelUpdateAftermouseEvent()
        self.leftdock.updateUI()
        self.menu.updateUI()

    def mousePressed(self, e: QMouseEvent):
        if self.model.predmode == PredictionMode.IMAGE:
            self.model.mousePress_imagemode(e.pos(), self.imageView.size())

        elif self.model.predmode == PredictionMode.DOCUMENT:
            self.model.mousePress_tablemode(e.pos(), self.imageView.size())

        self.modelUpdateAftermouseEvent()

    def mouseMoved(self, e: QMouseEvent):
        pos = e.pos()
        if e.buttons() == Qt.LeftButton:
            # in clicking
            if self.model.predmode == PredictionMode.IMAGE:
                self.model.mouseMoveClicked_imagemode(pos, self.imageView.size())
            elif self.model.predmode == PredictionMode.DOCUMENT:
                self.model.mouseMoveClicked_tablemode(pos, self.imageView.size())

        elif e.buttons() == Qt.NoButton:
            if self.model.predmode == PredictionMode.IMAGE:
                self.model.mouseMoveNoButton_imagemode(pos)
            elif self.model.predmode == PredictionMode.DOCUMENT:
                self.model.mouseMoveNoButton_tablemode(pos)

        self.modelUpdateAftermouseEvent()

    def modelUpdateAftermouseEvent(self):
        if self.model.showingmode == ShowingMode.SELECTED:
            self.model.rect_imagemode.hide()
            self.model.poly_tablemode.hide()
            self.imageView.setEnabled(False)

        elif self.model.showingmode == ShowingMode.ENTIRE:
            if self.model.predmode == PredictionMode.IMAGE:
                self.model.rect_imagemode.show()
                self.model.poly_tablemode.hide()
            elif self.model.predmode == PredictionMode.DOCUMENT:
                self.model.rect_imagemode.hide()
                self.model.poly_tablemode.show()
            self.imageView.setEnabled(True)

        self.imageView.repaint()