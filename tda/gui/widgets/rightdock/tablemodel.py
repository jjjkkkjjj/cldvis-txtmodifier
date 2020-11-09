from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

class PredictionTableModel(QAbstractTableModel):
    def __init__(self, prediction):
        super().__init__(parent=None)

        self._header_labels = ['Text']
        self._prediction = prediction

    def data(self, index, role=None):
        if role == Qt.DisplayRole:
            return self._prediction[index.row()]["text"]

    def headerData(self, section, orientation, role=None):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self._header_labels[section]
        return super().headerData(section, orientation, role)

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self._prediction)

    def columnCount(self, parent=None, *args, **kwargs):
        return 1