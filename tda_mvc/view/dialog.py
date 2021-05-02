from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import glob, os, sys, math

from ..utils.modes import ExportFileExtention, ExportDatasetFormat, PredictionMode, AreaMode, LanguageMode
from ..utils.funcs import create_fileters
from ..model.language import *

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        title = 'About cldvis'
        self.setWindowTitle(title)

        hbox = QHBoxLayout()

        label_icon = QLabel()
        label_icon.setPixmap(QMessageBox.standardIcon(QMessageBox.Information))
        hbox.addWidget(label_icon)

        label_text = QLabel()
        text = 'cldvis uses following icons <br>' \
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
               'Icons made by <a href="https://www.flaticon.com/authors/srip" title="srip">srip</a>, ' \
               '<a href="https://www.flaticon.com/authors/roundicons" title="Roundicons">Roundicons</a>' \
               'from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a>'
        label_text.setText(text)
        label_text.setTextFormat(Qt.RichText)
        label_text.setTextInteractionFlags(Qt.TextBrowserInteraction)
        label_text.setOpenExternalLinks(True)
        hbox.addWidget(label_text)

        self.setLayout(hbox)
        self.setFixedSize(400, 300)

class PreferencesDialog(QDialog):
    setCredentialJsonpath = Signal(str)
    languageChanged = Signal()
    def __init__(self, model, initial, parent=None):
        super().__init__(parent)

        from ..model import Model
        self.model: Model = model
        self.initial = initial

        self._confignames = ['languagemode', 'defaultareamode', 'defaultpredmode',
                             'credentialJsonpath', 'export_defaultFileFormat',
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

        self.languagemode = model.config.languagemode
        self.defaultareamode = model.config.defaultareamode
        self.defaultpredmode = model.config.defaultpredmode

        self.export_defaultFileFormat = model.config.export_defaultFileFormat
        self.export_sameRowY = model.config.export_sameRowY
        self.export_sameColX = model.config.export_sameColX
        self.export_datasetFormat = model.config.export_datasetFormat
        self.export_datasetDir = model.config.export_datasetDir

        self.initUI()
        self.establish_connection()
        self.updateUI()
        self.updateLanguage()

    @property
    def language(self):
        if self.languagemode == 'English':
            return English
        elif self.languagemode == 'Japanese':
            return Japanese

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

        ##### Basic Settings #####
        self.groupBox_basic = QGroupBox('Basic Settings')
        grid_basic = QGridLayout()

        self.label_languagemode = QLabel('Language:')
        self.comboBox_languagemode = QComboBox()
        self.comboBox_languagemode.addItems(LanguageMode.gen_list())
        self.comboBox_languagemode.setCurrentText(self.model.config.languagemode)

        self.label_defaultareamode = QLabel('Default Area mode:')
        self.comboBox_defaultareamode = QComboBox()
        self.comboBox_defaultareamode.addItems(AreaMode.gen_list())
        self.comboBox_defaultareamode.setCurrentText(self.model.config.defaultareamode)

        self.label_defaultpredmode = QLabel('Default Prediction mode:')
        self.comboBox_defaultpredmode = QComboBox()
        self.comboBox_defaultpredmode.addItems(PredictionMode.gen_list())
        self.comboBox_defaultpredmode.setCurrentText(self.model.config.defaultpredmode)

        layout_params = [
            [
                (self.label_languagemode, 0, 1, 2),
                (self.comboBox_languagemode, 2, 1, 2),
                (QLabel(), 4, 1, 4),  # dummy
            ],
            [
                (self.label_defaultareamode, 0, 1, 2),
                (self.comboBox_defaultareamode, 2, 1, 2),
                (QLabel(), 4, 1, 4), # dummy
            ],
            [
                (self.label_defaultpredmode, 0, 1, 2),
                (self.comboBox_defaultpredmode, 2, 1, 2),
                (QLabel(), 4, 1, 4),  # dummy
            ]
        ]
        setGridLayout(grid_basic, layout_params)
        self.groupBox_basic.setLayout(grid_basic)
        vbox.addWidget(self.groupBox_basic, 1)


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
        # basic settings
        self.comboBox_languagemode.currentIndexChanged.connect(lambda: self.connection('languagemode'))
        self.comboBox_defaultareamode.currentIndexChanged.connect(lambda: self.connection('defaultareamode'))
        self.comboBox_defaultpredmode.currentIndexChanged.connect(lambda: self.connection('defaultpredmode'))

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
        if self._isValidJsonPath:
            self.setCredentialJsonpath.emit(self.credentialJsonpath)

        enable_ok = True

        #### credential json path ####
        if self._isValidJsonPath is None:
            self.label_jsonpathStatus.setText(self.language.pref_notselected)
            icon = self.style().standardIcon(QStyle.SP_MessageBoxWarning)
            enable_ok = enable_ok and False
        elif self._isValidJsonPath:
            self.label_jsonpathStatus.setText(os.path.basename(self.credentialJsonpath))
            icon = self.style().standardIcon(QStyle.SP_DialogApplyButton)
            enable_ok = enable_ok and True
        else:
            self.label_jsonpathStatus.setText(self.language.pref_jsonInvalidStatus.format(os.path.basename(self.credentialJsonpath)))
            icon = self.style().standardIcon(QStyle.SP_MessageBoxCritical)
            enable_ok = enable_ok and False
        self.label_jsonpathStatusIcon.setPixmap(icon.pixmap(QSize(16, 16)))

        #### export dataset path ####
        if self.export_datasetDir:
            self.label_datasetdirStatus.setText(self.export_datasetDir)
            icon = self.style().standardIcon(QStyle.SP_DialogApplyButton)
            enable_ok = enable_ok and True
        else:
            self.label_datasetdirStatus.setText(self.language.pref_notselected)
            icon = self.style().standardIcon(QStyle.SP_MessageBoxCritical)
            enable_ok = enable_ok and False
        self.label_datasetdirStatusIcon.setPixmap(icon.pixmap(QSize(16, 16)))

        #### ok ####
        self.button_ok.setEnabled(enable_ok)

    def updateLanguage(self):
        language = self.language

        self.setWindowTitle(language.pref_title)
        self.groupBox_basic.setTitle(language.pref_basic)
        self.label_languagemode.setText(language.pref_languagemode)
        for i, val in enumerate(language.languagemode_list):
            self.comboBox_languagemode.setItemText(i, val)
        self.label_defaultareamode.setText(language.pref_defaultareamode)
        for i, val in enumerate(language.areamode_list):
            self.comboBox_defaultareamode.setItemText(i, val)
        self.label_defaultpredmode.setText(language.pref_defaultpredmode)
        for i, val in enumerate(language.predmode_list):
            self.comboBox_defaultpredmode.setItemText(i, val)
        self.button_readJsonpath.setText(language.pref_readJsonpath)
        self.groupBox_export.setTitle(language.pref_export)
        self.label_exportfileformat.setText(language.pref_exportfileformat)
        self.label_exportSameRowY.setText(language.pref_exportSameRowY)
        self.label_exportConcatColX.setText(language.pref_exportConcatColX)
        self.label_datasetformat.setText(language.pref_datasetformat)
        self.label_datasetdir.setText(language.pref_datasetdir)
        self.button_openDatasetDir.setText(language.open)
        self.button_ok.setText(language.ok)



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
        if connecttype == 'languagemode':
            self.languagemode = LanguageMode.gen_list()[self.comboBox_languagemode.currentIndex()]
            self.updateUI()
            self.updateLanguage()

        elif connecttype == 'defaultareamode':
            self.defaultareamode = AreaMode.gen_list()[self.comboBox_defaultareamode.currentIndex()]

        elif connecttype == 'defaultpredmode':
            self.defaultpredmode = PredictionMode.gen_list()[self.comboBox_defaultpredmode.currentIndex()]

        elif connecttype == 'credentialJsonpath':
            filters_list = create_fileters(('JSON', 'json'))
            filepath, _ = QFileDialog.getOpenFileName(self, self.language.pref_openjsonfile, '', ';;'.join(filters_list), None)

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
            dirpath = QFileDialog.getExistingDirectory(self, self.language.pref_opendatasetdir,
                                                       self.model.config.export_datasetDir)
            if dirpath == '':
                return

            self.export_datasetDir = dirpath

        elif connecttype == 'ok':
            # check if the languagemode is changed or not
            prevLanguagemode = self.model.config.languagemode

            ## save
            for attr in self._confignames:
                setattr(self.model.config, attr, getattr(self, attr))
            self.model.set_credentialJsonpath(self.credentialJsonpath)

            # emit
            if prevLanguagemode != self.model.config.languagemode:
                self.languageChanged.emit()

            self.close()
            return

        self.updateUI()


    def closeEvent(self, event):
        if self.initial and not self._isValidJsonPath:
            sys.exit()
        super().closeEvent(event)

class EditDialog(QDialog):
    edited = Signal(str)
    removed = Signal()
    def __init__(self, model, parent=None):
        super().__init__(parent)

        from ..model import Model
        self.model: Model = model

        self.initUI()
        self.establish_connection()
        self.updateLanguage()

    @property
    def annotation(self):
        return self.model.annotations.selectedAnnotation

    def initUI(self):
        title = 'Edit {}'.format(self.annotation.text)
        self.setWindowTitle(title)

        vbox = QVBoxLayout()
        self.shifhtEnterTextEdit = ShiftEnterTextEdit(self)
        self.shifhtEnterTextEdit.installEventFilter(self)
        self.shifhtEnterTextEdit.setText(self.annotation.text)
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

    def updateLanguage(self):
        language = self.model.language

        title = language.edittext.format(self.annotation.text)
        self.setWindowTitle(title)
        self.button_remove.setText(language.remove)
        self.button_cancel.setText(language.cancel)
        self.button_ok.setText(language.ok)


    def okClicked(self):
        text = self.shifhtEnterTextEdit.toPlainText()
        if self.annotation.text != text:
            self.edited.emit(text)
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


# https://github.com/fbjorn/QtWaitingSpinner/blob/master/pyqtspinner/spinner.py
class WaitingWidget(QWidget):
    def __init__(self, parent, centerOnParent=True, disableParentWhenSpinning=False,
                 modality=Qt.NonModal, roundness=100., opacity=None, fade=80., lines=20,
                 line_length=10, line_width=2, radius=10, speed=math.pi / 2, color=(0, 0, 0)):
        super().__init__(parent)

        self._centerOnParent = centerOnParent
        self._disableParentWhenSpinning = disableParentWhenSpinning

        self._color = QColor(*color)
        self._roundness = roundness
        self._minimumTrailOpacity = math.pi
        self._trailFadePercentage = fade
        self._revolutionsPerSecond = speed
        self._numberOfLines = lines
        self._lineLength = line_length
        self._lineWidth = line_width
        self._innerRadius = radius
        self._currentCounter = 0
        self._isSpinning = False

        self._timer = QTimer(self)
        self._timer.timeout.connect(self.rotate)
        self.updateSize()
        self.updateTimer()
        self.hide()

        self.setWindowModality(modality)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def paintEvent(self, QPaintEvent):
        self.updatePosition()
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.transparent)
        painter.setRenderHint(QPainter.Antialiasing, True)

        if self._currentCounter >= self._numberOfLines:
            self._currentCounter = 0

        painter.setPen(Qt.NoPen)
        for i in range(self._numberOfLines):
            painter.save()
            painter.translate(self._innerRadius + self._lineLength, self._innerRadius + self._lineLength)
            rotateAngle = float(360 * i) / float(self._numberOfLines)
            painter.rotate(rotateAngle)
            painter.translate(self._innerRadius, 0)
            distance = self.lineCountDistanceFromPrimary(i, self._currentCounter, self._numberOfLines)
            color = self.currentLineColor(
                distance,
                self._numberOfLines,
                self._trailFadePercentage,
                self._minimumTrailOpacity,
                self._color
            )
            painter.setBrush(color)
            painter.drawRoundedRect(
                QRect(0, -self._lineWidth / 2, self._lineLength, self._lineWidth),
                self._roundness,
                self._roundness,
                Qt.RelativeSize
            )
            painter.restore()

    def start(self):
        self.updatePosition()
        self._isSpinning = True
        self.show()

        if self.parentWidget and self._disableParentWhenSpinning:
            self.parentWidget().setEnabled(False)

        if not self._timer.isActive():
            self._timer.start()
            self._currentCounter = 0

    def stop(self):
        self._isSpinning = False
        self.hide()

        if self.parentWidget() and self._disableParentWhenSpinning:
            self.parentWidget().setEnabled(True)

        if self._timer.isActive():
            self._timer.stop()
            self._currentCounter = 0

    def setNumberOfLines(self, lines):
        self._numberOfLines = lines
        self._currentCounter = 0
        self.updateTimer()

    def setLineLength(self, length):
        self._lineLength = length
        self.updateSize()

    def setLineWidth(self, width):
        self._lineWidth = width
        self.updateSize()

    def setInnerRadius(self, radius):
        self._innerRadius = radius
        self.updateSize()

    @property
    def color(self):
        return self._color

    @property
    def roundness(self):
        return self._roundness

    @property
    def minimumTrailOpacity(self):
        return self._minimumTrailOpacity

    @property
    def trailFadePercentage(self):
        return self._trailFadePercentage

    @property
    def revolutionsPersSecond(self):
        return self._revolutionsPerSecond

    @property
    def numberOfLines(self):
        return self._numberOfLines

    @property
    def lineLength(self):
        return self._lineLength

    @property
    def lineWidth(self):
        return self._lineWidth

    @property
    def innerRadius(self):
        return self._innerRadius

    @property
    def isSpinning(self):
        return self._isSpinning

    def setRoundness(self, roundness):
        self._roundness = max(0.0, min(100.0, roundness))

    def setColor(self, color=Qt.black):
        self._color = QColor(color)

    def setRevolutionsPerSecond(self, revolutionsPerSecond):
        self._revolutionsPerSecond = revolutionsPerSecond
        self.updateTimer()

    def setTrailFadePercentage(self, trail):
        self._trailFadePercentage = trail

    def setMinimumTrailOpacity(self, minimumTrailOpacity):
        self._minimumTrailOpacity = minimumTrailOpacity

    def rotate(self):
        self._currentCounter += 1
        if self._currentCounter >= self._numberOfLines:
            self._currentCounter = 0
        self.update()

    def updateSize(self):
        size = (self._innerRadius + self._lineLength) * 2
        self.setFixedSize(size, size)

    def updateTimer(self):
        self._timer.setInterval(1000 / (self._numberOfLines * self._revolutionsPerSecond))

    def updatePosition(self):
        if self.parentWidget() and self._centerOnParent:
            self.move(
                self.parentWidget().width() / 2 - self.width() / 2,
                self.parentWidget().height() / 2 - self.height() / 2
            )

    def lineCountDistanceFromPrimary(self, current, primary, totalNrOfLines):
        distance = primary - current
        if distance < 0:
            distance += totalNrOfLines
        return distance

    def currentLineColor(self, countDistance, totalNrOfLines, trailFadePerc, minOpacity, colorinput):
        color = QColor(colorinput)
        if countDistance == 0:
            return color
        minAlphaF = minOpacity / 100.0
        distanceThreshold = int(math.ceil((totalNrOfLines - 1) * trailFadePerc / 100.0))
        if countDistance > distanceThreshold:
            color.setAlphaF(minAlphaF)
        else:
            alphaDiff = color.alphaF() - minAlphaF
            gradient = alphaDiff / float(distanceThreshold + 1)
            resultAlpha = color.alphaF() - gradient * countDistance
            # If alpha is out of bounds, clip it.
            resultAlpha = min(1.0, max(0.0, resultAlpha))
            color.setAlphaF(resultAlpha)
        return color

