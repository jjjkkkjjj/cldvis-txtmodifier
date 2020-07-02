from PySide2.QtWidgets import *

from .widgets import *
from .model import Model
from ..estimator.wrapper import Estimator

class MainWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.initUI()
        self.establish_connection()

        self.model = Model()

    def initUI(self):
        hbox = QHBoxLayout(self)

        # leftdock
        self.leftdock = LeftDockWidget(self)
        hbox.addWidget(self.leftdock, 1)

        # canvas as central widget
        self.canvas = CanvasWidget(self)
        hbox.addWidget(self.canvas, 7)

        # rightdock
        self.rightdock = RightDockWidget(self)
        hbox.addWidget(self.rightdock, 2)
        self.setLayout(hbox)

    def establish_connection(self):
        self.leftdock.imgChanged.connect(self.canvas.set_img)
        self.leftdock.ratioChanged.connect(self.canvas.set_img)
        self.leftdock.rectRemoved.connect(lambda: self.canvas.set_rubber(None))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.establish_connection()
        self.estimator = Estimator()

        self.check_enable()

    def initUI(self):
        self.main = MainWidget(self)
        self.setCentralWidget(self.main)

        self.menu = MenuBar(self.main)
        self.setMenuBar(self.menu)

    def establish_connection(self):
        self.main.leftdock.enableChecking.connect(self.check_enable)
        self.main.canvas.enableChecking.connect(self.check_enable)
        self.main.leftdock.predicting.connect(lambda imgpath, tableRect: self.predict(imgpath, tableRect))

    def check_enable(self):
        # back forward
        self.main.leftdock.check_enable_backforward()
        self.menu.check_enable_backforward()

        # zoom
        self.main.leftdock.check_enable_zoom()
        self.menu.check_enable_zoom()

        # run
        self.main.canvas.check_enable()
        self.main.leftdock.check_enable_run()
        self.menu.check_enable_run()

    def predict(self, imgpath, tableRect):
        pass