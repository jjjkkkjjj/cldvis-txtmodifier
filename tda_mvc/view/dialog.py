from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import glob, os, sys

from ..utils.modes import ExportFileExtention, ExportDatasetFormat
from ..utils.funcs import create_fileters

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        title = 'About Table Data Analyzer'
        self.setWindowTitle(title)

        hbox = QHBoxLayout()

        label_icon = QLabel()
        label_icon.setPixmap(QMessageBox.standardIcon(QMessageBox.Information))
        hbox.addWidget(label_icon)

        label_text = QLabel()
        text = 'Table Data Analyzer uses following icon <br>' \
               'by <a href="https://icons8.com/icons">icons8.com</a>;<br><br>' \
               '<a href="https://icons8.com/icon/XWoSyGbnshH2/file">File icon by Icons8</a><br>' \
               '<a href="https://icons8.com/icon/dINnkNb1FBl4/folder">Folder icon by Icons8</a><br>' \
               '<a href="https://icons8.com/icon/80323/next-page">Next page icon by Icons8</a><br>' \
               '<a href="https://icons8.com/icon/80689/back">Back icon by Icons8</a><br>' \
               '<a href="https://icons8.com/icon/63650/plus">Plus icon by Icons8</a><br>' \
               '<a href="https://icons8.com/icon/12386/minus">Minus icon by Icons8</a><br>' \
               '<a href="https://icons8.com/icon/107448/remove">Remove icon by Icons8</a><br>' \
               '<a href="https://icons8.com/icon/66368/artificial-intelligence">Artificial Intelligence icon by Icons8</a><br>' \
               '<a href="https://icons8.com/icon/107445/export-csv">Export CSV icon by Icons8</a><br>' \
               '' \
               'Icons made by <a href="https://www.flaticon.com/authors/srip" title="srip">srip</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a>'
        label_text.setText(text)
        label_text.setTextFormat(Qt.RichText)
        label_text.setTextInteractionFlags(Qt.TextBrowserInteraction)
        label_text.setOpenExternalLinks(True)
        hbox.addWidget(label_text)

        self.setLayout(hbox)
        self.setFixedSize(400, 300)