class JobThread(QThread):
    jobFinished = Signal(bool, object)
    def __init__(self, job, job_kwargs={}, parent=None):
        super().__init__(parent)

        assert callable(job), "job must be callable"
        self.job = job
        self.job_kwargs = job_kwargs

    def run(self):
        retval, results = self.job(**self.job_kwargs)
        self.jobFinished.emit(retval, results)


class WaitingDialog(QDialog):
    jobFinished = Signal(bool, object)

    label_message: QLabel
    waitingWidget: WaitingWidget
    def __init__(self, job, job_kwargs={}, title='', message='', parent=None):
        super().__init__(parent)

        self.jobthread = JobThread(job, job_kwargs, self)

        self.initUI()
        self.establish_connection()

        self.setWindowTitle(title)
        self.label_message.setText(message)

    def initUI(self):
        vbox = QVBoxLayout()

        self.label_message = QLabel()
        vbox.addWidget(self.label_message)

        self.waitingWidget = WaitingWidget(self)
        vbox.addWidget(self.waitingWidget)

        self.setLayout(vbox)

    def establish_connection(self):
        self.jobthread.jobFinished.connect(lambda retval, results: self.finish(retval, results))

    def start(self):
        self.waitingWidget.start()
        self.jobthread.start()

    def finish(self, retval, results):
        self.waitingWidget.stop()
        self.close()
        self.jobFinished.emit(retval, results)

