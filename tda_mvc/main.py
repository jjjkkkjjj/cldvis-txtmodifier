from PySide2.QtWidgets import *
from google.auth.exceptions import DefaultCredentialsError

from .model import Model
from .view import *
from .viewController import *


class MainViewController(LeftDockVCMixin, QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # create model
        self.model = Model()
        self.initUI()
        self.establish_connection()

        # check credential
        self.check_credential()

    def initUI(self):
        self.main = MainView(self.model, self)
        self.setCentralWidget(self.main)

    def establish_connection(self):
        LeftDockVCMixin.establish_connection(self)

    def check_credential(self):
        def show_credentialDialog():
            dialog = CredentialDialog()
            dialog.pathSet.connect(lambda path: set_credential(path))
            dialog.exec_()

        def set_credential(path):
            """
            This method must be called in initialization
            # https://cloud.google.com/vision/docs/ocr
            # https://www.youtube.com/watch?v=HMaoUdJQEgY
            # https://cloud.google.com/vision/docs/pdf
            :param path: str, credential json path
            :return:
            """
            try:
                self.model.set_credentialJsonpath(path)

            except DefaultCredentialsError:
                ret = QMessageBox.critical(self, 'Invalid', '{} is invalid!'.format(path), QMessageBox.Yes)
                if ret == QMessageBox.Yes:
                    show_credentialDialog()

        if self.model.isExistCredPath:
            # set credential
            set_credential(self.model.credentialJsonpath)
        else:
            show_credentialDialog()




