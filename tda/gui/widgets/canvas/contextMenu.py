from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from .._utils import _add_actions, _create_action

class ImgContextMenu(QMenu):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        # annotation
        self.action_remove_annotation = _create_action(self, "&Remove Annotation", slot=None,
                                                    tip="remove selected annotation")
        self.action_duplicate_annotation = _create_action(self, "&Duplicate Annotation", slot=None,
                                                       tip="duplicate selected annotation")

        # point
        self.action_remove_point = _create_action(self, "&Remove Point", slot=None,
                                                    tip="remove selected point")
        self.action_duplicate_point = _create_action(self, "&Duplicate Point", slot=None,
                                                       tip="duplicate selected point")

        _add_actions(self, (self.action_remove_annotation, self.action_duplicate_annotation, None,
                            self.action_remove_point, self.action_duplicate_point))

    def setEnabled_action(self, isSelectedPolygon, isSelectedPoint):
        # annotation
        self.action_remove_annotation.setEnabled(isSelectedPolygon)
        self.action_duplicate_annotation.setEnabled(isSelectedPolygon)

        # point
        self.action_remove_point.setEnabled(isSelectedPoint)
        self.action_duplicate_point.setEnabled(isSelectedPoint)