class PreferencesDialog(QDialog):

    def __init__(self, model, initial, parent=None):
        super().__init__(parent)



        from ..model import Model
        self.model: Model = model
        self.initial = initial

        self._confignames = ['credentialJsonpath', 'export_defaultFileFormat',
                             'export_sameRowY', 'export_sameColX', 'export_datasetFormat',
                             'export_datasetDir']
        # temporal attr
        # load jsonpath from environment path or config file
        try:
            self.credentialJsonpath = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
        except KeyError:
            if model.credentialJsonpath:
                self.credentialJsonpath = model.credentialJsonpath
            else:
                self.credentialJsonpath = ''
        # None: Not selected
        # False: Can't be loaded
        # True: OK.
        self._isValidJsonPath = None
        self.export_defaultFileFormat = model.config.export_defaultFileFormat
        self.export_sameRowY = model.config.export_sameRowY
        self.export_sameColX = model.config.export_sameColX
        self.export_datasetFormat = model.config.export_datasetFormat
        self.export_datasetDir = model.config.export_datasetDir

        self.initUI()
        self.establish_connection()
        self.updateUI()


    def initUI(self):
        title = 'Preferences'
        self.setWindowTitle(title)

        vbox = QVBoxLayout()

        def setGridLayout(layout, params):
            """
            Set gridlayout
            Parameters
            ----------
            layout : QGridLayout
                The gridlayout
            params : list of list of (widget, column)
                The list of [
                (widget, column, ...),
                (widget, column, ...),
                ]

                Note that row is not needed!!
            Returns
            -------
            """
            for row, row_params in enumerate(params):
                for param in row_params:
                    p = param[1:]
                    layout.addWidget(param[0], row, *p)

        ##### Google Cloud Vision #####
        self.groupBox_gcv = QGroupBox('Google Cloud Vision')
        grid_gcv = QGridLayout()

        self.label_jsonpath = QLabel('Json:')
        self.label_jsonpathStatus = QLabel('Not selected')
        self.label_jsonpathStatusIcon = QLabel()
        self.button_readJsonpath = QPushButton('Read Json')

        layout_params = [
            [
                (self.label_jsonpath, 0, 1, 2),
                (self.label_jsonpathStatus, 2, 1, 4),
                (self.label_jsonpathStatusIcon, 6, 1, 1),
                (self.button_readJsonpath, 7, 1, 1)
            ]
        ]
        setGridLayout(grid_gcv, layout_params)
        self.groupBox_gcv.setLayout(grid_gcv)
        vbox.addWidget(self.groupBox_gcv, 1)

        ##### export ######
        self.groupBox_export = QGroupBox('Export')
        grid_export = QGridLayout()

        self.label_exportfileformat = QLabel('Default File Format:')
        self.comboBox_exportfileformat = QComboBox()
        self.comboBox_exportfileformat.addItems(ExportFileExtention.gen_list())
        self.comboBox_exportfileformat.setCurrentText(self.model.config.export_defaultFileFormat)

        self.label_exportSameRowY = QLabel('Same Rows within:')
        self.spinBox_exportSameRowY = QSpinBox(self)
        self.spinBox_exportSameRowY.setRange(1, 9999)
        self.spinBox_exportSameRowY.setValue(self.model.config.export_sameRowY)
        self.label_exportSameRowYUnit = QLabel('pixel')

        self.label_exportConcatColX = QLabel('Concatenate Columns within:')
        self.spinBox_exportConcatColX = QSpinBox(self)
        self.spinBox_exportConcatColX.setRange(1, 9999)
        self.spinBox_exportConcatColX.setValue(self.model.config.export_sameColX)
        self.label_exportConcatColXUnit = QLabel('pixel')

        self.label_datasetformat = QLabel('Dataset Format:')
        self.comboBox_datasetformat = QComboBox()
        self.comboBox_datasetformat.addItems(ExportDatasetFormat.gen_list())
        self.comboBox_datasetformat.setCurrentText(self.model.config.export_datasetFormat)

        self.label_datasetdir = QLabel('Dataset Directory:')
        self.label_datasetdirStatus = QLabel('Not selected')
        self.label_datasetdirStatusIcon = QLabel()
        self.button_openDatasetDir = QPushButton('Open')

        layout_params = [
            [
                (self.label_exportfileformat, 0, 1, 2),
                (self.comboBox_exportfileformat, 2, 1, 2),
                (QLabel(), 4, 1, 4), # dummy
            ],
            [
                (self.label_exportSameRowY, 1, 1, 2),
                (self.spinBox_exportSameRowY, 3, 1, 2),
                (self.label_exportSameRowYUnit, 5, 1, 2),
            ],
            [
                (self.label_exportConcatColX, 1, 1, 2),
                (self.spinBox_exportConcatColX, 3, 1, 2),
                (self.label_exportConcatColXUnit, 5, 1, 2),
            ],
            [
                (self.label_datasetformat, 0, 1, 2),
                (self.comboBox_datasetformat, 2, 1, 2),
                (QLabel(), 4, 1, 4), # dummy
            ],
            [
                (self.label_datasetdir, 0, 1, 2),
                (self.label_datasetdirStatus, 2, 1, 4),
                (self.label_datasetdirStatusIcon, 6, 1, 1),
                (self.button_openDatasetDir, 7, 1, 1)
            ]
        ]

        setGridLayout(grid_export, layout_params)
        self.groupBox_export.setLayout(grid_export)
        vbox.addWidget(self.groupBox_export, 2)

        self.button_ok = QPushButton('OK')
        self.button_ok.setDefault(True)
        vbox.addWidget(self.button_ok)

        self.setLayout(vbox)
        self.setFixedSize(600, 500)

    def establish_connection(self):
        # google cloud vision
        self.button_readJsonpath.clicked.connect(lambda: self.connection('credentialJsonpath'))

        # export
        self.comboBox_exportfileformat.currentTextChanged.connect(lambda: self.connection('export_defaultFileFormat'))
        self.spinBox_exportSameRowY.valueChanged.connect(lambda: self.connection('export_sameRowY'))
        self.spinBox_exportConcatColX.valueChanged.connect(lambda: self.connection('export_sameColX'))
        self.comboBox_datasetformat.currentTextChanged.connect(lambda: self.connection('export_datasetFormat'))
        self.button_openDatasetDir.clicked.connect(lambda: self.connection('export_datasetDir'))

        self.button_ok.clicked.connect(lambda: self.connection('ok'))

    def updateUI(self):
        self._isValidJsonPath = self.checkJsonpath()

        enable_ok = True

        #### credential json path ####
        if self._isValidJsonPath is None:
            self.label_jsonpathStatus.setText('Not selected')
            icon = self.style().standardIcon(QStyle.SP_MessageBoxWarning)
            enable_ok = enable_ok and False
        elif self._isValidJsonPath:
            self.label_jsonpathStatus.setText(os.path.basename(self.credentialJsonpath))
            icon = self.style().standardIcon(QStyle.SP_DialogApplyButton)
            enable_ok = enable_ok and True
        else:
            self.label_jsonpathStatus.setText('{} is invalid'.format(os.path.basename(self.credentialJsonpath)))
            icon = self.style().standardIcon(QStyle.SP_MessageBoxCritical)
            enable_ok = enable_ok and False
        self.label_jsonpathStatusIcon.setPixmap(icon.pixmap(QSize(16, 16)))

        #### export dataset path ####
        if self.export_datasetDir:
            self.label_datasetdirStatus.setText(self.export_datasetDir)
            icon = self.style().standardIcon(QStyle.SP_DialogApplyButton)
            enable_ok = enable_ok and True
        else:
            self.label_datasetdirStatus.setText('Not selected')
            icon = self.style().standardIcon(QStyle.SP_MessageBoxCritical)
            enable_ok = enable_ok and False
        self.label_datasetdirStatusIcon.setPixmap(icon.pixmap(QSize(16, 16)))

        #### ok ####
        self.button_ok.setEnabled(enable_ok)


    def checkJsonpath(self):
        """
        This method must be called in initialization
        # https://cloud.google.com/vision/docs/ocr
        # https://www.youtube.com/watch?v=HMaoUdJQEgY
        # https://cloud.google.com/vision/docs/pdf
        :param path: str, credential json path
        :return:
            None: Not selected
            False: Can't be loaded
            True: OK.
        """
        if self.credentialJsonpath is None or self.credentialJsonpath == '':
            return None

        return self.model.check_credentialJsonpath(self.credentialJsonpath)

    def connection(self, connecttype):
        if connecttype == 'credentialJsonpath':
            filters_list = create_fileters(('JSON', 'json'))
            filepath, _ = QFileDialog.getOpenFileName(self, 'Open Credential Json File', '', ';;'.join(filters_list), None)

            self.credentialJsonpath = filepath if filepath != '' else None

        elif connecttype == 'export_defaultFileFormat':
            self.export_defaultFileFormat = self.comboBox_exportfileformat.currentText()

        elif connecttype == 'export_sameRowY':
            self.export_sameRowY = self.spinBox_exportSameRowY.value()

        elif connecttype == 'export_sameColX':
            self.export_sameColX = self.spinBox_exportConcatColX.value()

        elif connecttype == 'export_datasetFormat':
            self.export_datasetFormat = self.comboBox_datasetformat.currentText()

        elif connecttype == 'export_datasetDir':
            dirpath = QFileDialog.getExistingDirectory(self, 'Open Dataset Directory to be exported',
                                                       self.model.config.export_datasetDir)
            if dirpath == '':
                return

            self.export_datasetDir = dirpath

        elif connecttype == 'ok':
            ## save
            for attr in self._confignames:
                setattr(self.model.config, attr, getattr(self, attr))
            self.model.set_credentialJsonpath(self.credentialJsonpath)
            self.close()
            return

        self.updateUI()


    def closeEvent(self, event):
        if self.initial and not self._isValidJsonPath:
            sys.exit()
        super().closeEvent(event)

