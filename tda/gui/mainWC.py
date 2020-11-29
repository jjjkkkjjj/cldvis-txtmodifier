from PySide2.QtWidgets import *

from .mixin import *

class MainWindowController(SelectionMixin, PredictionMixin, UtilMixin, QMainWindow):
    # static property
    info = Info()
    annotation = Annotation()

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.initUI()
        self.establish_connection()

        self.check_enable()
        self.check_credential()

    def initUI(self):
        self.main = MainWidget(self)
        self.setCentralWidget(self.main)

        self.menu = MenuBar(self)
        self.setMenuBar(self.menu)

    def establish_connection(self):
        SelectionMixin.establish_connection(self)
        PredictionMixin.establish_connection(self)
        UtilMixin.establish_connection(self)

    @property
    def leftdock(self):
        return self.main.leftdock
    @property
    def canvas(self):
        return self.main.canvas
    @property
    def rightdock(self):
        return self.main.rightdock
