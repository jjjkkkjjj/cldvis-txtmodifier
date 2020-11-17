from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from .._utils import _add_actions, _create_action

class ImgContextMenu(QMenu):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        # polygon
        self.action_remove_polygon = _create_action(self, "&Remove Polygon", slot=None,
                                                    tip="remove selected polygon")
        self.action_duplicate_polygon = _create_action(self, "&Duplicate Polygon", slot=None,
                                                       tip="duplicate selected polygon")

        # point
        self.action_remove_point = _create_action(self, "&Remove Point", slot=None,
                                                    tip="remove selected point")
        self.action_duplicate_point = _create_action(self, "&Duplicate Point", slot=None,
                                                       tip="duplicate selected point")

        _add_actions(self, (self.action_remove_polygon, self.action_duplicate_polygon, None,
                            self.action_remove_point, self.action_duplicate_point))

    def setEnabled_action(self, mode):
        pass