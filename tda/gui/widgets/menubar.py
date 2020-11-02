from PySide2.QtWidgets import *
from PySide2.QtGui import *

from ..functions.dialogs import openAbout
from .baseWidget import BaseMenuBar


# shortcut list: https://doc.qt.io/qtforpython/PySide2/QtGui/QKeySequence.html
class MenuBar(BaseMenuBar):
    def __init__(self, mainWC):
        super().__init__(mainWC)

        self.initUI()
        self.establish_connection()

    def initUI(self):
        self.menu_file = self.addMenu('&File')
        self.menu_view = self.addMenu('&View')
        self.menu_run = self.addMenu('&Run')
        self.menu_help = self.addMenu('&Help')


    def establish_connection(self):
        ##### File #####
        # open folder
        self.action_openfolder = _create_action(self, "&Open Folder", slot=lambda: self.mainWC.leftdock.openDialog(True),
                                                shortcut="Ctrl+O", tip="open folder")
        # open files
        self.action_openfiles = _create_action(self, "&Open Files", slot=lambda: self.mainWC.leftdock.openDialog(False),
                                               shortcut="Ctrl+Shift+O", tip="open files")

        # back file
        self.action_backfile = _create_action(self, "&Back File", slot=lambda: self.mainWC.leftdock.backforward(True),
                                              shortcut="Alt+Left", tip="Back file")
        # forward file
        self.action_forwardfile = _create_action(self, "&Forward File", slot=lambda: self.mainWC.leftdock.backforward(False),
                                                 shortcut="Alt+Right", tip="Forward file")

        _add_actions(self.menu_file, (self.action_openfolder, self.action_openfiles, None, self.action_backfile, self.action_forwardfile))

        ##### View #####
        # zoom in
        self.action_zoomin = _create_action(self, '&Zoom In', slot=self.mainWC.leftdock.button_zoomin.click,
                                            shortcut="Ctrl++", tip='Zoom in')
        # zoom out
        self.action_zoomout = _create_action(self, '&Zoom Out', slot=self.mainWC.leftdock.button_zoomout.click,
                                             shortcut="Ctrl+-", tip='Zoom out')

        _add_actions(self.menu_view, (self.action_zoomin, self.action_zoomout, None))

        ##### Run #####
        # remove
        self.action_removeRect = _create_action(self, '&Remove Rectangle', slot=self.mainWC.leftdock.button_removeRect.click,
                                                shortcut="Ctrl+D", tip='Remove rectangle')
        # predict
        self.action_predictTable = _create_action(self, '&Predict Table', slot=self.mainWC.leftdock.button_predictTable.click,
                                                  shortcut="Ctrl+R", tip='Predict table')

        _add_actions(self.menu_run, (self.action_removeRect, self.action_predictTable, None))

        ##### Help #####
        # about
        self.action_about = _create_action(self, '&About', slot=lambda: openAbout(self.mainWC), tip='about Table Data Analyzer')

        _add_actions(self.menu_help, (self.action_about,))

    ##### check enable #####
    def check_enable_backforward(self):
        self.action_backfile.setEnabled(self.model.isExistBackImg)
        self.action_forwardfile.setEnabled(self.model.isExistForwardImg)

    def check_enable_zoom(self):
        self.action_zoomin.setEnabled(self.model.isExistImg)
        self.action_zoomout.setEnabled(self.model.isExistImg)

    def check_enable_run(self):
        self.action_removeRect.setEnabled(self.model.isExistRubberPercentRect)
        self.action_predictTable.setEnabled(self.model.isExistRubberPercentRect)


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