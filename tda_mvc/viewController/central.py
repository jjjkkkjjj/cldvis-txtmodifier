from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import os

from ..utils.modes import AreaMode, ShowingMode
from ..utils.funcs import get_pixmap
from ..view.dialog import EditDialog
from .base import VCAbstractMixin

class CentralVCMixin(VCAbstractMixin):

    @property
    def imageView(self):
        return self.central.imageView

    def establish_connection(self):
        self.central.label_filename.enterEvent = lambda e: self.label_mouseover(e, 'filename', True)
        self.central.label_filename.leaveEvent = lambda e: self.label_mouseover(e, 'filename', False)
        self.central.label_filename.mouseDoubleClickEvent = lambda e: self.label_doubleClicked(e, 'filename')
        self.central.label_savefilename.enterEvent = lambda e: self.label_mouseover(e, 'savefilename', True)
        self.central.label_savefilename.leaveEvent = lambda e: self.label_mouseover(e, 'savefilename', False)
        self.central.label_savefilename.mouseDoubleClickEvent = lambda e: self.label_doubleClicked(e, 'savefilename')

        self.imageView.rightClicked.connect(lambda e: self.rightClicked(e))
        self.imageView.mouseReleased.connect(lambda e: self.mouseReleased(e))
        self.imageView.mousePressed.connect(lambda e: self.mousePressed(e))
        self.imageView.mouseMoved.connect(lambda e: self.mouseMoved(e))
        self.imageView.mouseDoubleClicked.connect(lambda e: self.mouseDoubleClicked(e))
        self.imageView.filesDropped.connect(lambda filepaths: self.dropped(filepaths))

    def label_mouseover(self, e: QMouseEvent, labelname, isEnter):
        label: QLabel
        if labelname == 'filename':
            label = self.central.label_filename
        elif labelname == 'savefilename':
            label = self.central.label_savefilename
        else:
            return

        if not label.isEnabled():
            return
        if isEnter:
            label.setStyleSheet('color: red')
        else:
            label.setStyleSheet('color: black')

    def label_doubleClicked(self, e: QMouseEvent, labelname):
        language = self.model.language
        if labelname == 'filename':

            filename, ok = QInputDialog.getItem(self, language.selectfilenametitle, language.selectfilenametext.format(self.model.imgpath),
                                                self.model.imgfilenames, self.model.currentImgIndex, False)
            if ok and filename != self.model.currentImgfilename:
                # check whether to discard
                if not self.savetda(isDefault=True):
                    ret = QMessageBox.warning(self, language.discardallresults,
                                              language.discardallresultstext, QMessageBox.Yes | QMessageBox.No)
                    if ret == QMessageBox.No:
                        return
                self.model.discardAll()

                imgIndex = self.model.imgfilenames.index(filename)
                self.model.set_imgIndex(imgIndex)

                # load tda file
                tda = self.model.get_default_tda()
                self.setModel_from_tda(tda)

                # set entire and update
                self.leftdock.radioButton_entire.click()

        elif labelname == 'savefilename':
            savefilename, ok = QInputDialog.getText(self, language.setsavenametitle, '{}:'.format(language.savename), text=self.model.default_savename)

            if ok:
                _, ext = os.path.splitext(savefilename)
                if ext != '.tda':
                    savefilename += '.tda'
                self.model.default_savename = savefilename

                self.updateModel()
                self.updateAllUI()

    @property
    def predictedParentQSize(self):
        if self.model.showingmode == ShowingMode.SELECTED:
            _, originalImgQSize = get_pixmap(self.model)
            return originalImgQSize
        elif self.model.showingmode == ShowingMode.ENTIRE:
            return self.model.predictedAreaQSize
        return None

    def dropped(self, filepaths):
        self.model.set_imgPaths(filepaths)
        tda = self.model.get_default_tda()
        self.setModel_from_tda(tda)

        # update view
        self.updateModel()
        self.updateAllUI()

    @property
    def isMouseDisabled(self):
        return self.model.isPredicted and self.model.areamode == AreaMode.QUADRANGLE and self.model.showingmode == ShowingMode.ENTIRE

    def rightClicked(self, e: QContextMenuEvent):
        if not self.model.isExistImg:
            return

        if not self.model.isPredicted or self.isMouseDisabled:
            return

        contextMenu = self.imageView.contextMenu
        contextMenu.updateUI()
        action = contextMenu.exec_(self.imageView.mapToGlobal(e.pos()))
        if action == contextMenu.action_remove_annotation:
            self.model.annotations.remove_selectedAnnotation()
        elif action == contextMenu.action_duplicate_annotation:
            self.model.annotations.duplicate_selectedAnnotation()
        elif action == contextMenu.action_remove_point:
            self.model.annotations.remove_selectedAnnotationPoint()
        elif action == contextMenu.action_duplicate_point:
            self.model.annotations.duplicate_selectedAnnotationPoint()

        self.updateModel()
        self.updateAllUI()


    def mousePressed(self, e: QMouseEvent):
        if e.buttons() == Qt.RightButton:
            self.model.mouseClick_scroll(e.pos())
            return

        if not self.model.isExistImg:
            return

        if self.isMouseDisabled:
            return

        if self.model.isPredicted:
            self.model.annotations.mousePress(e.pos(), self.predictedParentQSize)

        else:
            if self.model.areamode == AreaMode.RECTANGLE:
                self.model.mousePress_rectmode(e.pos(), self.imageView.size())

            elif self.model.areamode == AreaMode.QUADRANGLE:
                self.model.mousePress_quadmode(e.pos(), self.imageView.size())

        self.modelUpdateAftermouseEvent()

    def mouseMoved(self, e: QMouseEvent):
        pos = e.pos()
        if e.buttons() == Qt.RightButton:
            movedAmount = self.model.mouseMove_scroll(pos)

            hscrollBar = self.central.scrollArea.horizontalScrollBar()
            hscrollBar.setValue(hscrollBar.value() + movedAmount.x())

            vscrollBar = self.central.scrollArea.verticalScrollBar()
            vscrollBar.setValue(vscrollBar.value() + movedAmount.y())
            return

        if not self.model.isExistImg:
            return

        if self.isMouseDisabled:
            return

        if self.model.isPredicted:
            if e.buttons() == Qt.LeftButton:
                self.model.annotations.mouseMoveClicked(pos, self.predictedParentQSize)
            elif e.buttons() == Qt.NoButton:
                self.model.annotations.mouseMoveNoButton(pos)
                if self.model.annotations.isExistSelectedAnnotation:
                    self.rightdock.tableview.selectRow(self.model.annotations.selectedAnnotationIndex)
        else:
            if e.buttons() == Qt.LeftButton:
                # in clicking
                if self.model.areamode == AreaMode.RECTANGLE:
                    self.model.mouseMoveClicked_rectmode(pos, self.imageView.size())
                elif self.model.areamode == AreaMode.QUADRANGLE:
                    self.model.mouseMoveClicked_quadmode(pos, self.imageView.size())

            elif e.buttons() == Qt.NoButton:
                if self.model.areamode == AreaMode.RECTANGLE:
                    self.model.mouseMoveNoButton_rectmode(pos)
                elif self.model.areamode == AreaMode.QUADRANGLE:
                    self.model.mouseMoveNoButton_quadmode(pos)

        # scroll
        hscrollBar = self.central.scrollArea.horizontalScrollBar()
        if pos.x() < hscrollBar.value() or hscrollBar.value() + hscrollBar.pageStep() < pos.x():
            if pos.x() < hscrollBar.value():
                movedX = pos.x() - hscrollBar.value()
            else:
                movedX = pos.x() - (hscrollBar.value() + hscrollBar.pageStep())
            hscrollBar.setValue(hscrollBar.value() + movedX)

        vscrollBar = self.central.scrollArea.verticalScrollBar()
        if pos.y() < vscrollBar.value() or vscrollBar.value() + vscrollBar.pageStep() < pos.y():
            if pos.y() < vscrollBar.value():
                movedY = pos.y() - vscrollBar.value()
            else:
                movedY = pos.y() - (vscrollBar.value() + vscrollBar.pageStep())
            vscrollBar.setValue(vscrollBar.value() + movedY)

        self.modelUpdateAftermouseEvent()

    def mouseReleased(self, e: QMouseEvent):
        if e.buttons() == Qt.RightButton:
            self.model.mouseRelease_scroll()
            return

        if not self.model.isExistImg:
            return

        if self.isMouseDisabled:
            return

        if self.model.isPredicted:
            self.model.annotations.mouseRelease()

        else:
            if self.model.areamode == AreaMode.RECTANGLE:
                self.model.mouseRelease_rectmode()
            elif self.model.areamode == AreaMode.QUADRANGLE:
                self.model.mouseRelease_quadmode()

        self.modelUpdateAftermouseEvent()
        self.leftdock.updateUI()
        self.menu.updateUI()

    def mouseDoubleClicked(self, e: QMouseEvent):
        if not self.model.isExistImg:
            return

        if not self.model.annotations.isExistSelectedAnnotation or self.isMouseDisabled:
            return

        def edited(text):
            self.model.annotations.set_text_selectedAnnoatation(text)
            self.updateAllUI()

        def remove():
            self.model.annotations.remove_selectedAnnotation()
            self.updateModel()
            self.updateAllUI()

        editDialog = EditDialog(self.model, self)
        editDialog.edited.connect(lambda text: edited(text))
        editDialog.removed.connect(remove)
        editDialog.exec_()

    def modelUpdateAftermouseEvent(self):
        if not self.model.isPredicted:
            self.model.predictedArea.hide()
            if self.model.showingmode == ShowingMode.SELECTED:
                self.model.rectangle.hide()
                self.model.quadrangle.hide()
                self.imageView.setEnabled(False)

            elif self.model.showingmode == ShowingMode.ENTIRE:
                if self.model.areamode == AreaMode.RECTANGLE:
                    self.model.rectangle.show()
                    self.model.quadrangle.hide()
                elif self.model.areamode == AreaMode.QUADRANGLE:
                    self.model.rectangle.hide()
                    self.model.quadrangle.show()
                self.imageView.setEnabled(True)
        else:
            self.model.rectangle.hide()
            self.model.quadrangle.hide()
            if self.model.showingmode == ShowingMode.ENTIRE:
                self.model.predictedArea.show()
            elif self.model.showingmode == ShowingMode.SELECTED:
                self.model.predictedArea.hide()
            self.imageView.setEnabled(True)

        self.imageView.repaint()