from PySide2.QtWidgets import *
from google.auth.exceptions import DefaultCredentialsError
import cv2, os

from .model import Model
from .utils.modes import ShowingMode, AreaMode
from .utils.paint import *
from .utils.funcs import get_pixmap
from .view import *
from .viewController import *


class MainViewController(LeftDockVCMixin, CentralVCMixin, RightDockVCMixin, QMainWindow):
    debug = False
    saveForDebug = False
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
    @property
    def rightdock(self):
        return self.main.rightdock

    def initUI(self):
        self.main = MainView(self.model, self)
        self.setCentralWidget(self.main)

        self.menu = MenuBar(self.model, self)
        self.setMenuBar(self.menu)

    def updateAllUI(self):
        self.leftdock.updateUI()
        self.central.updateUI()
        self.rightdock.updateUI()
        self.menu.updateUI()

    def establish_connection(self):
        LeftDockVCMixin.establish_connection(self)
        CentralVCMixin.establish_connection(self)
        RightDockVCMixin.establish_connection(self)

    def check_credential(self):
        def showPreferences():
            dialog = PreferencesDialog(self.model, initial=True, parent=self)
            dialog.setCredentialJsonpath.connect(lambda path: setCredentialJsonpath(path))
            dialog.exec_()

        def setCredentialJsonpath(path):
            self.model.set_credentialJsonpath(path)

        if not self.model.isExistCredPath:
            showPreferences()
        elif not self.model.check_credentialJsonpath(self.model.credentialJsonpath):
            showPreferences()
        else:
            setCredentialJsonpath(self.model.credentialJsonpath)

    def updateModel(self):
        if not self.model.isExistImg:
            return

        if self.model.default_tdaname == '':
            filename = os.path.splitext(os.path.basename(self.model.imgpath))[0]
            self.model.default_tdaname = filename + '.tda'

        if not self.model.isPredicted:
            #### Not predicted ####

            # predicted area is inactive
            self.model.predictedArea.hide()
            if self.model.showingmode == ShowingMode.ENTIRE:
                #### Entire mode ####
                # set parant size and offset point
                _, originalImgQSize = get_pixmap(self.model)
                if self.model.areamode == AreaMode.RECTANGLE:
                    self.model.rectangle.show()
                    self.model.rectangle.set_parentVals(parentQSize=originalImgQSize)

                elif self.model.areamode == AreaMode.QUADRANGLE:
                    self.model.quadrangle.show()
                    self.model.quadrangle.set_parentVals(parentQSize=originalImgQSize)


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
                _, originalImgQSize = get_pixmap(self.model)
                self.model.predictedArea.set_parentVals(parentQSize=originalImgQSize)
                self.model.annotations.set_parentVals(parentQSize=self.model.predictedAreaQSize, offsetQPoint=self.model.predictedAreaTopLeft)
                if self.model.areamode == AreaMode.RECTANGLE:
                    # change area's color
                    self.model.predictedArea.set_color(poly_default_color=Color(border=orange, fill=transparency),
                                                       vertex_default_color=NoColor())
                    # area is shown only
                    self.model.predictedArea.show()
                    self.model.annotations.hide()

                elif self.model.areamode == AreaMode.QUADRANGLE:
                    # change area's color
                    self.model.predictedArea.set_color(poly_default_color=Color(border=orange, fill=light_orange),
                                                       vertex_default_color=NoColor())
                    # area and annotations are shown
                    self.model.predictedArea.show()
                    self.model.annotations.show()


            elif self.model.showingmode == ShowingMode.SELECTED:
                #### Selected mode ####

                # set parant size and offset point
                _, originalImgQSize = get_pixmap(self.model)
                if self.model.areamode == AreaMode.RECTANGLE:
                    self.model.annotations.set_parentVals(parentQSize=originalImgQSize, offsetQPoint=QPoint(0, 0))

                    self.model.predictedArea.hide()
                    self.model.annotations.show()

                elif self.model.areamode == AreaMode.QUADRANGLE:
                    self.model.annotations.set_parentVals(parentQSize=originalImgQSize, offsetQPoint=QPoint(0, 0))

                    self.model.predictedArea.hide()
                    self.model.annotations.show()


    def resizeEvent(self, event):
        self.updateAllUI()

    def closeEvent(self, event):
        self.model.clearTmpImg()