from PySide2.QtWidgets import *
from PySide2.QtCore import *

import glob, os, sys

from .utils import check_instance
from ..widgets.baseWidget import BaseWidget

SUPPORTED_EXTENSIONS = ['.jpeg', '.jpg', '.png', '.tif', '.tiff', '.bmp', '.die', '.pbm', '.pgm', '.ppm', '.pxm', '.pnm', '.hdr', '.pic']

def openFiles(self, name, exts):
    _ = check_instance('self', self, BaseWidget)

    #filters = 'Images (*.jpeg *.jpg *.png *.tif *.tiff *.bmp *.die *.pbm *.pgm *.ppm *.pxm *.pnm *.hdr *.pic)'
    if isinstance(exts, (list, tuple)):
        filters = '{} ({})'.format(name, ' '.join(['*' + ext for ext in exts]))
    else:
        filters = '{} (*{})'.format(name, exts)

    # filenames is (list of str(filepath), str(filters))
    filenames = QFileDialog.getOpenFileNames(self, 'OpenFiles', self.model.config.last_opendir, filters, None,
                                             QFileDialog.DontUseNativeDialog)
    filenames = filenames[0]

    return filenames
    """
    dialog = QFileDialog(self)
    dialog.setWindowTitle('Open Files')
    dialog.setNameFilter(filters)
    dialog.setFileMode(QFileDialog.ExistingFile)
    if dialog.exec_() == QDialog.Accepted:
        return dialog.selectedFiles()
    """

def openDir(self):
    _ = check_instance('self', self, BaseWidget)

    dirname = QFileDialog.getExistingDirectory(self, 'OpenDir', self.model.config.last_opendir, QFileDialog.DontUseNativeDialog)

    filenames = sorted(glob.glob(os.path.join(dirname, '*')))
    # remove not supported files and directories
    filenames = [filename for filename in filenames if os.path.splitext(filename)[-1] in SUPPORTED_EXTENSIONS]



    return filenames

def openAbout(mainWidget):
    from ..mainWindow import MainWidget
    _ = check_instance('mainWidget', mainWidget, MainWidget)

    #msgBox = QMessageBox.information(mainWidget, 'About Table Data Analyzer', 'aaaa')
    aboutBox = AboutDialog(mainWidget)
    aboutBox.show()


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
               '<a href="https://icons8.com/icon/66368/artificial-intelligence">Artificial Intelligence icon by Icons8</a>' \
               '' \
               'Icons made by <a href="https://www.flaticon.com/authors/srip" title="srip">srip</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a>'
        label_text.setText(text)
        label_text.setTextFormat(Qt.RichText)
        label_text.setTextInteractionFlags(Qt.TextBrowserInteraction)
        label_text.setOpenExternalLinks(True)
        hbox.addWidget(label_text)

        self.setLayout(hbox)
        self.setFixedSize(400, 300)

def openCredential(mainWidget):
    from ..mainWindow import MainWidget
    _ = check_instance('mainWidget', mainWidget, MainWidget)

    credential = CredentialDialog(mainWidget)
    credential.show()

class CredentialDialog(QDialog):
    pathSet = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._jsonpath = None

        self.initUI()
        self.establish_connection()

        self.check_enable()

    @property
    def jsonpath(self):
        return self._jsonpath
    @jsonpath.setter
    def jsonpath(self, path):
        self._jsonpath = path
        if path:
            self.label_path.setText('Json Path: {}'.format(self._jsonpath))
        else:
            self.label_path.setText('Json Path: Not selected')

        self.check_enable()

    @property
    def isSetPath(self):
        return self._jsonpath is not None

    def initUI(self):
        title = 'Set credential'
        self.setWindowTitle(title)

        vbox = QVBoxLayout()

        self.label_path = QLabel('Json Path: Not selected')
        vbox.addWidget(self.label_path)

        hbox = QHBoxLayout()
        self.button_read = QPushButton('Read Json')
        hbox.addWidget(self.button_read)

        self.button_ok = QPushButton('OK')
        hbox.addWidget(self.button_ok)
        vbox.addLayout(hbox)

        self.setLayout(vbox)
        self.setFixedSize(400, 200)

    def establish_connection(self):
        self.button_read.clicked.connect(self.readJsonpath)
        self.button_ok.clicked.connect(self._emit_jsonpath)

    def check_enable(self):
        # always enabled
        # self.button_read.setEnabled(not self.isSetPath)
        self.button_ok.setEnabled(self.isSetPath)

    def readJsonpath(self):
        filters = 'JSON (*.json)'
        filename = QFileDialog.getOpenFileName(self, 'OpenFile', '', filters, None, QFileDialog.DontUseNativeDialog)

        self.jsonpath = filename[0] if filename[0] != '' else None

    def _emit_jsonpath(self):
        # set path
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = self.jsonpath
        self.pathSet.emit(self.jsonpath)
        self.close()

    def closeEvent(self, event):
        if not self.isSetPath:
            sys.exit()