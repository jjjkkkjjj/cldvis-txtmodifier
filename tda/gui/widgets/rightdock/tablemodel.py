from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

class PredictionTableModel(QAbstractTableModel):
    def __init__(self, results):
        super().__init__()

        self._header_labels = ['Text']
        self._results = results

    def data(self, index, role=None):
        if role == Qt.DisplayRole:
            return self._results[index.row()]["text"]

    def headerData(self, section, orientation, role=None):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self._header_labels[section]
        return super().headerData(section, orientation, role)

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self._results)

    def columnCount(self, parent=None, *args, **kwargs):
        return 1