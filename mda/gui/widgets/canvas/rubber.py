from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

class Rubber(QRubberBand):
    def __init__(self, parent=None):
        super().__init__(QRubberBand.Rectangle, parent)