from PySide2.QtWidgets import *

from . import *

class MainWidget(QWidget):
    def __init__(self, mainWC):
        super().__init__(parent=mainWC)

        self.mainWC = mainWC

        self.initUI()


    def initUI(self):
        # leftdock
        self.leftdock = LeftDockWidget(self.mainWC)

        # canvas as central widget
        self.canvas = CanvasWidget(self.mainWC)

        # rightdock
        self.rightdock = RightDockWidget(self.mainWC)

        self.changeUIRatio(1, 7, 2)


    def changeUIRatio(self, l, c, r):
        layout = self.layout()
        if layout:
            layout.setStretch(0, l)# leftdock
            layout.setStretch(1, c)# canvas
            layout.setStretch(2, r)# rightdock
            return
        # create layout
        hbox = QHBoxLayout(self)

        # leftdock
        hbox.addWidget(self.leftdock, l)

        # canvas as central widget
        hbox.addWidget(self.canvas, c)

        # rightdock
        hbox.addWidget(self.rightdock, r)
        self.setLayout(hbox)
