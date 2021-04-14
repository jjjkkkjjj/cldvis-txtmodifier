from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import os, glob

from ..view import AboutDialog
from ..utils.modes import PredictionMode, ShowingMode, AreaMode
from ..utils.exception import PredictionError
from ..utils.funcs import qsize_from_quadrangle
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
        self.leftdock.radioButton_rect.clicked.connect(lambda: self.areamodeChanged(AreaMode.RECTANGLE))
        self.leftdock.radioButton_quad.clicked.connect(lambda: self.areamodeChanged(AreaMode.QUADRANGLE))
        self.leftdock.button_removeArea.clicked.connect(self.removeArea)
        self.leftdock.comboBox_predmode.currentTextChanged.connect(lambda predmode: self.predmodeChanged(PredictionMode(predmode)))
        self.leftdock.button_predict.clicked.connect(self.predict)

        ### menu ###
        # open
        self.menu.action_openfiles.triggered.connect(self.openfile)
        self.menu.action_openfolder.triggered.connect(self.openFolder)
        self.menu.action_forwardfile.triggered.connect(lambda: self.changeImg(True))
        self.menu.action_backfile.triggered.connect(lambda: self.changeImg(False))

        # viewer
        self.menu.action_zoomin.triggered.connect(lambda: self.zoomInOut(True))
        self.menu.action_zoomout.triggered.connect(lambda: self.zoomInOut(False))
        self.menu.action_showentire.triggered.connect(lambda: self.leftdock.radioButton_selected.click())
        self.menu.action_showselected.triggered.connect(lambda: self.leftdock.radioButton_selected.click())

        # prediction
        self.menu.action_areaRectMode.triggered.connect(lambda: self.leftdock.radioButton_rect.click())
        self.menu.action_areaQuadMode.triggered.connect(lambda: self.leftdock.radioButton_quad.click())
        self.menu.action_removeArea.triggered.connect(self.removeArea)
        self.menu.action_predictImageMode.triggered.connect(lambda: self.leftdock.comboBox_predmode.setCurrentIndex(0))
        self.menu.action_predictDocumentMode.triggered.connect(lambda: self.leftdock.comboBox_predmode.setCurrentIndex(1))
        self.menu.action_predict.triggered.connect(self.predict)

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

        self.updateModel()
        self.updateAllUI()

    def openAbout(self):
        aboutBox = AboutDialog(self)
        aboutBox.show()

    def predmodeChanged(self, mode):
        self.model.predmode = mode

        self.updateModel()
        self.updateAllUI()

    def showingmodeChanged(self, mode):
        self.model.showingmode = mode

        if self.model.showingmode == ShowingMode.SELECTED:
            if self.model.areamode == AreaMode.RECTANGLE:
                self.model.saveSelectedImg_rectmode(self.model.imgpath)
            elif self.model.areamode == AreaMode.QUADRANGLE:
                self.model.saveSelectedImg_quadmode(self.model.imgpath)

        self.updateModel()
        self.updateAllUI()

    def areamodeChanged(self, mode):
        self.model.areamode = mode

        self.updateModel()
        self.updateAllUI()

    def removeArea(self):
        self.model.removeArea()
        self.leftdock.radioButton_entire.click()
        # call areamodeChanged, so below codes are redundant
        #self.updateAllUI()

    def predict(self):
        from ..main import MainViewController
        import json
        import numpy as np
        if MainViewController.debug:

            # read results from json
            if self.model.areamode == AreaMode.RECTANGLE:
                # read predictedArea from csv
                self.model.rectangle.set_percent_points(np.loadtxt(os.path.join('.', 'debug', 'rect.csv'), delimiter=',').reshape((2, 2)))
                self.model.rectangle.set_parentVals(parentQSize=self.central.imageView.size())

                self.model.selectedRectImgPath = os.path.join('.', 'debug', '20200619173238005_x355X2640y337Y1787.jpg')
                if self.model.predmode == PredictionMode.IMAGE:
                    jsonpath = os.path.join('debug', 'result-rect-image.json')
                elif self.model.predmode == PredictionMode.DOCUMENT:
                    jsonpath = os.path.join('debug', 'result-rect-document.json')

                with open(jsonpath, 'r') as f:
                    results = json.load(f)
            elif self.model.areamode == AreaMode.QUADRANGLE:
                # read predictedArea from csv
                self.model.quadrangle.set_percent_points(np.loadtxt(os.path.join('.', 'debug', 'poly.csv'), delimiter=',').reshape((4, 2)))
                self.model.quadrangle.set_parentVals(parentQSize=self.central.imageView.size())

                self.model.selectedQuadImgPath = os.path.join('.', 'debug', '20200619173238005_tlx386tly346trx2620try380brx2600bry1790blx366bly1764.jpg')
                if self.model.predmode == PredictionMode.IMAGE:
                    jsonpath = os.path.join('debug', 'result-quad-image.json')
                elif self.model.predmode == PredictionMode.DOCUMENT:
                    jsonpath = os.path.join('debug', 'result-quad-document.json')

                with open(jsonpath, 'r') as f:
                    results = json.load(f)
            self.model.results = results

        else:
            try:
                # prediction
                import json
                if self.model.predmode == PredictionMode.IMAGE:
                    if self.model.selectedImgPath is None:
                        self.model.saveSelectedImg_rectmode(self.model.imgpath)
                    results = self.model.detectAsImage(imgpath=self.model.selectedImgPath)

                    np.savetxt(os.path.join('debug', 'rect.csv'), self.model.rectangle.percent_points, delimiter=',')
                    if self.model.areamode == AreaMode.RECTANGLE:
                        self.model.saveAsJson(os.path.join('debug', 'result-rect-image.json'))
                    elif self.model.areamode == AreaMode.QUADRANGLE:
                        self.model.saveAsJson(os.path.join('debug', 'result-quad-image.json'))

                elif self.model.predmode == PredictionMode.DOCUMENT:
                    if self.model.selectedImgPath is None:
                        self.model.saveSelectedImg_quadmode(self.model.imgpath)
                    results = self.model.detectAsDocument(imgpath=self.model.selectedImgPath)

                    np.savetxt(os.path.join('debug', 'poly.csv'), self.model.quadrangle.percent_points, delimiter=',')
                    if self.model.areamode == AreaMode.RECTANGLE:
                        self.model.saveAsJson(os.path.join('debug', 'result-rect-document.json'))
                    elif self.model.areamode == AreaMode.QUADRANGLE:
                        self.model.saveAsJson(os.path.join('debug', 'result-quad-document.json'))


            except PredictionError as e:
                # show messagebox
                ret = QMessageBox.critical(self, 'Error', 'Error was occurred. Status: {}'.format(e), QMessageBox.Yes)
                if ret == QMessageBox.Yes:
                    # remove tmp files
                    self.model.clearTmpImg()

        # set the annotations from the predicted results
        self.model.predictedArea.set_percent_points(self.model.areaPercentPts)
        self.model.predictedArea.set_parentVals(parentQSize=self.model.areaParentQSize, offsetQPoint=self.model.areaOffsetQPoint)
        if self.model.showingmode == ShowingMode.ENTIRE:
            self.model.annotations.set_results(results, baseWidget=self.central.imageView,
                                       parentQSize=self.model.areaQSize, offsetQPoint=self.model.areaTopLeft)

        elif self.model.showingmode == ShowingMode.SELECTED:
            self.model.annotations.set_results(results, baseWidget=self.central.imageView,
                                       parentQSize=self.central.imageView.size(), offsetQPoint=QPoint(0, 0))
        # update all
        self.updateModel()
        self.updateAllUI()

