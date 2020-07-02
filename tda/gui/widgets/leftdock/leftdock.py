from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

from .button import Button, _get_iconpath
from ...functions.dialogs import *
from ..baseWidget import BaseWidget

class LeftDockWidget(BaseWidget):
    imgChanged = Signal(str, int) # emit imgpath and zoomvalue
    ratioChanged = Signal(str, int) # emit imgpath and zoomvalue
    enableChecking = Signal()
    rectRemoved = Signal()

    def __init__(self, mainWidget):
        super().__init__(mainWidget)

        self.initUI()
        self.establish_connection()

    def initUI(self):
        vbox = QVBoxLayout()

        ###### open ######
        # open folder and file
        vbox_open = QVBoxLayout()
        self.groupBox_open = QGroupBox('Open', self)

        self.button_openfolder = Button('folder.png')
        vbox_open.addWidget(self.button_openfolder)

        self.button_openfile = Button('file.png')
        vbox_open.addWidget(self.button_openfile)

        # open back and forward
        hbox_backforward = QHBoxLayout()
        self.button_back = Button('back.png')
        hbox_backforward.addWidget(self.button_back)

        self.button_forward = Button('forward.png')
        hbox_backforward.addWidget(self.button_forward)

        vbox_open.addLayout(hbox_backforward)

        self.groupBox_open.setLayout(vbox_open)
        vbox.addWidget(self.groupBox_open, 1)

        ###### Viewer ######
        vbox_viewer = QVBoxLayout()
        self.groupBox_viewer = QGroupBox('Viewer', self)

        ## zoom in and out ##
        hbox_zoom_auto = QHBoxLayout()
        self.button_zoomin = Button('zoomin.png')
        hbox_zoom_auto.addWidget(self.button_zoomin)

        self.button_zoomout = Button('zoomout.png')
        hbox_zoom_auto.addWidget(self.button_zoomout)
        vbox_viewer.addLayout(hbox_zoom_auto, 1)

        ## zoom manually ##
        self.spinBox_zoom = QSpinBox(self)
        self.spinBox_zoom.setRange(20, 200)
        self.spinBox_zoom.setValue(100)
        vbox_viewer.addWidget(self.spinBox_zoom, 1)

        self.groupBox_viewer.setLayout(vbox_viewer)
        vbox.addWidget(self.groupBox_viewer, 1)

        ##### Run #####
        vbox_run = QVBoxLayout()
        self.groupBox_run = QGroupBox('Run', self)

        # remove
        self.button_removeRect = Button('remove.png')
        vbox_run.addWidget(self.button_removeRect)

        # predict
        self.button_predictTable = Button('predict.png')
        vbox_run.addWidget(self.button_predictTable)

        self.groupBox_run.setLayout(vbox_run)
        vbox.addWidget(self.groupBox_run, 1)

        self.setLayout(vbox)

    def establish_connection(self):
        self.button_openfolder.clicked.connect(lambda: self.openDialog(True))
        self.button_openfile.clicked.connect(lambda: self.openDialog(False))

        self.button_back.clicked.connect(lambda: self.backforward(True))
        self.button_forward.clicked.connect(lambda: self.backforward(False))

        self.button_zoomin.clicked.connect(lambda: self.buttonZoomClicked(True))
        self.button_zoomout.clicked.connect(lambda: self.buttonZoomClicked(False))

        self.button_removeRect.clicked.connect(self.buttonRemoveRectClicked)
        self.button_predictTable.clicked.connect(self.buttonPredictTableClicked)

        self.spinBox_zoom.valueChanged.connect(self.spinBoxZoomValueChanged)

    ##### connection func #####
    def openDialog(self, isFolder):
        if isFolder:
            filenames = openDir(self)
        else:
            filenames = openFiles(self)

        if len(filenames) == 0:
            _ = QMessageBox.warning(self, 'Warning', 'No image files!!', QMessageBox.Ok)
            self.model.set_imgPaths(None)
        else:
            self.model.set_imgPaths(filenames)

        self.imgChanged.emit(self.model.imgpath, self.spinBox_zoom.value())
        self.enableChecking.emit()

    def backforward(self, isBack):
        if isBack:
            self.model.back()
        else:
            self.model.forward()

        self.imgChanged.emit(self.model.imgpath, self.spinBox_zoom.value())
        self.enableChecking.emit()

    def buttonZoomClicked(self, isZoomIn):
        if isZoomIn:
            r = min(self.spinBox_zoom.value() + 10, 200)
        else:
            r = max(self.spinBox_zoom.value() - 10, 20)

        self.spinBox_zoom.setValue(r)

    def spinBoxZoomValueChanged(self, value):
        self.ratioChanged.emit(self.model.imgpath, value)

    def buttonRemoveRectClicked(self):
        self.rectRemoved.emit()

    def buttonPredictTableClicked(self):
        pass

    ##### check enable #####
    def check_enable_backforward(self):
        self.button_back.setEnabled(self.model.isExistBackImg)
        self.button_forward.setEnabled(self.model.isExistForwardImg)

    def check_enable_zoom(self):
        self.spinBox_zoom.setEnabled(self.model.isExistImg)
        self.button_zoomin.setEnabled(self.model.isExistImg)
        self.button_zoomout.setEnabled(self.model.isExistImg)

    def check_enable_run(self):
        self.button_removeRect.setEnabled(self.model.isExistRubberPercentRect)
        self.button_predictTable.setEnabled(self.model.isExistRubberPercentRect)