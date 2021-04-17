from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from google.auth.exceptions import DefaultCredentialsError
import glob, os, sys

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

        # jsonpath => '': Not selected, None: Can't be loaded, other: OK.
        try:
            self.jsonpath = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
        except KeyError:
            self.jsonpath = ''
        # None: Not selected
        # False: Can't be loaded
        # True: OK.
        self.isValidJsonPath = None

        from ..model import Model
        self.model: Model = model
        self.initial = initial

        self.initUI()
        self.establish_connection()
        self.updateUI()


    def initUI(self):
        title = 'Preferences'
        self.setWindowTitle(title)

        vbox = QVBoxLayout()

        hbox_jsonpath = QHBoxLayout()
        self.label_jsonpath = QLabel('Json Path: Not selected')
        hbox_jsonpath.addWidget(self.label_jsonpath, 5)
        self.label_jsonpathStatus = QLabel()
        hbox_jsonpath.addWidget(self.label_jsonpathStatus, 1)
        self.button_readJsonpath = QPushButton('Read Json')
        hbox_jsonpath.addWidget(self.button_readJsonpath, 1)
        vbox.addLayout(hbox_jsonpath)

        self.button_ok = QPushButton('OK')
        self.button_ok.setDefault(True)
        vbox.addWidget(self.button_ok)

        self.setLayout(vbox)
        self.setFixedSize(600, 200)

    def establish_connection(self):
        self.button_readJsonpath.clicked.connect(self.readJsonpath)
        self.button_ok.clicked.connect(self.close)

    def updateUI(self):
        self.isValidJsonPath = self.checkJsonpath()

        if self.isValidJsonPath is None:
            self.label_jsonpath.setText('Json Path: Not selected')
            icon = self.style().standardIcon(QStyle.SP_MessageBoxWarning)
            self.button_ok.setEnabled(False)
        elif self.isValidJsonPath:
            self.label_jsonpath.setText('Json Path: {}'.format(os.path.basename(self.jsonpath)))
            icon = self.style().standardIcon(QStyle.SP_DialogApplyButton)
            self.button_ok.setEnabled(True)
        else:
            self.label_jsonpath.setText('Json Path: {} is invalid'.format(os.path.basename(self.jsonpath)))
            icon = self.style().standardIcon(QStyle.SP_MessageBoxCritical)
            self.button_ok.setEnabled(False)

        self.label_jsonpathStatus.setPixmap(icon.pixmap(QSize(16, 16)))

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
        if self.jsonpath is None or self.jsonpath == '':
            return None
        try:
            self.model.set_credentialJsonpath(self.jsonpath)
            return True
        except DefaultCredentialsError:
            return False

    def readJsonpath(self):
        filters = 'JSON (*.json)'
        filename = QFileDialog.getOpenFileName(self, 'OpenFile', '', filters, None, QFileDialog.DontUseNativeDialog)

        self.jsonpath = filename[0] if filename[0] != '' else None
        self.updateUI()

    def closeEvent(self, event):
        if self.initial and not self.isValidJsonPath:
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