from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from ..utils.funcs import check_instance, create_action, add_actions
from ..utils.modes import ShowingMode
from ..model import Model
from .leftdock import LeftDockView
from .central import CentralView
from .rightdock import RightDockView

class MainView(QWidget):
    def __init__(self, model, parent=None):
        super().__init__(parent=parent)

        self.model = check_instance('model', model, Model)
        self.initUI()

    def initUI(self):
        self.leftdock = LeftDockView(self.model, self)
        self.central = CentralView(self.model, self)
        self.rightdock = RightDockView(self.model, self)

        # create layout
        hbox = QHBoxLayout()

        # leftdock
        hbox.addWidget(self.leftdock, 1)
        # canvas as central widget
        hbox.addWidget(self.central, 7)
        # rightdock
        hbox.addWidget(self.rightdock, 2)

        self.setLayout(hbox)

class MenuBar(QMenuBar):
    ### Attributes ###
    # menu
    menu_file: QMenu
    menu_edit: QMenu
    menu_viewer: QMenu
    menu_prediction: QMenu
    menu_help: QMenu

    # action
    # file menu
    action_openfolder: QAction
    action_openfiles: QAction
    action_savetda: QAction
    action_saveastda: QAction
    action_loadtda: QAction
    action_backfile: QAction
    action_forwardfile: QAction
    action_exportCSV: QAction
    action_exportDataset: QAction
    action_exit: QAction

    # edit menu
    action_undo: QAction
    action_redo: QAction

    # view menu
    action_zoomin: QAction
    action_zoomout: QAction
    action_showentire: QAction
    action_showselected: QAction

    # prediction menu
    action_predict: QAction
    action_done: QAction
    action_discard: QAction
    action_areaRectMode: QAction
    action_areaQuadMode: QAction
    action_predictImageMode: QAction
    action_predictDocumentMode: QAction

    # help menu
    action_about: QAction
    action_preferences: QAction

    model: Model

    def __init__(self, model: Model, parent=None):
        super().__init__(parent=parent)

        self.model = check_instance('model', model, Model)
        self.initUI()
        self.updateUI()
        self.updateLanguage()

    def initUI(self):
        self.menu_file = self.addMenu('&File')
        self.menu_edit = self.addMenu('&Edit')
        self.menu_viewer = self.addMenu('&View')
        self.menu_prediction = self.addMenu('&Prediction')
        self.menu_help = self.addMenu('&Help')

        ##### File #####
        # open folder
        self.action_openfolder = create_action(self, "&Open Folder", slot=None,
                                                shortcut="Ctrl+O", tip="Open a folder")
        # open files
        self.action_openfiles = create_action(self, "&Open Files", slot=None,
                                               shortcut="Ctrl+Shift+O", tip="Open files")

        # save
        self.action_savetda = create_action(self, "&Save", slot=None,
                                            shortcut="Ctrl+S", tip="Save a tda file in dataset directory")
        # save as tda
        self.action_saveastda = create_action(self, "&Save as tda", slot=None,
                                              shortcut="Ctrl+Shift+S", tip="Save a tda file in specific location")
        # load
        self.action_loadtda = create_action(self, "&Load tda", slot=None,
                                            shortcut="Ctrl+l", tip="Load a tda file from specific location")

        # back file
        self.action_backfile = create_action(self, "&Back File", slot=None,
                                              shortcut="Alt+Left", tip="Back to a previous file")
        # forward file
        self.action_forwardfile = create_action(self, "&Forward File", slot=None,
                                                 shortcut="Alt+Right", tip="Forward to a next file")

        # export csv
        self.action_exportCSV = create_action(self, "&Export File", slot=None,
                                              shortcut="Ctrl+E", tip="Export a file for table to specific location")

        # export dataset
        self.action_exportDataset = create_action(self, "&Export Dataset", slot=None,
                                                  shortcut="Ctrl+Shift+E", tip="Export a file for dataset to specific location")

        # exit
        self.action_exit = create_action(self, "&Exit", slot=None,
                                         shortcut="Ctrl+Q", tip="Quit this application")


        add_actions(self.menu_file, (self.action_openfolder, self.action_openfiles, None,
                                     self.action_savetda, self.action_saveastda, self.action_loadtda, None,
                                     self.action_backfile, self.action_forwardfile, None,
                                     self.action_exportCSV, self.action_exportDataset, None,
                                     self.action_exit))

        ##### Edit #####
        # undo
        self.action_undo = create_action(self, '&Undo', slot=None,
                                         shortcut='Ctrl+Z', tip='Undo')
        # redo
        self.action_redo = create_action(self, '&Redo', slot=None,
                                         shortcut='Ctrl+Y', tip='Redo')

        add_actions(self.menu_edit, (self.action_undo, self.action_redo, None))

        ##### View #####
        # zoom in
        self.action_zoomin = create_action(self, '&Zoom In', slot=None,
                                            shortcut="Ctrl++", tip='Zoom in')
        # zoom out
        self.action_zoomout = create_action(self, '&Zoom Out', slot=None,
                                             shortcut="Ctrl+-", tip='Zoom out')

        # show entire image
        self.action_showentire = create_action(self, '&Show Entire Image', slot=None,
                                                shortcut='Ctrl+Alt+E', tip='Show the entire image')

        # show selected image
        self.action_showselected = create_action(self, '&Show Selected Image', slot=None,
                                                  shortcut='Ctrl+Alt+R', tip='Show the selected image')

        add_actions(self.menu_viewer, (self.action_zoomin, self.action_zoomout, None,
                                        self.action_showentire, self.action_showselected))

        ##### Run #####
        # predict
        self.action_predict = create_action(self, '&Predict Table', slot=None,
                                            shortcut="Ctrl+P", tip='Predict texts through google cloud vision API')
        # done
        self.action_done = create_action(self, '&Done', slot=None,
                                         shortcut="Ctrl+G", tip='Finish editing. Auto save will be done and '
                                                                'default file name will be renamed by appending the sequence number')
        # remove
        self.action_discard = create_action(self, '&Discard', slot=None,
                                            shortcut="Ctrl+D", tip='Discard the rectangle/quadrangle in selection mode\n'
                                                                   'Discard the results in editing annotation mode')

        # area mode
        self.action_areaRectMode = create_action(self, '&Rectangle Mode', slot=None,
                                                  shortcut="r", tip='Use rectangle for prediction')

        self.action_areaQuadMode = create_action(self, '&Quadrangle Mode', slot=None,
                                                  shortcut="q", tip='Use quadrangle for prediction')

        # predict as image mode
        self.action_predictImageMode = create_action(self, '&Image mode', slot=None,
                                                      shortcut='Ctrl+shift+I', tip='Predict texts as Image mode')

        # predict as table mode
        self.action_predictDocumentMode = create_action(self, '&Document mode', slot=None,
                                                         shortcut='Ctrl+shift+D', tip='Predict texts as Document mode')


        add_actions(self.menu_prediction, (self.action_predict, None, self.action_done, self.action_discard, None,
                                           self.action_areaRectMode, self.action_areaQuadMode, None,
                                           self.action_predictImageMode, self.action_predictDocumentMode))

        ##### Help #####
        # about
        self.action_about = create_action(self, '&About', slot=None,
                                           tip='About Table Data Analyzer')

        # preferences
        self.action_preferences = create_action(self, '&Preferences', slot=None,
                                                shortcut="Ctrl+,", tip='Open preferences')

        add_actions(self.menu_help, (self.action_about, None, self.action_preferences))

    def updateUI(self):
        """
        Check if each part is enabled or not
        Returns
        -------

        """
        self.action_predict.setEnabled(self.model.isPredictable and not self.model.isPredicted)
        self.action_done.setEnabled(self.model.isPredicted)
        self.action_discard.setEnabled(self.model.isExistArea)

        self.updateFile()
        self.updateEdit()
        self.updateViewer()
        self.updatePrediction()

    def updateFile(self):
        # save
        self.action_savetda.setEnabled(self.model.isPredicted)
        self.action_saveastda.setEnabled(self.model.isPredicted)
        self.action_loadtda.setEnabled(self.model.isExistImg)
        # open file
        self.action_backfile.setEnabled(self.model.isExistBackImg)
        self.action_forwardfile.setEnabled(self.model.isExistForwardImg)
        # export
        self.action_exportCSV.setEnabled(self.model.isPredicted)
        self.action_exportDataset.setEnabled(self.model.isPredicted)

    def updateEdit(self):
        self.action_undo.setEnabled((self.model.isUndoable and not self.model.isPredicted) or \
                                    (self.model.annotations.isUndoable and self.model.isPredicted))
        self.action_redo.setEnabled((self.model.isRedoable and not self.model.isPredicted) or \
                                    (self.model.annotations.isRedoable and self.model.isPredicted))

    def updateViewer(self):
        self.action_zoomin.setEnabled(self.model.isExistImg and self.model.isZoomInable)
        self.action_zoomout.setEnabled(self.model.isExistImg and self.model.isZoomOutable)
        self.action_showselected.setEnabled(self.model.isPredictable)

    def updatePrediction(self):
        # below is replaced into
        # `not (self.model.showingmode == ShowingMode.SELECTED and not self.model.isRectPredictable)`
        # due to De Morgan's laws
        self.action_areaRectMode.setEnabled((self.model.showingmode == ShowingMode.ENTIRE or self.model.isRectPredictable)
                                            and (not self.model.isPredicted))
        self.action_areaQuadMode.setEnabled((self.model.showingmode == ShowingMode.ENTIRE or self.model.isQuadPredictable)
                                            and (not self.model.isPredicted))

        self.action_predictImageMode.setEnabled(not self.model.isPredicted)
        self.action_predictDocumentMode.setEnabled(not self.model.isPredicted)

    def updateLanguage(self):
        language = self.model.language

        # menu
        self.menu_file.setTitle(language.menu_file)
        self.menu_edit.setTitle(language.menu_edit)
        self.menu_viewer.setTitle(language.menu_viewer)
        self.menu_prediction.setTitle(language.menu_prediction)
        self.menu_help.setTitle(language.menu_help)

        # action
        # file menu
        self.action_openfolder.setText(language.menu_action_openfolder)
        self.action_openfiles.setText(language.menu_action_openfiles)
        self.action_savetda.setText(language.menu_action_savetda)
        self.action_saveastda.setText(language.menu_action_saveastda)
        self.action_loadtda.setText(language.menu_action_loadtda)
        self.action_backfile.setText(language.menu_action_backfile)
        self.action_forwardfile.setText(language.menu_action_forwardfile)
        self.action_exportCSV.setText(language.menu_action_exportCSV)
        self.action_exportDataset.setText(language.menu_action_exportDataset)
        self.action_exit.setText(language.menu_action_exit)

        # edit menu
        self.action_undo.setText(language.menu_action_undo)
        self.action_redo.setText(language.menu_action_redo)

        # view menu
        self.action_zoomin.setText(language.menu_action_zoomin)
        self.action_zoomout.setText(language.menu_action_zoomout)
        self.action_showentire.setText(language.menu_action_showentire)
        self.action_showselected.setText(language.menu_action_showselected)

        # prediction menu
        self.action_predict.setText(language.menu_action_predict)
        self.action_done.setText(language.menu_action_done)
        self.action_discard.setText(language.menu_action_discard)
        self.action_areaRectMode.setText(language.menu_action_areaRectMode)
        self.action_areaQuadMode.setText(language.menu_action_areaQuadMode)
        self.action_predictImageMode.setText(language.menu_action_predictImageMode)
        self.action_predictDocumentMode.setText(language.menu_action_predictDocumentMode)

        # help menu
        self.action_about.setText(language.menu_action_about)
        self.action_preferences.setText(language.menu_action_preferences)

