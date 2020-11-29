from PySide2.QtWidgets import *
from PySide2.QtCore import *

from google.auth.exceptions import DefaultCredentialsError

from .functions.dialogs import CredentialDialog
from .model import Info, Annotation
from ..estimator.vision import Vision, PredictError
from .widgets import *

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
    info: Info
    annotation: Annotation

    def establish_connection(self):
        pass


class UtilMixin(MWAbstractMixin):
    def establish_connection(self):
        # check enable
        self.leftdock.enableChecking.connect(self.check_enable)
        self.canvas.enableChecking.connect(self.check_enable)

    def check_enable(self):
        # back forward
        self.leftdock.check_enable_backforward(self.info.isExistBackImg, self.info.isExistForwardImg)
        self.menu.check_enable_backforward(self.info.isExistBackImg, self.info.isExistForwardImg)

        # zoom
        self.leftdock.check_enable_zoom(self.info.isExistImg)
        self.menu.check_enable_zoom(self.info.isExistImg)

        # run
        self.canvas.check_enable(self.info.isExistImg)
        self.leftdock.check_enable_run(self.info.isExistRubberPercentRect)
        self.menu.check_enable_run(self.info.isExistRubberPercentRect)

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
        self.leftdock.rectRemoved.connect(lambda: self.canvas.set_rubber(None))

        # rubber
        self.canvas.rubberCreated.connect(lambda rubberPercentRect: self.set_rubber(rubberPercentRect))

    """
    rubber
    """
    def set_rubber(self, rubberPercentRect):
        self.info.set_rubberPercentRect(rubberPercentRect)
        self.canvas.set_rubber(rubberPercentRect)

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
        self.leftdock.predicting.connect(lambda mode: self.predict(self.info.imgpath, self.info.rubberPercentRect, mode))

        # img
        self.canvas.img.contextActionSelected.connect(lambda actionType, index: self.set_contextAction(actionType, index))


    def predict(self, imgpath, tableRect, mode):
        """
        :param imgpath: str
        :param tableRect: tuple = (left, top, right, bottom) with percent mode
        :param mode: str, 'image' or 'file'
        :return:
        """
        if mode == 'image':
            from ..debug._utils import DEBUG
            if DEBUG:
                # for debug
                with open('tda/debug/result.json', 'r') as f:
                    import json
                    results = json.load(f)

            else:
                # TODO: show loading dialog
                # save tmp image
                tmpimgpath = self.info.save_tmpimg(imgpath, tableRect)
                try:
                    # detect
                    results = self.vision.detect_localImg(tmpimgpath)

                except PredictError as e:
                    ret = QMessageBox.critical(self, 'Error', 'Error was occurred. Status: {}'.format(e), QMessageBox.Yes)
                    if ret == QMessageBox.Yes:
                        # remove tmp files
                        self.info.remove_tmpimg()


            self.canvas.set_predictedRubber(results)
            self.rightdock.set_results(results)

        elif mode == 'file':
            pass
        else:
            raise ValueError('Invalid mode was passed')


    def set_contextAction(self, actionType, index):
        self.canvas.img.set_contextAction(actionType, index)
        self.rightdock.set_contextAction(actionType, index)
        # tablemodelとimgのpolygonをまとめて，mvcモデルを作る