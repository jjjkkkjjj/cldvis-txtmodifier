from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from .button import Button

class LeftDockWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()

        self.button_openfolder = Button('folder.png')
        vbox.addWidget(self.button_openfolder)

        self.button_openfile = Button('file.png')
        vbox.addWidget(self.button_openfile)

        self.setLayout(vbox)