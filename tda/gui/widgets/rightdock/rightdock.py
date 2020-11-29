from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from ..baseWidget import BaseWidget
from .tablemodel import PredictionTableModel
from ..eveUtils import *

class RightDockWidget(BaseWidget):
    def __init__(self, mainWidgetController):
        super().__init__(mainWidgetController)

        self.initUI()
        self.tableModel = PredictionTableModel()
        self.tableview.setModel(self.tableModel)

    def initUI(self):
        vbox = QVBoxLayout()

        self.label_predict = QLabel(self)
        self.label_predict.setText("Prediction")
        vbox.addWidget(self.label_predict)

        #self.textedit = QTextEdit(self)
        #vbox.addWidget(self.textedit)

        self.tableview = QTableView(self)
        self.tableview.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        vbox.addWidget(self.tableview)

        self.setLayout(vbox)


    def set_contextAction(self, actionType, index):
        if actionType == ContextActionType.REMOVE_ANNOTATION:
            del self.tableModel[index]
        elif actionType == ContextActionType.DUPLICATE_ANNOTATION:
            self.tableModel.append(self.tableModel.get_text(index), self.tableModel.get_bbox(index))
        elif actionType == ContextActionType.REMOVE_POINT:
            pass
        elif actionType == ContextActionType.DUPLICATE_POINT:
            pass
        self.tableview.repaint()