from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

from ..utils.funcs import check_instance
from ..model import Model

class RightDockView(QWidget):
    ### Attributes ###
    label_predict: QLabel
    tableview: QTableView

    # model
    model: Model

    def __init__(self, model: Model, parent=None):
        super().__init__(parent=parent)

        self.model = check_instance('model', model, Model)
        self.initUI()
        self.updateUI()
        self.updateLanguage()

    def initUI(self):
        vbox = QVBoxLayout()

        self.label_predict = QLabel(self)
        self.label_predict.setText("Prediction")
        vbox.addWidget(self.label_predict)

        # self.textedit = QTextEdit(self)
        # vbox.addWidget(self.textedit)

        self.tableview = QTableView(self)
        self.tableview.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableview.setModel(self.model)
        vbox.addWidget(self.tableview)

        self.setLayout(vbox)

    def updateUI(self):
        self.model.layoutChanged.emit()
        self.tableview.repaint()

    def updateLanguage(self):
        language = self.model.language
        self.label_predict.setText(language.prediction)