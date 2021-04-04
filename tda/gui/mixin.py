from PySide2.QtWidgets import *
from PySide2.QtCore import *

from google.auth.exceptions import DefaultCredentialsError

from .functions.dialogs import CredentialDialog
from .model import InfoManager, AnnotationManager, SelectionManager
from ..estimator.vision import Vision, PredictError
from .widgets import *
from .widgets.eveUtils import AreaMode
from .widgets.eveUtils import PredictionMode, ShowingMode

class MWAbstractMixin(object):
    # widget
    leftdock: LeftDockWidget
    canvas: CanvasWidget
    rightdock: RightDockWidget
    main: MainWidget
    menu: MenuBar
    # gcp
    vision: Vision
    # info
    info: InfoManager
    annotation: AnnotationManager
    selection: SelectionManager

    def establish_connection(self):
        pass


class UtilMixin(MWAbstractMixin):
    def establish_connection(self):
        # check enable
        self.leftdock.enableChecking.connect(self.check_enable)
        self.canvas.enableChecking.connect(self.check_enable)

        # change showing mode
        self.leftdock.showingChanged.connect(self.showingModeChanged)

    def check_enable(self):
        # back forward
        self.leftdock.check_enable_backforward(self.info.isExistBackImg, self.info.isExistForwardImg)
        self.menu.check_enable_backforward(self.info.isExistBackImg, self.info.isExistForwardImg)

        # zoom
        self.leftdock.check_enable_zoom(self.info.isExistImg)
        self.menu.check_enable_zoom(self.info.isExistImg)

        # showing
        self.leftdock.check_enable_radioButtionShowing(self.info.isExistAreaPercentRect)

        # run
        self.canvas.check_enable(self.info.isExistImg)
        self.leftdock.check_enable_run(self.info.isExistAreaPercentRect)
        self.menu.check_enable_run(self.info.isExistAreaPercentRect)

        # TODO: check enable function in editing

    """
    credential
    """
    def check_credential(self):
        # jsonpath = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')

        if self.info.isExistCredPath:
            self.set_credential(self.info.credentialJsonpath)
        else:
            self.show_credentialDialog()

    def set_credential(self, path):
        """
        This method must be called in initialization
        # https://cloud.google.com/vision/docs/ocr
        # https://www.youtube.com/watch?v=HMaoUdJQEgY
        # https://cloud.google.com/vision/docs/pdf
        :param path: str, credential json path
        :return:
        """
        try:
            self.vision = Vision(path)
            self.info.set_credentialJsonpath(path)
        except DefaultCredentialsError:
            ret = QMessageBox.critical(self, 'Invalid', '{} is invalid!'.format(path), QMessageBox.Yes)
            if ret == QMessageBox.Yes:
                self.show_credentialDialog()

    def showingModeChanged(self):
        zoomvalue = self.leftdock.spinBox_zoom.value()
        if self.leftdock.showingmode == ShowingMode.ALL:
            self.canvas.set_img(self.info.imgpath, zoomvalue)

        elif self.leftdock.showingmode == ShowingMode.SELECTED:
            from ..debug._utils import DEBUG
            if DEBUG:
                tmpimgpath = '.tda/tmp/20200619173238005_x355X2640y337Y1787.jpg'
            else:
                tmpimgpath = self.info.save_tmpimg(self.info.imgpath, self.info.areaPercentPolygon, self.selection.predictionMode)
            self.canvas.set_img(tmpimgpath, zoomvalue)


    def show_credentialDialog(self):
        dialog = CredentialDialog(self)
        dialog.pathSet.connect(lambda path: self.set_credential(path))
        dialog.exec_()

class SelectionMixin(MWAbstractMixin):

    def establish_connection(self):
        # button action
        self.leftdock.imgSet.connect(lambda paths, value: self.set_imgpath(paths, value))
        self.leftdock.imgChanged.connect(lambda isBack, value: self.change_img(isBack, value))
        self.leftdock.ratioChanged.connect(lambda value: self.set_img(value))
        self.leftdock.rectRemoved.connect(lambda: self.canvas.set_selectionArea(None))

        # rubber
        self.canvas.selectionAreaCreated.connect(lambda areaPercentPolygon: self.set_selectionArea(areaPercentPolygon))
        self.canvas.img.painting.connect(lambda painter: self.paint_area(painter))

        # mode change
        self.leftdock.predictionModeChanged.connect(lambda mode: self.mode_change(mode))
    """
    rubber
    """
    def set_selectionArea(self, areaPercentPolygon):
        self.info.set_selectionArea(areaPercentPolygon)
        self.canvas.set_selectionArea(areaPercentPolygon)

    def paint_area(self, painter):
        self.selection.area.paint(painter)

    def mode_change(self, mode):
        mode = PredictionMode(mode)
        if mode == PredictionMode.IMAGE:
            self.main.changeUIRatio(1, 7, 2)
        elif mode == PredictionMode.TABLE:
            self.main.changeUIRatio(1, 4, 3)
        self.selection.predictionMode = mode

    """
    img
    """
    def set_imgpath(self, paths, value):
        self.info.set_imgPaths(paths)
        self.set_img(value)

    def change_img(self, isBack, value):
        if isBack:
            self.info.back()
        else:
            self.info.forward()
        self.set_img(value)

    def set_img(self, value):
        self.canvas.set_img(self.info.imgpath, value)

