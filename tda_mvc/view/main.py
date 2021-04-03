from PySide2.QtWidgets import *

from ..utils.funcs import check_instance
from ..model import Model
from .leftdock import LeftDockView
from .central import CentralView

class MainView(QWidget):
    def __init__(self, model, parent=None):
        super().__init__(parent=parent)

        self.model = check_instance('model', model, Model)
        self.initUI()

    def initUI(self):
        self.leftdock = LeftDockView(self.model, self)
        self.central = CentralView(self.model, self)

        # create layout
        hbox = QHBoxLayout()

        # leftdock
        hbox.addWidget(self.leftdock, 1)
        # canvas as central widget
        hbox.addWidget(self.central, 7)
        # rightdock
        # hbox.addWidget(self.rightdock, r)

        self.setLayout(hbox)

class MenuBar(QMenuBar):
    ### Attributes ###
    # menu
    menu_file: QMenu
    menu_viewer: QMenu
    menu_prediction: QMenu
    menu_help: QMenu

    # action
    # file menu
    action_openfolder: QAction
    action_openfiles: QAction
    action_backfile: QAction
    action_forwardfile: QAction

    # viewer menu
    action_zoomin: QAction
    action_zoomout: QAction

    # prediction menu
    action_removeRect: QAction
    action_predictTable: QAction

    # help menu
    action_about: QAction

    def __init__(self, model: Model, parent=None):
        super().__init__(parent=parent)

        self.model = check_instance('model', model, Model)
        self.initUI()

    def initUI(self):
        self.menu_file = self.addMenu('&File')
        self.menu_viewer = self.addMenu('&View')
        self.menu_prediction = self.addMenu('&Run')
        self.menu_help = self.addMenu('&Help')

        ##### File #####
        # open folder
        self.action_openfolder = _create_action(self, "&Open Folder", slot=None,
                                                shortcut="Ctrl+O", tip="open folder")
        # open files
        self.action_openfiles = _create_action(self, "&Open Files", slot=None,
                                               shortcut="Ctrl+Shift+O", tip="open files")

        # back file
        self.action_backfile = _create_action(self, "&Back File", slot=None,
                                              shortcut="Alt+Left", tip="Back file")
        # forward file
        self.action_forwardfile = _create_action(self, "&Forward File", slot=None,
                                                 shortcut="Alt+Right", tip="Forward file")

        _add_actions(self.menu_file, (self.action_openfolder, self.action_openfiles, None,
                                      self.action_backfile, self.action_forwardfile))

        ##### View #####
        # zoom in
        self.action_zoomin = _create_action(self, '&Zoom In', slot=None,
                                            shortcut="Ctrl++", tip='Zoom in')
        # zoom out
        self.action_zoomout = _create_action(self, '&Zoom Out', slot=None,
                                             shortcut="Ctrl+-", tip='Zoom out')

        _add_actions(self.menu_viewer, (self.action_zoomin, self.action_zoomout, None))

        ##### Run #####
        # remove
        self.action_removeRect = _create_action(self, '&Remove Rectangle', slot=None,
                                                shortcut="Ctrl+D", tip='Remove rectangle')
        # predict
        self.action_predictTable = _create_action(self, '&Predict Table', slot=None,
                                                  shortcut="Ctrl+R", tip='Predict table')

        _add_actions(self.menu_prediction, (self.action_removeRect, self.action_predictTable, None))

        ##### Help #####
        # about
        self.action_about = _create_action(self, '&About', slot=None,
                                           tip='about Table Data Analyzer')

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