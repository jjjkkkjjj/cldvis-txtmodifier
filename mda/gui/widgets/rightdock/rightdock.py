from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

class RightDockWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()

        self.textedit = QTextEdit(self)

        vbox.addWidget(self.textedit)

        self.setLayout(vbox)