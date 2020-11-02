from PySide2.QtWidgets import *
import os, cv2
from google.auth.exceptions import DefaultCredentialsError

from .widgets import *
from .model import Model
from .functions.dialogs import CredentialDialog
from ..estimator.vision import Vision, PredictError


class MainWindowController(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.establish_connection()

        self.model = Model()

        self.check_enable()
        self.check_credential()

    def initUI(self):
        self.main = MainWidget(self)
        self.setCentralWidget(self.main)

        self.menu = MenuBar(self)
        self.setMenuBar(self.menu)

    @property
    def leftdock(self):
        return self.main.leftdock
    @property
    def canvas(self):
        return self.main.canvas

    def establish_connection(self):
        self.leftdock.enableChecking.connect(self.check_enable)
        self.canvas.enableChecking.connect(self.check_enable)
        self.leftdock.predicting.connect(lambda imgpath, tableRect, mode: self.predict(imgpath, tableRect, mode))

    def check_enable(self):
        # back forward
        self.leftdock.check_enable_backforward()
        self.menu.check_enable_backforward()

        # zoom
        self.leftdock.check_enable_zoom()
        self.menu.check_enable_zoom()

        # run
        self.canvas.check_enable()
        self.leftdock.check_enable_run()
        self.menu.check_enable_run()

    def predict(self, imgpath, tableRect, mode):
        """
        :param imgpath: str
        :param tableRect: tuple = (left, top, right, bottom) with percent mode
        :param mode: str, 'image' or 'file'
        :return:
        """
        if mode == 'image':

            # save tmp image
            # tmpimgpath = self.model.save_tmpimg(imgpath, tableRect)
            try:
                # detect
                # results = self.vision.detect_localImg(tmpimgpath)

                # for debug
                with open('.tda/tmp/result.json', 'r') as f:
                    import json
                    results = json.load(f)

                self.canvas.set_predictedRubber(results)
                #ここからRightDockに結果表示→選択されると，そのBBoxが表示されるようになる

            except PredictError as e:
                ret = QMessageBox.critical(self, 'Error', 'Error was occurred. Status: {}'.format(e), QMessageBox.Yes)
                if ret == QMessageBox.Yes:
                    # remove tmp files
                    self.model.remove_tmpimg()

        elif mode == 'file':
            pass
        else:
            raise ValueError('Invalid mode was passed')


    """
    credential
    """
    def check_credential(self):
        # jsonpath = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')

        if self.model.isExistCredPath:
            self.set_credential(self.model.credentialJsonpath)
        else:
            self.show_credentialDialog()

    def set_credential(self, path):
        """
        This method must be called in initialization
        :param path: str, credential json path
        :return:
        """
        try:
            self.vision = Vision(path)
            self.model.set_credentialJsonpath(path)
        except DefaultCredentialsError:
            ret = QMessageBox.critical(self, 'Invalid', '{} is invalid!'.format(path), QMessageBox.Yes)
            if ret == QMessageBox.Yes:
                self.show_credentialDialog()
        # ここらへんからapiとの接続を頑張る
        # https://cloud.google.com/vision/docs/ocr
        # https://www.youtube.com/watch?v=HMaoUdJQEgY
        # https://cloud.google.com/vision/docs/pdf

    def show_credentialDialog(self):
        dialog = CredentialDialog(self)
        dialog.pathSet.connect(lambda path: self.set_credential(path))
        dialog.exec_()