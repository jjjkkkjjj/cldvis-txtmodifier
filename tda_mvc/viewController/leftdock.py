from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import os, glob
import pandas as pd

from ..view import AboutDialog, PreferencesDialog
from ..utils.modes import PredictionMode, ShowingMode, AreaMode, ExportFileExtention
from ..utils.exception import PredictionError
from ..utils.funcs import parse_annotations, create_fileters
from ..model import TDA
from .base import VCAbstractMixin

SUPPORTED_EXTENSIONS = ['.jpeg', '.jpg', '.png', '.tif', '.tiff', '.bmp', '.die', '.pbm', '.pgm', '.ppm',
                        '.pxm', '.pnm', '.hdr', '.pic']

class LeftDockVCMixin(VCAbstractMixin):

    def establish_connection(self):
        ### leftdock ###
        # file
        self.leftdock.button_openfile.clicked.connect(self.openfile)
        self.leftdock.button_openfolder.clicked.connect(self.openFolder)
        self.leftdock.button_forward.clicked.connect(lambda: self.changeImg(True))
        self.leftdock.button_back.clicked.connect(lambda: self.changeImg(False))
        self.leftdock.button_exportCSV.clicked.connect(self.exportCSV)
        self.leftdock.button_exportDataset.clicked.connect(self.exportDataset)

        # view
        self.leftdock.button_zoomin.clicked.connect(lambda: self.zoomInOut(True))
        self.leftdock.button_zoomout.clicked.connect(lambda: self.zoomInOut(False))
        self.leftdock.spinBox_zoom.valueChanged.connect(lambda value: self.zoomValueChanged(value))
        self.leftdock.radioButton_entire.clicked.connect(lambda: self.showingmodeChanged(ShowingMode.ENTIRE))
        self.leftdock.radioButton_selected.clicked.connect(lambda: self.showingmodeChanged(ShowingMode.SELECTED))

        # prediction
        self.leftdock.radioButton_rect.clicked.connect(lambda: self.areamodeChanged(AreaMode.RECTANGLE))
        self.leftdock.radioButton_quad.clicked.connect(lambda: self.areamodeChanged(AreaMode.QUADRANGLE))
        self.leftdock.button_discard.clicked.connect(self.discard)
        self.leftdock.comboBox_predmode.currentTextChanged.connect(lambda predmode: self.predmodeChanged(PredictionMode(predmode)))
        self.leftdock.button_predict.clicked.connect(self.predict)

        ### menu ###
        # file
        self.menu.action_openfiles.triggered.connect(self.openfile)
        self.menu.action_openfolder.triggered.connect(self.openFolder)
        self.menu.action_savetda.triggered.connect(lambda: self.savetda(True))
        self.menu.action_saveastda.triggered.connect(lambda: self.savetda(False))
        self.menu.action_loadtda.triggered.connect(self.loadtda)
        self.menu.action_forwardfile.triggered.connect(lambda: self.changeImg(True))
        self.menu.action_backfile.triggered.connect(lambda: self.changeImg(False))
        self.menu.action_exportCSV.triggered.connect(self.exportCSV)
        self.menu.action_exportDataset.triggered.connect(self.exportDataset)

        # view
        self.menu.action_zoomin.triggered.connect(lambda: self.zoomInOut(True))
        self.menu.action_zoomout.triggered.connect(lambda: self.zoomInOut(False))
        self.menu.action_showentire.triggered.connect(lambda: self.leftdock.radioButton_selected.click())
        self.menu.action_showselected.triggered.connect(lambda: self.leftdock.radioButton_selected.click())

        # prediction
        self.menu.action_areaRectMode.triggered.connect(lambda: self.leftdock.radioButton_rect.click())
        self.menu.action_areaQuadMode.triggered.connect(lambda: self.leftdock.radioButton_quad.click())
        self.menu.action_discard.triggered.connect(self.discard)
        self.menu.action_predictImageMode.triggered.connect(lambda: self.leftdock.comboBox_predmode.setCurrentIndex(0))
        self.menu.action_predictDocumentMode.triggered.connect(lambda: self.leftdock.comboBox_predmode.setCurrentIndex(1))
        self.menu.action_predict.triggered.connect(self.predict)

        # about
        self.menu.action_about.triggered.connect(self.openAbout)
        self.menu.action_preferences.triggered.connect(self.openPreferences)

    def openfile(self):
        filters = '{} ({})'.format('Images', ' '.join(['*' + ext for ext in SUPPORTED_EXTENSIONS]))

        filenames = QFileDialog.getOpenFileNames(self, 'OpenFiles', self.model.config.last_opendir, filters, None)
        filenames = filenames[0]
        if len(filenames) == 0:
            _ = QMessageBox.warning(self, 'Warning', 'No image files!!', QMessageBox.Ok)
            filenames = None

        self.model.set_imgPaths(filenames)
        # update view
        self.updateModel()
        self.updateAllUI()

    def openFolder(self):
        dirpath = QFileDialog.getExistingDirectory(self, 'OpenDir', self.model.config.last_opendir)

        filenames = sorted(glob.glob(os.path.join(dirpath, '*')))
        # remove not supported files and directories
        filenames = [filename for filename in filenames if os.path.splitext(filename)[-1] in SUPPORTED_EXTENSIONS]

        self.model.set_imgPaths(filenames)
        # update view
        self.updateModel()
        self.updateAllUI()

    def savetda(self, isDefault):
        if isDefault:
            filename = os.path.splitext(self.model.defaultsavename)[0]
            filepath = os.path.join(self.model.config.export_datasetdir, 'tda', filename + '.tda')
            if os.path.exists(filepath):
                ret = QMessageBox.warning(self, 'Notification',
                                          '{} has already existed\nAre you sure to overwrite it?'.format(self.model.defaultsavename),
                                          QMessageBox.No | QMessageBox.Yes)
                if ret == QMessageBox.No:
                    return

            self.model.saveInDefaultDirectory()
        else:
            filename = os.path.splitext(os.path.basename(self.model.imgpath))[0]
            filters_list = create_fileters(('TDA Binary', 'tda'))
            filepath, selected_filter = QFileDialog.getSaveFileName(self, 'Export file as',
                                                                    os.path.join(self.model.config.export_datasetdir, filename),
                                                                    ';;'.join(filters_list), None)
            if filepath == '':
                return
            tda = TDA(self.model)
            TDA.save(tda, filepath)
        QMessageBox.information(self, 'Saved', 'Saved to {}'.format(filepath))

    def loadtda(self):
        filters_list = create_fileters(('TDA Binary', 'tda'))
        filepath, _ = QFileDialog.getOpenFileName(self, 'Open TDA Binary File', self.model.config.export_datasetdir, ';;'.join(filters_list), None)
        if filepath == '':
            return

        tda = TDA.load(filepath)
        self.model.areamode = tda.areamode
        # rectangle
        self.model.rectangle.set_percent_points(tda.rectangle_percent_pts)
        self.model.rectangle.set_parentVals(parentQSize=self.central.imageView.size())
        # quadrangle
        self.model.quadrangle.set_percent_points(tda.quadrangle_percent_pts)
        self.model.quadrangle.set_parentVals(parentQSize=self.central.imageView.size())
        # predictedArea
        self.model.predictedArea.set_percent_points(tda.predictedArea_percent_pts)
        self.model.predictedArea.set_parentVals(parentQSize=self.model.areaParentQSize,
                                                offsetQPoint=self.model.areaOffsetQPoint)
        # annotation
        self.model.results = tda.results_dict
        if self.model.showingmode == ShowingMode.ENTIRE:
            self.model.annotations.set_results(tda.results_dict, baseWidget=self.central.imageView,
                                               parentQSize=self.model.areaQSize, offsetQPoint=self.model.areaTopLeft)

        elif self.model.showingmode == ShowingMode.SELECTED:
            self.model.annotations.set_results(tda.results_dict, baseWidget=self.central.imageView,
                                               parentQSize=self.central.imageView.size(), offsetQPoint=QPoint(0, 0))

        filename = os.path.basename(filepath)
        self.model.defaultsavename = filename

        self.updateModel()
        self.updateAllUI()

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

    def exportCSV(self):
        table_list = parse_annotations(self.model)
        filters_list = create_fileters(*ExportFileExtention.gen_filters_args(self.model.config.export_defaultFileFormat))
        filename = os.path.splitext(os.path.basename(self.model.imgpath))[0]
        filepath, selected_filter = QFileDialog.getSaveFileName(self, 'Export file as', os.path.join(self.model.config.export_datasetdir, filename),
                                               ';;'.join(filters_list), None)
        #with open('./debug/texts.csv', 'w') as f:
        if filepath == '':
            return

        # too dirty...
        ext = selected_filter.split('*.')[-1][:-1]
        def _check_and_append_ext(filepath, e):
            if os.path.splitext(filepath)[1] == '':
                filepath += '.' + e
            return filepath

        filepath = _check_and_append_ext(filepath, ext)
        df = pd.DataFrame(table_list)
        if ext == 'csv':
            df.to_csv(filepath, sep=',', header=False, index=False, encoding='utf-8')

        elif ext == 'xlsx':
            df.to_excel(filepath, header=False, index=False, encoding='utf-8')

        elif ext == 'tsv':
            df.to_csv(filepath, sep='\t', header=False, index=False, encoding='utf-8')

        elif ext == 'psv':
            df.to_csv(filepath, sep='|', header=False, index=False, encoding='utf-8')


    def exportDataset(self):
        pass

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
        aboutBox.exec_()

    def openPreferences(self):
        preferencesBox = PreferencesDialog(self.model, initial=False, parent=self)
        preferencesBox.exec_()

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

    def discard(self):
        if self.model.isPredicted:
            ret = QMessageBox.warning(self, 'Discard all results', 'Are you sure you want to discard all results?', QMessageBox.Yes | QMessageBox.No)
            if ret == QMessageBox.No:
                return

            self.model.discard_annotations()

            self.updateModel()
            self.updateAllUI()

        else:
            ret = QMessageBox.warning(self, 'Discard selection', 'Are you sure you want to discard selection area?',
                                      QMessageBox.Yes | QMessageBox.No)
            if ret == QMessageBox.No:
                return

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

