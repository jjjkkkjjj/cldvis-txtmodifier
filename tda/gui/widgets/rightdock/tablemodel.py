from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

class PredictionTableModel(QAbstractTableModel):

    def __init__(self):
        super().__init__(parent=None)

        self._header_labels = ['Text']

    @property
    def annotation(self):
        from ...mainWC import MainWindowController
        return MainWindowController.annotation

    def data(self, index, role=None):
        if role == Qt.DisplayRole:
            return self.get_text(index.row())

    def headerData(self, section, orientation, role=None):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self._header_labels[section]
        return super().headerData(section, orientation, role)

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.annotation)

    def columnCount(self, parent=None, *args, **kwargs):
        return 1

    def get_text(self, index):
        return self.annotation[index].text
    def get_bbox_percent(self, index):
        return self.annotation[index].points_percent

    """
    def __delitem__(self, index):
        self.layoutAboutToBeChanged.emit()
        del self.annotation[index]
        self.layoutChanged.emit()


    def append(self, text, points):
        self.layoutAboutToBeChanged.emit()
        self._prediction += [{'text': text, 'bbox': points}]
        self.layoutChanged.emit()
    """