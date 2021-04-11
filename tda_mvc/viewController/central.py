from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

from ..utils.modes import AreaMode, ShowingMode
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
        if self.model.isPredicted:
            return

        if self.model.areamode == AreaMode.RECTANGLE:
            self.model.mouseRelease_rectmode()
        elif self.model.areamode == AreaMode.QUADRANGLE:
            self.model.mouseRelease_quadmode()

        self.modelUpdateAftermouseEvent()
        self.leftdock.updateUI()
        self.menu.updateUI()

    def mousePressed(self, e: QMouseEvent):
        if self.model.isPredicted:
            return

        if self.model.areamode == AreaMode.RECTANGLE:
            self.model.mousePress_rectmode(e.pos(), self.imageView.size())

        elif self.model.areamode == AreaMode.QUADRANGLE:
            self.model.mousePress_quadmode(e.pos(), self.imageView.size())

        self.modelUpdateAftermouseEvent()

    def mouseMoved(self, e: QMouseEvent):
        if self.model.isPredicted:
            return

        pos = e.pos()
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