class EditDialog(QDialog):
    edited = Signal(object, str)
    removed = Signal()
    def __init__(self, annotation, parent=None):
        super().__init__(parent)

        self.annoatation = annotation

        self.initUI()
        self.establish_connection()

    def initUI(self):
        title = 'Edit {}'.format(self.annoatation.text)
        self.setWindowTitle(title)

        vbox = QVBoxLayout()
        self.shifhtEnterTextEdit = ShiftEnterTextEdit(self)
        self.shifhtEnterTextEdit.installEventFilter(self)
        self.shifhtEnterTextEdit.setText(self.annoatation.text)
        self.shifhtEnterTextEdit.moveCursor(QTextCursor.End)
        self.shifhtEnterTextEdit.selectAll()
        vbox.addWidget(self.shifhtEnterTextEdit)

        hbox = QHBoxLayout()
        self.button_remove = QPushButton('Remove')
        hbox.addWidget(self.button_remove, 1)
        self.button_cancel = QPushButton('Cancel')
        hbox.addWidget(self.button_cancel, 2)
        self.button_ok = QPushButton('OK')
        self.button_ok.setDefault(True)
        hbox.addWidget(self.button_ok, 2)
        vbox.addLayout(hbox)

        self.setLayout(vbox)


    def establish_connection(self):
        self.shifhtEnterTextEdit.enterKeyPressed.connect(self.okClicked)
        self.button_ok.clicked.connect(self.okClicked)
        self.button_cancel.clicked.connect(self.close)
        self.button_remove.clicked.connect(self.removeClicked)

    def okClicked(self):
        text = self.shifhtEnterTextEdit.toPlainText()
        if self.annoatation.text != text:
            self.edited.emit(self.annoatation, text)
        self.close()

    def removeClicked(self):
        self.removed.emit()
        self.close()

class ShiftEnterTextEdit(QTextEdit):
    enterKeyPressed = Signal(QKeyEvent)
    def keyPressEvent(self, event):
        # shift enter
        if event.modifiers() == Qt.ShiftModifier and event.key() == Qt.Key_Return:
            self.insertPlainText('\n')
            return
        # enter only
        elif event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.enterKeyPressed.emit(event)
            return
        super().keyPressEvent(event)