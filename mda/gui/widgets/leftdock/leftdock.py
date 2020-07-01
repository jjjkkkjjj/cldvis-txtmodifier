from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

from .button import Button, _get_iconpath
from ...functions.dialogs import *
from ..baseWidget import BaseWidget

class LeftDockWidget(BaseWidget):
    imgChanged = Signal(str, int) # emit imgpath and zoomvalue
    ratioChanged = Signal(str, int) # emit imgpath and zoomvalue

    def __init__(self, mainWidget):
        super().__init__(mainWidget)

        self.initUI()
        self.establish_connection()

    def initUI(self):
        vbox = QVBoxLayout()

        ###### open ######
        vbox_open = QVBoxLayout()
        self.groupBox_open = QGroupBox('Open', self)

        self.button_openfolder = Button('folder.png')
        vbox_open.addWidget(self.button_openfolder)

        self.button_openfile = Button('file.png')
        vbox_open.addWidget(self.button_openfile)

        self.groupBox_open.setLayout(vbox_open)
        vbox.addWidget(self.groupBox_open)

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
        vbox.addWidget(self.groupBox_viewer)

        self.setLayout(vbox)

    def establish_connection(self):
        self.button_openfolder.clicked.connect(lambda: self.openDialog('folder'))
        self.button_openfile.clicked.connect(lambda: self.openDialog('file'))

        self.button_zoomin.clicked.connect(lambda: self.buttonZoomClicked(True))
        self.button_zoomout.clicked.connect(lambda: self.buttonZoomClicked(False))

        self.spinBox_zoom.valueChanged.connect(self.spinBoxZoomValueChanged)

    def openDialog(self, opentype):
        if opentype == 'folder':
            filenames = openDir(self)
        elif opentype == 'file':
            filenames = openFiles(self)
        else:
            assert False, "Invalid Error"

        if len(filenames) == 0:
            _ = QMessageBox.warning(self, 'Warning', 'No image files!!', QMessageBox.Ok)
            self.model.set_imgPaths(None)
        else:
            self.model.set_imgPaths(filenames)

        self.imgChanged.emit(self.model.imgpath, self.spinBox_zoom.value())

    def buttonZoomClicked(self, zoomin):
        if zoomin:
            r = min(self.spinBox_zoom.value() + 10, 200)
        else:
            r = max(self.spinBox_zoom.value() - 10, 20)

        self.spinBox_zoom.setValue(r)

    def spinBoxZoomValueChanged(self, value):
        self.ratioChanged.emit(self.model.imgpath, value)