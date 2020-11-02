from PySide2.QtWidgets import *
import os, cv2
from google.auth.exceptions import DefaultCredentialsError

from .widgets import *
from .model import Model
from .functions.dialogs import CredentialDialog
from ..estimator.wrapper import Estimator

class MainWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.initUI()
        self.establish_connection()

        self.model = Model()

        self.check_credential()

    def initUI(self):
        hbox = QHBoxLayout(self)

        # leftdock
        self.leftdock = LeftDockWidget(self)
        hbox.addWidget(self.leftdock, 1)

        # canvas as central widget
        self.canvas = CanvasWidget(self)
        hbox.addWidget(self.canvas, 7)

        # rightdock
        self.rightdock = RightDockWidget(self)
        hbox.addWidget(self.rightdock, 2)
        self.setLayout(hbox)

    def establish_connection(self):
        self.leftdock.imgChanged.connect(self.canvas.set_img)
        self.leftdock.ratioChanged.connect(self.canvas.set_img)
        self.leftdock.rectRemoved.connect(lambda: self.canvas.set_rubber(None))
        #self.leftdock.datasetAdding.connect()

    def check_credential(self):
        #jsonpath = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')

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
            self.model.set_credentialJsonpath(path)
        except DefaultCredentialsError:
            ret = QMessageBox.critical(self, 'Invalid', '{} is invalid!'.format(path), QMessageBox.Yes)
            if ret == QMessageBox.Yes:
                self.show_credentialDialog()
        #ここらへんからapiとの接続を頑張る
        #https://cloud.google.com/vision/docs/ocr
        #https://www.youtube.com/watch?v=HMaoUdJQEgY
        #https://cloud.google.com/vision/docs/pdf

    def show_credentialDialog(self):
        dialog = CredentialDialog(self)
        dialog.pathSet.connect(lambda path: self.set_credential(path))
        dialog.exec_()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.establish_connection()
        self.estimator = Estimator()

        self.check_enable()

    def initUI(self):
        self.main = MainWidget(self)
        self.setCentralWidget(self.main)

        self.menu = MenuBar(self.main)
        self.setMenuBar(self.menu)

    def establish_connection(self):
        self.main.leftdock.enableChecking.connect(self.check_enable)
        self.main.canvas.enableChecking.connect(self.check_enable)
        self.main.leftdock.predicting.connect(lambda imgpath, tableRect: self.predict(imgpath, tableRect))

    def check_enable(self):
        # back forward
        self.main.leftdock.check_enable_backforward()
        self.menu.check_enable_backforward()

        # zoom
        self.main.leftdock.check_enable_zoom()
        self.menu.check_enable_zoom()

        # run
        self.main.canvas.check_enable()
        self.main.leftdock.check_enable_run()
        self.menu.check_enable_run()

    def predict(self, imgpath, tableRect):
        """
        :param imgpath: str
        :param tableRect: tuple = (left, top, right, bottom) with percent mode
        :return:
        """

        def save(directory='./img'):
            img = cv2.imread(imgpath)
            h, w, _ = img.shape

            xmin, ymin, xmax, ymax = tableRect
            xmin, xmax = int(xmin * w), int(xmax * w)
            ymin, ymax = int(ymin * h), int(ymax * h)

            filename, ext = os.path.splitext(os.path.basename(imgpath))
            apex = '_x{}X{}y{}Y{}'.format(xmin, xmax, ymin, ymax)
            savepath = os.path.abspath(os.path.join(directory, filename + apex + '.jpg'))

            cv2.imwrite(savepath, img[ymin:ymax, xmin:xmax])

        save()