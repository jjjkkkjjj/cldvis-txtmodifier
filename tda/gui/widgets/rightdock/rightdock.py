from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from ..baseWidget import BaseWidget

class RightDockWidget(BaseWidget):
    def __init__(self, mainWidgetController):
        super().__init__(mainWidgetController)

        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()

        self.label_predict = QLabel(self)
        self.label_predict.setText("Prediction")
        vbox.addWidget(self.label_predict)

        self.textedit = QTextEdit(self)

        vbox.addWidget(self.textedit)

        self.setLayout(vbox)