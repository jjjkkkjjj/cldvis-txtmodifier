from PySide2.QtWidgets import *
from PySide2.QtCore import *

import glob, os

from .utils import check_instance
from ..widgets.baseWidget import BaseWidget

SUPPORTED_EXTENSIONS = ['.jpeg', '.jpg', '.png', '.tif', '.tiff', '.bmp', '.die', '.pbm', '.pgm', '.ppm', '.pxm', '.pnm', '.hdr', '.pic']

def openFiles(self):
    _ = check_instance('self', self, BaseWidget)

    filters = 'Images (*.jpeg *.jpg *.png *.tif *.tiff *.bmp *.die *.pbm *.pgm *.ppm *.pxm *.pnm *.hdr *.pic)'
    # filenames is (list of str(filepath), str(filters))
    filenames = QFileDialog.getOpenFileNames(self, 'OpenFiles', self.model.config.last_opendir, filters, None, QFileDialog.DontUseNativeDialog)
    return filenames[0]
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
               '<a href="https://icons8.com/icon/12386/minus">Minus icon by Icons8</a>'
        label_text.setText(text)
        label_text.setTextFormat(Qt.RichText)
        label_text.setTextInteractionFlags(Qt.TextBrowserInteraction)
        label_text.setOpenExternalLinks(True)
        hbox.addWidget(label_text)

        self.setLayout(hbox)
        self.setFixedSize(400, 200)