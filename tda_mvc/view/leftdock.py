from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

from .parts.button import Button
from ..utils.modes import PredictionMode
from ..utils.funcs import check_instance
from ..model import Model

class LeftDockView(QWidget):
    ### Signal ###


    ### Attributes ###
    # group
    groupBox_file: QGroupBox
    groupBox_viewer: QGroupBox
    groupBox_prediction: QGroupBox

    # open
    button_openfolder: Button
    button_openfile: Button
    button_back: Button
    button_forward: Button

    # viewer
    button_zoomout: Button
    button_zoomin: Button
    spinBox_zoom: QSpinBox
    groupBox_showing: QGroupBox
    radioButton_all: QRadioButton
    radioButton_selected: QRadioButton

    # run
    button_removeRect: Button
    comboBox_predmode: QComboBox
    button_predict: Button

    # model
    model: Model

    def __init__(self, model: Model, parent=None):
        super().__init__(parent=parent)

        self.model = check_instance('model', model, Model)
        self.initUI()
        self.updateUI()


    def initUI(self):
        vbox = QVBoxLayout()

        ###### open ######
        # open folder and file
        vbox_open = QVBoxLayout()
        self.groupBox_file = QGroupBox('Open', self)

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

        self.groupBox_file.setLayout(vbox_open)
        vbox.addWidget(self.groupBox_file, 1)

        ###### Viewer ######
        vbox_viewer = QVBoxLayout()
        self.groupBox_viewer = QGroupBox('Viewer', self)

        ## zoom in and out ##
        hbox_zoom_auto = QHBoxLayout()

        self.button_zoomout = Button('zoomout.png')
        hbox_zoom_auto.addWidget(self.button_zoomout)

        self.button_zoomin = Button('zoomin.png')
        hbox_zoom_auto.addWidget(self.button_zoomin)
        vbox_viewer.addLayout(hbox_zoom_auto, 1)

        ## zoom manually ##
        self.spinBox_zoom = QSpinBox(self)
        self.spinBox_zoom.setRange(20, 200)
        self.spinBox_zoom.setValue(100)
        vbox_viewer.addWidget(self.spinBox_zoom, 1)

        # showing
        vbox_showing = QVBoxLayout()
        self.groupBox_showing = QGroupBox('Showing', self)

        self.radioButton_all = QRadioButton('All')
        self.radioButton_all.setChecked(True)
        vbox_showing.addWidget(self.radioButton_all)

        self.radioButton_selected = QRadioButton('Selected')
        vbox_showing.addWidget(self.radioButton_selected)

        self.groupBox_showing.setLayout(vbox_showing)
        vbox_viewer.addWidget(self.groupBox_showing, 1)

        self.groupBox_viewer.setLayout(vbox_viewer)
        vbox.addWidget(self.groupBox_viewer, 1)

        ##### Run #####
        vbox_run = QVBoxLayout()
        self.groupBox_prediction = QGroupBox('Run', self)

        # remove
        self.button_removeRect = Button('remove.png')
        vbox_run.addWidget(self.button_removeRect)

        # predict
        self.comboBox_predmode = QComboBox(self)
        self.comboBox_predmode.addItems(PredictionMode.gen_list())
        vbox_run.addWidget(self.comboBox_predmode)
        self.button_predict = Button('cloud-vision.png')
        vbox_run.addWidget(self.button_predict)

        # add dataset
        self.button_addDataset = Button('add-dataset.png')
        vbox_run.addWidget(self.button_addDataset)

        self.groupBox_prediction.setLayout(vbox_run)
        vbox.addWidget(self.groupBox_prediction, 1)

        self.setLayout(vbox)

    def updateUI(self):
        """
        Check if each part is enabled or not
        Returns
        -------

        """
        self.updateFileView()

    def updateFileView(self):
        self.button_back.setEnabled(self.model.isExistBackImg)
        self.button_forward.setEnabled(self.model.isExistForwardImg)