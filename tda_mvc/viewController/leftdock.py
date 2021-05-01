from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import os, glob, json
import pandas as pd

from ..view import AboutDialog, PreferencesDialog
from ..utils.modes import PredictionMode, ShowingMode, AreaMode, ExportFileExtention, ExportDatasetFormat
from ..utils.exception import PredictionError
from ..utils.funcs import create_fileters, get_pixmap
from ..model import TDA
from .base import VCAbstractMixin

SUPPORTED_EXTENSIONS = ['.jpeg', '.jpg', '.png', '.tif', '.tiff', '.bmp', '.die', '.pbm', '.pgm', '.ppm',
                        '.pxm', '.pnm', '.hdr', '.pic']

class LeftDockVCMixin(VCAbstractMixin):

    def establish_connection(self):
        ### leftdock ###
        self.leftdock.button_predict.clicked.connect(self.predict)
        self.leftdock.button_done.clicked.connect(self.done)
        self.leftdock.button_discard.clicked.connect(self.discard)

        # file
        self.leftdock.button_openfile.clicked.connect(self.openfile)
        self.leftdock.button_openfolder.clicked.connect(self.openFolder)
        self.leftdock.button_forward.clicked.connect(lambda: self.changeImg(True))
        self.leftdock.button_back.clicked.connect(lambda: self.changeImg(False))
        self.leftdock.button_exportCSV.clicked.connect(self.exportTableFile)
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
        self.leftdock.comboBox_predmode.currentIndexChanged.connect(lambda modeindex: self.predmodeChanged(PredictionMode.mode(modeindex)))

        ### menu ###
        self.menu.action_predict.triggered.connect(self.predict)
        self.menu.action_done.triggered.connect(self.done)
        self.menu.action_discard.triggered.connect(self.discard)
        # file
        self.menu.action_openfiles.triggered.connect(self.openfile)
        self.menu.action_openfolder.triggered.connect(self.openFolder)
        self.menu.action_savetda.triggered.connect(lambda: self.savetda(True))
        self.menu.action_saveastda.triggered.connect(lambda: self.savetda(False))
        self.menu.action_loadtda.triggered.connect(self.loadtda)
        self.menu.action_forwardfile.triggered.connect(lambda: self.changeImg(True))
        self.menu.action_backfile.triggered.connect(lambda: self.changeImg(False))
        self.menu.action_exportCSV.triggered.connect(self.exportTableFile)
        self.menu.action_exportDataset.triggered.connect(self.exportDataset)
        self.menu.action_exit.triggered.connect(self.close)

        # edit
        self.menu.action_undo.triggered.connect(lambda: self.undoredo(True))
        self.menu.action_redo.triggered.connect(lambda: self.undoredo(False))

        # view
        self.menu.action_zoomin.triggered.connect(lambda: self.zoomInOut(True))
        self.menu.action_zoomout.triggered.connect(lambda: self.zoomInOut(False))
        self.menu.action_showentire.triggered.connect(lambda: self.leftdock.radioButton_entire.click())
        self.menu.action_showselected.triggered.connect(lambda: self.leftdock.radioButton_selected.click())

        # prediction
        self.menu.action_areaRectMode.triggered.connect(lambda: self.leftdock.radioButton_rect.click())
        self.menu.action_areaQuadMode.triggered.connect(lambda: self.leftdock.radioButton_quad.click())
        self.menu.action_predictImageMode.triggered.connect(lambda: self.leftdock.comboBox_predmode.setCurrentIndex(0))
        self.menu.action_predictDocumentMode.triggered.connect(lambda: self.leftdock.comboBox_predmode.setCurrentIndex(1))

        # about
        self.menu.action_about.triggered.connect(self.openAbout)
        self.menu.action_preferences.triggered.connect(self.openPreferences)

    @property
    def language(self):
        return self.model.language

    def openfile(self):
        filters = '{} ({})'.format('Images', ' '.join(['*' + ext for ext in SUPPORTED_EXTENSIONS]))

        filenames = QFileDialog.getOpenFileNames(self, self.language.openfiles, self.model.config.lastOpenDir, filters, None)
        filenames = filenames[0]
        if len(filenames) == 0:
            _ = QMessageBox.warning(self, self.language.warning, self.language.notselectedtext, QMessageBox.Ok)
            filenames = None

        self.model.set_imgPaths(filenames)
        tda = self.model.get_default_tda()
        self.setModel_from_tda(tda)

        # update view
        self.updateAll()

    def openFolder(self):
        dirpath = QFileDialog.getExistingDirectory(self, self.language.opendir, self.model.config.lastOpenDir)

        filenames = sorted(glob.glob(os.path.join(dirpath, '*')))
        # remove not supported files and directories
        filenames = [filename for filename in filenames if os.path.splitext(filename)[-1] in SUPPORTED_EXTENSIONS]

        self.model.set_imgPaths(filenames)
        tda = self.model.get_default_tda()
        self.setModel_from_tda(tda)

        # update view
        self.updateAll()

    def savetda(self, isDefault):
        if not self.model.annotations.isEdited:
            # not asked if the results are not edited
            return True

        if isDefault:
            filepath = os.path.join(self.model.export_tdaDir, self.model.default_savename)
            if os.path.exists(filepath):
                ret = QMessageBox.warning(self, self.language.notification,
                                          self.language.existfiletext.format(self.model.default_savename),
                                          QMessageBox.No | QMessageBox.Yes)
                if ret == QMessageBox.No:
                    return False

            self.model.saveInDefaultDirectory()
        else:
            filename = os.path.splitext(os.path.basename(self.model.imgpath))[0]
            filters_list = create_fileters(('TDA Binary', 'tda'))
            filepath, selected_filter = QFileDialog.getSaveFileName(self, self.language.exportfileas,
                                                                    os.path.join(self.model.config.lastSavedtdaDir, filename),
                                                                    ';;'.join(filters_list), None)
            if filepath == '':
                return False
            tda = TDA(self.model)
            TDA.save(tda, filepath)
            self.model.set_lastSavedtdaDir(filepath)
        _ = QMessageBox.information(self, self.language.saved, self.language.savedtotext.format(filepath))
        return True

    def loadtda(self):
        filters_list = create_fileters(('TDA Binary', 'tda'))
        filepath, _ = QFileDialog.getOpenFileName(self, self.language.opentdabinary, self.model.export_tdaDir, ';;'.join(filters_list), None)
        if filepath == '':
            return

        tda = TDA.load(filepath)
        self.setModel_from_tda(tda)

        self.updateAll()

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
        if self.model.isPredicted:
            if not self.savetda(isDefault=True):
                ret = QMessageBox.warning(self, self.language.discardallresults, self.language.discardallresultstext, QMessageBox.Yes | QMessageBox.No)
                if ret == QMessageBox.No:
                    return
            self.model.discardAll()

        #  change image if NOT predicted or
        #                 predicted and saved or
        #                 predicted and NOT saved and discard
        if isForward:
            self.model.forward()
        else:
            self.model.back()

        tda = self.model.get_default_tda()
        self.setModel_from_tda(tda)

        # set entire and update
        self.leftdock.radioButton_entire.click()

    def exportTableFile(self):
        filters_list = create_fileters(*ExportFileExtention.gen_filters_args(self.model.config.export_defaultFileFormat))
        filename = os.path.splitext(os.path.basename(self.model.default_savename))[0]
        filepath, selected_filter = QFileDialog.getSaveFileName(self, self.language.exportfileas, os.path.join(self.model.config.lastSavedTableFileDir, filename),
                                               ';;'.join(filters_list), None)
        #with open('./debug/texts.csv', 'w') as f:
        if filepath == '':
            return

        # too dirty...
        fileformat = selected_filter.split(' ')[0]
        ext = selected_filter.split('*.')[-1][:-1]
        def _check_and_append_ext(filepath, e):
            if os.path.splitext(filepath)[1] == '':
                filepath += '.' + e
            return filepath

        filepath = _check_and_append_ext(filepath, ext)
        if fileformat == 'CSV':
            self.model.saveAsCSV(filepath)

        elif fileformat == 'EXCEL':
            self.model.saveAsEXCEL(filepath)

        elif fileformat == 'TSV':
            self.model.saveAsTSV(filepath)

        elif fileformat == 'PSV':
            self.model.saveAsPSV(filepath)
        else:
            return
        self.model.set_lastSavedTableFileDir(filepath)
        QMessageBox.information(self, self.language.savedasdataset, self.language.savedasdatasettext.format(filepath, fileformat))

    def exportDataset(self):
        filters_list = create_fileters(*ExportDatasetFormat.gen_filters_args(self.model.config.lastSavedDatasetDir))
        filename = os.path.splitext(os.path.basename(self.model.imgpath))[0]
        filepath, selected_filter = QFileDialog.getSaveFileName(self, self.language.exportdataset,
                                                                os.path.join(self.model.export_datasetDir, filename),
                                                                ';;'.join(filters_list), None)
        # with open('./debug/texts.csv', 'w') as f:
        if filepath == '':
            return

        # too dirty...
        fileformat = selected_filter.split(' ')[0]
        ext = selected_filter.split('*.')[-1][:-1]

        def _check_and_append_ext(filepath, e):
            if os.path.splitext(filepath)[1] == '':
                filepath += '.' + e
            return filepath

        filepath = _check_and_append_ext(filepath, ext)
        if fileformat == 'VOC':
            self.model.saveAsVOC(filepath)
        else:
            return
        self.model.set_lastSavedDatasetDir(filepath)
        QMessageBox.information(self, self.language.savedasdataset, self.language.savedasdatasettext.format(filepath, fileformat))

    def undoredo(self, isUndo):
        if self.model.isPredicted:
            if self.model.showingmode == ShowingMode.ENTIRE:
                baseWidget = self.central.imageView
                parentQSize = self.model.areaQSize
                offsetQPoint = self.model.areaTopLeft
            elif self.model.showingmode == ShowingMode.SELECTED:
                baseWidget = self.central.imageView
                parentQSize = self.central.imageView.size()
                offsetQPoint = QPoint(0, 0)
            if isUndo:
                self.model.annotations.undo(baseWidget, parentQSize, offsetQPoint)
            else:
                self.model.annotations.redo(baseWidget, parentQSize, offsetQPoint)
        else:
            if isUndo:
                self.model.undo()
            else:
                self.model.redo()

        # update
        self.updateModel()
        self.updateAllUI()

    def zoomInOut(self, isZoomIn):
        if isZoomIn:
            r = min(self.leftdock.spinBox_zoom.value() + 10, 200)
        else:
            r = max(self.leftdock.spinBox_zoom.value() - 10, 20)

        # call zoomValueChanged
        self.leftdock.spinBox_zoom.setValue(r)

    def zoomValueChanged(self, value):
        # get the current ration on center position before zoom
        _, size = get_pixmap(self.model)
        hscrollBar = self.central.scrollArea.horizontalScrollBar()
        hratio = (hscrollBar.value() + hscrollBar.pageStep()/2) / size.width()

        vscrollBar = self.central.scrollArea.verticalScrollBar()
        vratio = (vscrollBar.value() + vscrollBar.pageStep()/2) / size.height()

        self.model.zoomvalue = value

        self.updateAll()

        # align center position after zoom
        _, size = get_pixmap(self.model)
        hscrollBar = self.central.scrollArea.horizontalScrollBar()
        hscrollBar.setValue(int(hratio * size.width()) - int(hscrollBar.pageStep()/2))

        vscrollBar = self.central.scrollArea.verticalScrollBar()
        vscrollBar.setValue(int(vratio * size.height()) - int(vscrollBar.pageStep()/2))


    def openAbout(self):
        aboutBox = AboutDialog(self)
        aboutBox.exec_()

    def openPreferences(self):
        preferencesBox = PreferencesDialog(self.model, initial=False, parent=self)
        preferencesBox.languageChanged.connect(self.updateLanguage)
        preferencesBox.exec_()

    def predmodeChanged(self, mode):
        self.model.predmode = mode

        self.updateAll()

    def showingmodeChanged(self, mode):
        self.model.showingmode = mode

        if self.model.showingmode == ShowingMode.SELECTED:
            if self.model.areamode == AreaMode.RECTANGLE:
                self.model.saveSelectedImg_rectmode(self.model.imgpath)
            elif self.model.areamode == AreaMode.QUADRANGLE:
                self.model.saveSelectedImg_quadmode(self.model.imgpath)

        self.updateAll()

    def areamodeChanged(self, mode):
        self.model.areamode = mode

        self.updateModel()
        self.updateAllUI()

    def done(self):
        # save to default directory
        if not self.savetda(isDefault=True):
            return
        # discard all results
        self.model.discardAll()
        # count up default_savename
        self.model.countup_defaultsavename()

        # set entire and update
        self.leftdock.radioButton_entire.click()


    def discard(self):
        if self.model.isPredicted:
            if self.model.annotations.isEdited:
                ret = QMessageBox.warning(self, self.language.discardallresults, self.language.discardallresultstext, QMessageBox.Yes | QMessageBox.No)
                if ret == QMessageBox.No:
                    return

        else:
            ret = QMessageBox.warning(self, self.language.discardarea, self.language.discardarreatext,
                                      QMessageBox.Yes | QMessageBox.No)
            if ret == QMessageBox.No:
                return

        self.model.discardAll()
        self.leftdock.radioButton_entire.click()
        # call areamodeChanged, so below codes are redundant
        # self.updateModel()
        # self.updateAllUI()

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

        else:
            try:
                # prediction
                # save image file in tmp before prediction
                if self.model.areamode == AreaMode.RECTANGLE:
                    if self.model.selectedImgPath is None:
                        self.model.saveSelectedImg_rectmode(self.model.imgpath)
                elif self.model.areamode == AreaMode.QUADRANGLE:
                    if self.model.selectedImgPath is None:
                        self.model.saveSelectedImg_quadmode(self.model.imgpath)

                if self.model.predmode == PredictionMode.IMAGE:
                    results = self.model.detectAsImage(imgpath=self.model.selectedImgPath)

                    if MainViewController.saveForDebug:
                        np.savetxt(os.path.join('debug', 'rect.csv'), self.model.rectangle.percent_points, delimiter=',')
                        if self.model.areamode == AreaMode.RECTANGLE:
                            self.model.saveAsJson(os.path.join('debug', 'result-rect-image.json'))
                        elif self.model.areamode == AreaMode.QUADRANGLE:
                            self.model.saveAsJson(os.path.join('debug', 'result-quad-image.json'))

                elif self.model.predmode == PredictionMode.DOCUMENT:
                    results = self.model.detectAsDocument(imgpath=self.model.selectedImgPath)

                    if MainViewController.saveForDebug:
                        np.savetxt(os.path.join('debug', 'poly.csv'), self.model.quadrangle.percent_points, delimiter=',')
                        if self.model.areamode == AreaMode.RECTANGLE:
                            self.model.saveAsJson(os.path.join('debug', 'result-rect-document.json'))
                        elif self.model.areamode == AreaMode.QUADRANGLE:
                            self.model.saveAsJson(os.path.join('debug', 'result-quad-document.json'))


            except PredictionError as e:
                # show messagebox
                ret = QMessageBox.critical(self, self.language.couldntpredict, self.language.couldntpredicttext.format(str(e)), QMessageBox.Yes)
                if ret == QMessageBox.Yes:
                    # remove tmp files
                    self.model.clearTmpImg()
                return
            except Exception as e:
                import traceback
                ret = QMessageBox.critical(self, self.language.unexpectederror, self.language.unexpectederrortext.format(str(e)), QMessageBox.Yes)
                if ret == QMessageBox.Yes:
                    # remove tmp files
                    self.model.clearTmpImg()
                return

        # set the annotations from the predicted results
        self.model.predictedArea.set_percent_points(self.model.areaPercentPts)
        self.model.predictedArea.set_parentVals(parentQSize=self.model.areaParentQSize, offsetQPoint=self.model.areaOffsetQPoint)
        if self.model.showingmode == ShowingMode.ENTIRE:
            self.model.set_results(results, baseWidget=self.central.imageView,
                                       parentQSize=self.model.areaQSize, offsetQPoint=self.model.areaTopLeft)

        elif self.model.showingmode == ShowingMode.SELECTED:
            self.model.set_results(results, baseWidget=self.central.imageView,
                                       parentQSize=self.central.imageView.size(), offsetQPoint=QPoint(0, 0))

        self.model.saveInDefaultDirectory()
        # update all
        self.updateAll()

        QMessageBox.information(self, self.language.notification, self.language.predictedtext.format(self.model.tdapath))

