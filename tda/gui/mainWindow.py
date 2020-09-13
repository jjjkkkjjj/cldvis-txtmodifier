from PySide2.QtWidgets import *
import os, cv2

from .widgets import *
from .model import Model
from ..estimator.wrapper import Estimator

class MainWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.initUI()
        self.establish_connection()

        self.model = Model()

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