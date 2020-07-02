from PySide2.QtWidgets import *

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
