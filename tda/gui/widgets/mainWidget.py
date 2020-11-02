from PySide2.QtWidgets import *

from . import *

class MainWidget(QWidget):
    def __init__(self, mainWC):
        super().__init__(parent=mainWC)

        self.mainWC = mainWC

        self.initUI()
        self.establish_connection()


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

    def establish_connection(self):
        self.leftdock.imgChanged.connect(self.canvas.set_img)
        self.leftdock.ratioChanged.connect(self.canvas.set_img)
        self.leftdock.rectRemoved.connect(lambda: self.canvas.set_rubber(None))
        #self.leftdock.datasetAdding.connect()
