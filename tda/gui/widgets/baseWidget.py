from PySide2.QtWidgets import *

class BaseWidget(QWidget):
    def __init__(self, mainWC):
        from ..mainWC import MainWindowController

        if not isinstance(mainWC, MainWindowController):
            ValueError('argument must be MainWidgetController, but got {}'.format(type(mainWC).__name__))

        super().__init__(parent=mainWC)
        self.mainWC = mainWC

    @property
    def model(self):
        return self.mainWC.model

class BaseMenuBar(QMenuBar):
    def __init__(self, mainWC):
        from ..mainWC import MainWindowController

        if not isinstance(mainWC, MainWindowController):
            ValueError('argument must be MainWidgetController, but got {}'.format(type(mainWC).__name__))

        super().__init__(parent=mainWC)
        self.mainWC = mainWC

    @property
    def model(self):
        return self.mainWC.model