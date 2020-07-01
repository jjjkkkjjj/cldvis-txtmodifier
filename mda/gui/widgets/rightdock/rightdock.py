from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from ..baseWidget import BaseWidget

class RightDockWidget(BaseWidget):
    def __init__(self, mainWidget):
        super().__init__(mainWidget)

        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()

        self.textedit = QTextEdit(self)

        vbox.addWidget(self.textedit)

        self.setLayout(vbox)