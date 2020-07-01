from PySide2.QtWidgets import *

class BaseWidget(QWidget):
    def __init__(self, mainWidget):
        from ..mainWindow import MainWidget

        if not isinstance(mainWidget, MainWidget):
            ValueError('parent must be MainWidget, but got {}'.format(type(mainWidget).__name__))

        super().__init__(parent=mainWidget)
        self.mainWidget = mainWidget