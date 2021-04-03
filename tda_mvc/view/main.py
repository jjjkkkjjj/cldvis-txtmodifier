from PySide2.QtWidgets import *

from ..utils.funcs import check_instance
from ..model import Model
from .leftdock import LeftDockView

class MainView(QWidget):
    def __init__(self, model, parent=None):
        super().__init__(parent=parent)

        self.model = check_instance('model', model, Model)
        self.initUI()

    def initUI(self):
        self.leftdock = LeftDockView(self.model, self)

        # create layout
        hbox = QHBoxLayout()

        # leftdock
        hbox.addWidget(self.leftdock, 1)
        # canvas as central widget
        # hbox.addWidget(self.canvas, c)
        # rightdock
        # hbox.addWidget(self.rightdock, r)

        self.setLayout(hbox)