from PySide2.QtWidgets import *

from . import *

class MainWidget(QWidget):
    def __init__(self, mainWC):
        super().__init__(parent=mainWC)

        self.mainWC = mainWC

        self.initUI()


    def initUI(self):
        hbox = QHBoxLayout(self)

        # leftdock
        self.leftdock = LeftDockWidget(self.mainWC)
        hbox.addWidget(self.leftdock, 1)

        # canvas as central widget
        self.canvas = CanvasWidget(self.mainWC)
        hbox.addWidget(self.canvas, 7)

        # rightdock
        self.rightdock = RightDockWidget(self.mainWC)
        hbox.addWidget(self.rightdock, 2)
        self.setLayout(hbox)

