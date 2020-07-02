from PySide2.QtWidgets import *
from PySide2.QtGui import *

from ..functions.dialogs import openAbout


# shortcut list: https://doc.qt.io/qtforpython/PySide2/QtGui/QKeySequence.html
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
        self.menu_view = self.addMenu('&View')
        self.menu_help = self.addMenu('&Help')


    def establish_connection(self, mainWidget):
        ##### File #####
        # open folder
        self.action_openfolder = _create_action(self, "&Open Folder", slot=lambda: mainWidget.leftdock.openDialog('folder'),
                                                 shortcut="Ctrl+O", tip="open folder")

        # open files
        self.action_openfiles = _create_action(self, "&Open Files", slot=lambda: mainWidget.leftdock.openDialog('file'),
                                               shortcut="Ctrl+Shift+O", tip="open files")

        _add_actions(self.menu_file, (self.action_openfolder, self.action_openfiles, None))

        ##### View #####
        # zoom in
        self.action_zoomin = _create_action(self, '&Zoom In', slot=mainWidget.leftdock.button_zoomin.click,
                                            shortcut="Ctrl++", tip='Zoom in')
        # zoom out
        self.action_zoomout = _create_action(self, '&Zoom Out', slot=mainWidget.leftdock.button_zoomout.click,
                                             shortcut="Ctrl+-", tip='Zoom out')

        _add_actions(self.menu_view, (self.action_zoomin, self.action_zoomout, None))

        ##### Help #####
        # about
        self.action_about = _create_action(self, '&About', slot=lambda: openAbout(mainWidget), tip='about Table Data Analyzer')

        _add_actions(self.menu_help, (self.action_about,))

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