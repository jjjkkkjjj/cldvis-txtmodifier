from PySide2.QtWidgets import *


import glob, os

from .utils import path_desktop

SUPPORTED_EXTENSIONS = ['.jpeg', '.jpg', '.png', '.tif', '.tiff', '.bmp', '.die', '.pbm', '.pgm', '.ppm', '.pxm', '.pnm', '.hdr', '.pic']

def openFiles(self):
    filters = 'Images (*.jpeg *.jpg *.png *.tif *.tiff *.bmp *.die *.pbm *.pgm *.ppm *.pxm *.pnm *.hdr *.pic)'

    filenames = QFileDialog.getOpenFileNames(self, 'OpenFiles', path_desktop(), filters, None, QFileDialog.DontUseNativeDialog)
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
    dirname = QFileDialog.getExistingDirectory(self, 'OpenDir', path_desktop(), QFileDialog.DontUseNativeDialog)

    filenames = sorted(glob.glob(os.path.join(dirname, '*')))
    # remove not supported files and directories
    filenames = [filename for filename in filenames if os.path.splitext(filename)[-1] in SUPPORTED_EXTENSIONS]



    return filenames