class PredictionMixin(MWAbstractMixin):

    def establish_connection(self):
        # button action
        # self.leftdock.datasetAdding.connect()
        self.leftdock.predicting.connect(lambda: self.predict(self.info.imgpath, self.info.areaPercentPolygon))

        # img
        self.canvas.img.painting.connect(lambda painter: self.paint_annotations(painter))
        self.canvas.img.contextActionSelected.connect(lambda actionType: self.set_contextAction(actionType))


    def predict(self, imgpath, areaPercentPolygon):
        """
        :param imgpath: str
        :param areaPercentPolygon:
            image mode;
                tuple = (xmin, ymin, xmax, ymax) with percent mode
            table mode;
                tuple = (tl, tr, br, bl) with percent mode
        :return:
        """
        if self.leftdock.predictionmode == PredictionMode.IMAGE:
            from ..debug._utils import DEBUG
            if DEBUG:
                import numpy as np
                areaPercentPolygon = np.loadtxt('tda/debug/image_rect.csv', delimiter=',')
                # for debug
                with open('tda/debug/result-rect.json', 'r') as f:
                    import json
                    results = json.load(f)

            else:
                # TODO: show loading dialog
                # save tmp image
                tmpimgpath = self.info.save_tmpimg(imgpath, areaPercentPolygon, self.leftdock.predictionmode)
                try:
                    # detect
                    results = self.vision.detect_localImg(tmpimgpath)

                except PredictError as e:
                    ret = QMessageBox.critical(self, 'Error', 'Error was occurred. Status: {}'.format(e), QMessageBox.Yes)
                    if ret == QMessageBox.Yes:
                        # remove tmp files
                        self.info.remove_tmpimg()

            self.canvas.switch_areaMode(areamode=AreaMode.PREDICTION, showingmode=self.leftdock.showingmode)
            # showing changeの際の変換
            if self.leftdock.showingmode == ShowingMode.ALL:
                parentQSize = self.selection.area.qsize
                offsetQPoint = self.selection.area.topLeft
            else:
                parentQSize = self.canvas.img.size()
                offsetQPoint = QPoint(0, 0)
            self.annotation.set_detectionResult(results, baseWidget=self.canvas.img,
                                                parentQSize=parentQSize, offsetQPoint=offsetQPoint)
            self.annotation.show()
            self.update_contents()


        elif self.leftdock.predictionmode == PredictionMode.TABLE:
            from ..debug._utils import DEBUG
            if DEBUG:
                import numpy as np
                # for debug
                areaPercentPolygon = np.loadtxt('tda/debug/table_polygon.csv', delimiter=',')
                # for debug
                with open('tda/debug/result-table.json', 'r') as f:
                    import json
                    results = json.load(f)
            else:
                tmpimgpath = self.info.save_tmpimg(imgpath, areaPercentPolygon, self.leftdock.predictionmode)
                try:
                    # detect
                    results = self.vision.detect_localImg(tmpimgpath)

                except PredictError as e:
                    ret = QMessageBox.critical(self, 'Error', 'Error was occurred. Status: {}'.format(e), QMessageBox.Yes)
                    if ret == QMessageBox.Yes:
                        # remove tmp files
                        self.info.remove_tmpimg()

            #とりあえず，imageの表示方法と共通化．共通化の際にエリアの拡大表示．
            self.canvas.switch_areaMode(areamode=AreaMode.PREDICTION, showingmode=self.leftdock.showingmode)
            if self.leftdock.showingmode == ShowingMode.ALL:
                parentQSize = self.selection.area.qsize
                offsetQPoint = self.selection.area.topLeft
            else:
                parentQSize = self.canvas.img.size()
                offsetQPoint = QPoint(0, 0)
            self.annotation.set_detectionResult(results, baseWidget=self.canvas.img,
                                                parentQSize=parentQSize, offsetQPoint=offsetQPoint)
            self.annotation.show()
            self.update_contents()
        else:
            raise ValueError('Invalid mode was passed')

    def paint_annotations(self, painter):
        for anno in self.annotation:
            anno.paint(painter)

    def set_contextAction(self, actionType):
        self.annotation.change_annotations(actionType)
        self.update_contents()

    def update_contents(self):
        """
        update contents when changing data
        :return:
        """
        # draw polygons
        self.canvas.img.repaint()
        # update table contents
        self.rightdock.tableModel.layoutChanged.emit()