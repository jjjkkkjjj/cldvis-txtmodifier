from PySide2.QtWidgets import *
from PySide2.QtGui import *


class MenuBar(QMenuBar):
    def __init__(self, mainWidget):
        super().__init__(parent=mainWidget)
        from ..mainWindow import MainWidget

        if not isinstance(mainWidget, MainWidget):
            ValueError('parent must be MainWidget, but got {}'.format(type(mainWidget).__name__))

        self.initUI()
        self.establish_connection(mainWidget)

    def initUI(self):
        self.menu_file = self.addMenu('&File')


    def establish_connection(self, mainWidget):
        # open folder
        self.action_openfolder =  _create_action(self, "&Open Folder", slot=lambda: mainWidget.leftdock.openDialog('folder'),
                                                 shortcut="Ctrl+F", tip="open folder")

        # open files
        self.action_openfiles = _create_action(self, "&Open Files", slot=lambda: mainWidget.leftdock.openDialog('file'),
                                               shortcut="Ctrl+Shift+F", tip="open files")

        _add_actions(self.menu_file, (self.action_openfolder, self.action_openfiles, None))



def _add_actions(target, actions):
    for action in actions:
        if action is None:
            target.addSeparator()
        else:
            target.addAction(action)

def _create_action(self, text, slot=None, shortcut=None,
                  icon=None, tip=None, checkable=False, ):
    action = QAction(text, self)
    if icon is not None:
        action.setIcon(QIcon(":/%s.png" % icon))
    if shortcut is not None:
        action.setShortcut(shortcut)
    if tip is not None:
        action.setToolTip(tip)
        action.setStatusTip(tip)
    if slot is not None:
        action.triggered.connect(slot)
    if checkable:
        action.setCheckable(True)
    return action