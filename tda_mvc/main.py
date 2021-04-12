from PySide2.QtWidgets import *
from google.auth.exceptions import DefaultCredentialsError
import cv2

from .model import Model
from .utils.modes import ShowingMode, AreaMode
from .utils.paint import *
from .utils.funcs import get_pixmap
from .view import *
from .viewController import *


class MainViewController(LeftDockVCMixin, CentralVCMixin, QMainWindow):
    debug = False
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # create model
        self.model = Model()
        self.initUI()
        self.establish_connection()

        # check credential
        self.check_credential()

    @property
    def leftdock(self):
        return self.main.leftdock
    @property
    def central(self):
        return self.main.central

    def initUI(self):
        self.main = MainView(self.model, self)
        self.setCentralWidget(self.main)

        self.menu = MenuBar(self.model, self)
        self.setMenuBar(self.menu)

    def updateAllUI(self):
        self.leftdock.updateUI()
        self.central.updateUI()
        self.menu.updateUI()

    def establish_connection(self):
        LeftDockVCMixin.establish_connection(self)
        CentralVCMixin.establish_connection(self)

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

    def updateModel(self):
        if not self.model.isPredicted:
            #### Not predicted ####

            # predicted area is inactive
            self.model.predictedArea.hide()
            if self.model.showingmode == ShowingMode.ENTIRE:
                #### Entire mode ####
                # set parant size and offset point
                pixmap = get_pixmap(self.model)
                if self.model.areamode == AreaMode.RECTANGLE:
                    self.model.rectangle.show()
                    self.model.rectangle.set_parentVals(parentQSize=pixmap.size())

                elif self.model.areamode == AreaMode.QUADRANGLE:
                    self.model.quadrangle.show()
                    self.model.quadrangle.set_parentVals(parentQSize=pixmap.size())


            elif self.model.showingmode == ShowingMode.SELECTED:
                #### Selected mode ####
                if self.model.areamode == AreaMode.RECTANGLE:
                    self.model.rectangle.hide()
                elif self.model.areamode == AreaMode.QUADRANGLE:
                    self.model.quadrangle.hide()


        else:
            #### predicted ####
            # rectangle and quadrangle are inactivate
            self.model.rectangle.hide()
            self.model.quadrangle.hide()

            if self.model.showingmode == ShowingMode.ENTIRE:
                #### Entire mode ####
                # set parant size and offset point
                pixmap = get_pixmap(self.model)
                self.model.predictedArea.set_parentVals(parentQSize=pixmap.size())
                self.model.set_parentVals_annotations(parentQSize=self.model.predictedAreaQSize, offsetQPoint=self.model.predictedAreaTopLeft)
                if self.model.areamode == AreaMode.RECTANGLE:
                    # change area's color
                    self.model.predictedArea.set_color(poly_default_color=Color(border=orange, fill=transparency),
                                                       vertex_default_color=NoColor())
                    # area is shown only
                    self.model.predictedArea.show()
                    self.model.hide_annotations()

                elif self.model.areamode == AreaMode.QUADRANGLE:
                    # change area's color
                    self.model.predictedArea.set_color(poly_default_color=Color(border=orange, fill=light_orange),
                                                       vertex_default_color=NoColor())
                    # area and annotations are shown
                    self.model.predictedArea.show()
                    self.model.show_annotations()


            elif self.model.showingmode == ShowingMode.SELECTED:
                #### Selected mode ####

                # set parant size and offset point
                pixmap = get_pixmap(self.model)
                if self.model.areamode == AreaMode.RECTANGLE:
                    self.model.set_parentVals_annotations(parentQSize=pixmap.size(), offsetQPoint=QPoint(0, 0))

                    self.model.predictedArea.hide()
                    self.model.show_annotations()

                elif self.model.areamode == AreaMode.QUADRANGLE:
                    self.model.set_parentVals_annotations(parentQSize=pixmap.size(), offsetQPoint=QPoint(0, 0))

                    self.model.predictedArea.hide()
                    self.model.show_annotations()


    def closeEvent(self, event):
        self.model.clearTmpImg()