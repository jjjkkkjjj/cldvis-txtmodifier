from PySide2.QtWidgets import *
from PySide2.QtGui import *

from ..functions.dialogs import openAbout
from .baseWidget import BaseMenuBar
from ._utils import _create_action, _add_actions

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
    def check_enable_backforward(self, isExistBackImg, isExistForwardImg):
        self.action_backfile.setEnabled(isExistBackImg)
        self.action_forwardfile.setEnabled(isExistForwardImg)

    def check_enable_zoom(self, isExistImg):
        self.action_zoomin.setEnabled(isExistImg)
        self.action_zoomout.setEnabled(isExistImg)

    def check_enable_run(self, isExistRubberPercentRect):
        self.action_removeRect.setEnabled(isExistRubberPercentRect)
        self.action_predictTable.setEnabled(isExistRubberPercentRect)


