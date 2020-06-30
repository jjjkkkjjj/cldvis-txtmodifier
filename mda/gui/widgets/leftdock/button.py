from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

import pathlib

class Button(QPushButton):
    def __init__(self, icon_filename, parent=None):
        super().__init__(parent=parent)

        icon = QIcon(QPixmap(_get_iconpath(icon_filename)))
        self.setIcon(icon)


def _get_iconpath(icon_filename):
    icondir = pathlib.Path.joinpath(pathlib.Path(__file__).parent.parent.parent, 'icon')
    return str(pathlib.Path.joinpath(icondir, icon_filename))