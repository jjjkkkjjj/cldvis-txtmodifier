from PySide2.QtWidgets import *
from PySide2.QtCore import *
import os, glob

from ..view import AboutDialog
from ..utils.modes import PredictionMode, ShowingMode
from .base import VCAbstractMixin

SUPPORTED_EXTENSIONS = ['.jpeg', '.jpg', '.png', '.tif', '.tiff', '.bmp', '.die', '.pbm', '.pgm', '.ppm',
                        '.pxm', '.pnm', '.hdr', '.pic']

class LeftDockVCMixin(VCAbstractMixin):

    def establish_connection(self):
        ### leftdock ###
        # open
        self.leftdock.button_openfile.clicked.connect(self.openfile)
        self.leftdock.button_openfolder.clicked.connect(self.openFolder)
        self.leftdock.button_forward.clicked.connect(lambda: self.changeImg(True))
        self.leftdock.button_back.clicked.connect(lambda: self.changeImg(False))

        # viewer
        self.leftdock.button_zoomin.clicked.connect(lambda: self.zoomInOut(True))
        self.leftdock.button_zoomout.clicked.connect(lambda: self.zoomInOut(False))
        self.leftdock.spinBox_zoom.valueChanged.connect(lambda value: self.zoomValueChanged(value))
        self.leftdock.radioButton_entire.clicked.connect(lambda: self.showingmodeChanged(ShowingMode.ENTIRE))
        self.leftdock.radioButton_selected.clicked.connect(lambda: self.showingmodeChanged(ShowingMode.SELECTED))

        # prediction
        self.leftdock.button_removeArea.clicked.connect(self.removeArea)
        self.leftdock.comboBox_predmode.currentTextChanged.connect(lambda predmode: self.predmodeChanged(PredictionMode(predmode)))

        ### menu ###
        # open
        self.menu.action_openfiles.triggered.connect(self.openfile)
        self.menu.action_openfolder.triggered.connect(self.openFolder)
        self.menu.action_forwardfile.triggered.connect(lambda: self.changeImg(True))
        self.menu.action_backfile.triggered.connect(lambda: self.changeImg(False))

        # viewer
        self.menu.action_zoomin.triggered.connect(lambda: self.zoomInOut(True))
        self.menu.action_zoomout.triggered.connect(lambda: self.zoomInOut(False))
        self.menu.action_showentire.triggered.connect(lambda: self.showingmodeChanged(ShowingMode.ENTIRE))
        self.menu.action_showselected.triggered.connect(lambda: self.showingmodeChanged(ShowingMode.SELECTED))

        # about
        self.menu.action_about.triggered.connect(self.openAbout)

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
        self.central.updateUI()

    def openFolder(self):
        dirname = QFileDialog.getExistingDirectory(self, 'OpenDir', self.model.config.last_opendir,
                                                   QFileDialog.DontUseNativeDialog)

        filenames = sorted(glob.glob(os.path.join(dirname, '*')))
        # remove not supported files and directories
        filenames = [filename for filename in filenames if os.path.splitext(filename)[-1] in SUPPORTED_EXTENSIONS]

        self.model.set_imgPaths(filenames)
        # update view
        self.leftdock.updateUI()
        self.central.updateUI()

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
        self.central.updateUI()

    def zoomInOut(self, isZoomIn):
        if isZoomIn:
            r = min(self.leftdock.spinBox_zoom.value() + 10, 200)
        else:
            r = max(self.leftdock.spinBox_zoom.value() - 10, 20)

        # call zoomValueChanged
        self.leftdock.spinBox_zoom.setValue(r)

    def zoomValueChanged(self, value):
        self.model.zoomvalue = value
        self.central.updateUI()

    def openAbout(self):
        aboutBox = AboutDialog(self)
        aboutBox.show()

    def predmodeChanged(self, mode):
        self.model.predmode = mode

        self.leftdock.updateUI()
        self.central.updateUI()
        self.menu.updateUI()

    def showingmodeChanged(self, mode):
        self.model.showingmode = mode

        if self.model.predmode == PredictionMode.IMAGE:
            self.model.saveSelectedImg_imagemode(self.model.imgpath)
        elif self.model.predmode == PredictionMode.TABLE:
            self.model.saveSelectedImg_tablemode(self.model.imgpath)

        self.leftdock.updateUI()
        self.central.updateUI()
        self.menu.updateUI()

    def removeArea(self):
        self.model.removeArea()

        self.leftdock.updateUI()
        self.central.updateUI()
        self.menu.updateUI()