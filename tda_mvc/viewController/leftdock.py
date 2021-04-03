from PySide2.QtWidgets import *
from PySide2.QtCore import *
import os, glob

from .base import VCAbstractMixin

SUPPORTED_EXTENSIONS = ['.jpeg', '.jpg', '.png', '.tif', '.tiff', '.bmp', '.die', '.pbm', '.pgm', '.ppm',
                                '.pxm', '.pnm', '.hdr', '.pic']

class LeftDockVCMixin(VCAbstractMixin):

    @property
    def leftdock(self):
        return self.main.leftdock

    def establish_connection(self):
        self.leftdock.button_openfile.clicked.connect(self.openfile)
        self.leftdock.button_openfolder.clicked.connect(self.openFolder)
        self.leftdock.button_forward.clicked.connect(lambda: self.changeImg(True))
        self.leftdock.button_back.clicked.connect(lambda: self.changeImg(False))

    def openfile(self):
        filters = '{} ({})'.format('Images', ' '.join(['*' + ext for ext in SUPPORTED_EXTENSIONS]))

        filenames = QFileDialog.getOpenFileNames(self, 'OpenFiles', self.model.config.last_opendir, filters, None,
                                                 QFileDialog.DontUseNativeDialog)
        filenames = filenames[0]
        if len(filenames) == 0:
            _ = QMessageBox.warning(self, 'Warning', 'No image files!!', QMessageBox.Ok)
            filenames = None

        self.model.set_imgPaths(filenames)
        # update view
        self.leftdock.updateUI()

    def openFolder(self):
        dirname = QFileDialog.getExistingDirectory(self, 'OpenDir', self.model.config.last_opendir,
                                                   QFileDialog.DontUseNativeDialog)

        filenames = sorted(glob.glob(os.path.join(dirname, '*')))
        # remove not supported files and directories
        filenames = [filename for filename in filenames if os.path.splitext(filename)[-1] in SUPPORTED_EXTENSIONS]

        self.model.set_imgPaths(filenames)
        # update view
        self.leftdock.updateUI()

    def changeImg(self, isForward):
        """
        Change image.
        Parameters
        ----------
        isNext: bool
            Whether to go forward or back

        Returns
        -------

        """
        if isForward:
            self.model.forward()
        else:
            self.model.back()
        # update view
        self.leftdock.updateUI()
