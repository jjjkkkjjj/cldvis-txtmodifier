from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import pathlib

from ..utils.modes import PredictionMode, ShowingMode, AreaMode
from ..utils.funcs import check_instance
from ..model import Model

class Button(QPushButton):
    def __init__(self, icon_filename, parent=None):
        super().__init__(parent=parent)

        icon = QIcon(QPixmap(_get_iconpath(icon_filename)))
        self.setIcon(icon)


def _get_iconpath(icon_filename):
    icondir = pathlib.Path.joinpath(pathlib.Path(__file__).parent.parent, 'icon')
    return str(pathlib.Path.joinpath(icondir, icon_filename))

class LeftDockView(QWidget):
    ### Attributes ###
    # group
    groupBox_file: QGroupBox
    groupBox_view: QGroupBox
    groupBox_prediction: QGroupBox
    groupBox_areamode: QGroupBox

    button_done: Button
    button_predict: Button
    button_discard: Button

    # file
    button_openfolder: Button
    button_openfile: Button
    button_back: Button
    button_forward: Button
    button_exportCSV: Button
    button_exportDataset: Button

    # view
    button_zoomout: Button
    button_zoomin: Button
    spinBox_zoom: QSpinBox
    groupBox_showing: QGroupBox
    radioButton_entire: QRadioButton
    radioButton_selected: QRadioButton

    # run
    radioButton_rect: QRadioButton
    radioButton_quad: QRadioButton

    # predict
    comboBox_predmode: QComboBox


    # model
    model: Model

    def __init__(self, model: Model, parent=None):
        super().__init__(parent=parent)

        self.model = check_instance('model', model, Model)
        self.initUI()
        self.updateUI()
        self.updateLanguage()


    def initUI(self):
        vbox = QVBoxLayout()

        # predict
        self.button_predict = Button('cloud-vision.png')
        vbox.addWidget(self.button_predict)
        # done
        self.button_done = Button('done.png')
        vbox.addWidget(self.button_done)
        # remove
        self.button_discard = Button('remove.png')
        vbox.addWidget(self.button_discard)

        ###### file ######
        # file folder and file
        vbox_file = QVBoxLayout()
        self.groupBox_file = QGroupBox('File', self)

        self.button_openfolder = Button('folder.png')
        vbox_file.addWidget(self.button_openfolder)
        self.button_openfile = Button('file.png')
        vbox_file.addWidget(self.button_openfile)

        # open back and forward
        hbox_backforward = QHBoxLayout()
        self.button_back = Button('back.png')
        hbox_backforward.addWidget(self.button_back)
        self.button_forward = Button('forward.png')
        hbox_backforward.addWidget(self.button_forward)

        vbox_file.addLayout(hbox_backforward)

        # Export csv and dataset
        self.button_exportCSV = Button('export-csv.png')
        vbox_file.addWidget(self.button_exportCSV)
        self.button_exportDataset = Button('export-dataset.png')
        vbox_file.addWidget(self.button_exportDataset)

        self.groupBox_file.setLayout(vbox_file)
        vbox.addWidget(self.groupBox_file, 1)

        ###### View ######
        vbox_view = QVBoxLayout()
        self.groupBox_view = QGroupBox('View', self)

        ## zoom in and out ##
        hbox_zoom_auto = QHBoxLayout()

        self.button_zoomout = Button('zoomout.png')
        hbox_zoom_auto.addWidget(self.button_zoomout)

        self.button_zoomin = Button('zoomin.png')
        hbox_zoom_auto.addWidget(self.button_zoomin)
        vbox_view.addLayout(hbox_zoom_auto, 1)

        ## zoom manually ##
        self.spinBox_zoom = QSpinBox(self)
        self.spinBox_zoom.setRange(20, 200)
        self.spinBox_zoom.setValue(100)
        vbox_view.addWidget(self.spinBox_zoom, 1)

        # showing
        vbox_showing = QVBoxLayout()
        self.groupBox_showing = QGroupBox('Showing', self)

        self.radioButton_entire = QRadioButton('Entire')
        self.radioButton_entire.setChecked(True)
        vbox_showing.addWidget(self.radioButton_entire)

        self.radioButton_selected = QRadioButton('Selected')
        vbox_showing.addWidget(self.radioButton_selected)

        self.groupBox_showing.setLayout(vbox_showing)
        vbox_view.addWidget(self.groupBox_showing, 1)

        self.groupBox_view.setLayout(vbox_view)
        vbox.addWidget(self.groupBox_view, 1)

        ##### Run #####
        vbox_run = QVBoxLayout()
        self.groupBox_prediction = QGroupBox('Prediction', self)

        # area mode
        vbox_areamode = QVBoxLayout()
        self.groupBox_areamode = QGroupBox('Area Mode', self)

        self.radioButton_rect = QRadioButton('Rectangle')
        vbox_areamode.addWidget(self.radioButton_rect)

        self.radioButton_quad = QRadioButton('Quadrangle')
        vbox_areamode.addWidget(self.radioButton_quad)
        if self.model.areamode == AreaMode.RECTANGLE:
            self.radioButton_rect.setChecked(True)
        elif self.model.areamode == AreaMode.QUADRANGLE:
            self.radioButton_quad.setChecked(True)

        self.groupBox_areamode.setLayout(vbox_areamode)
        vbox_run.addWidget(self.groupBox_areamode, 1)


        # predict
        self.comboBox_predmode = QComboBox(self)
        self.comboBox_predmode.addItems(PredictionMode.gen_list())
        vbox_run.addWidget(self.comboBox_predmode)
        self.comboBox_predmode.setCurrentText(self.model.predmode.value)

        self.groupBox_prediction.setLayout(vbox_run)
        vbox.addWidget(self.groupBox_prediction, 1)

        self.setLayout(vbox)

    def updateUI(self):
        """
        Check if each part is enabled or not
        Returns
        -------

        """
        self.button_predict.setEnabled(self.model.isPredictable and not self.model.isPredicted)
        self.button_done.setEnabled(self.model.isPredicted)
        self.button_discard.setEnabled(self.model.isExistArea)

        self.updateFile()
        self.updateView()
        self.updatePrediction()

    def updateFile(self):
        # open file
        self.button_back.setEnabled(self.model.isExistBackImg)
        self.button_forward.setEnabled(self.model.isExistForwardImg)
        # export
        self.button_exportCSV.setEnabled(self.model.isPredicted)
        self.button_exportDataset.setEnabled(self.model.isPredicted)

    def updateView(self):
        self.spinBox_zoom.setEnabled(self.model.isExistImg)
        self.button_zoomin.setEnabled(self.model.isExistImg and self.model.isZoomInable)
        self.button_zoomout.setEnabled(self.model.isExistImg and self.model.isZoomOutable)
        self.radioButton_selected.setEnabled(self.model.isPredictable)

    def updatePrediction(self):
        # below is replaced into
        # `not (self.model.showingmode == ShowingMode.SELECTED and not self.model.isRectPredictable)`
        # due to De Morgan's laws
        self.radioButton_rect.setEnabled(self.model.showingmode == ShowingMode.ENTIRE or self.model.isRectPredictable)
        self.radioButton_quad.setEnabled(self.model.showingmode == ShowingMode.ENTIRE or self.model.isQuadPredictable)

        # if the image has already predicted, disable
        self.groupBox_areamode.setEnabled(not self.model.isPredicted)
        self.comboBox_predmode.setEnabled(not self.model.isPredicted)

    def updateLanguage(self):
        language = self.model.language

        self.groupBox_file.setTitle(language.leftdock_file)
        self.groupBox_view.setTitle(language.leftdock_view)
        self.groupBox_showing.setTitle(language.leftdock_showing)
        self.radioButton_entire.setText(language.leftdock_entire)
        self.radioButton_selected.setText(language.leftdock_selected)
        self.groupBox_prediction.setTitle(language.leftdock_prediction)
        self.groupBox_areamode.setTitle(language.leftdock_areamode)
        self.radioButton_rect.setText(language.leftdock_rectangle)
        self.radioButton_quad.setText(language.leftdock_quadrangle)
        for i, text in enumerate(language.leftdock_predmode):
            self.comboBox_predmode.setItemText(i, text)

