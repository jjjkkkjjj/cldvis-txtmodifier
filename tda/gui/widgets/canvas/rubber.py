from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from ..eveUtils import MoveActionState

class Rubber(QRubberBand):
    def __init__(self, parent=None):
        super().__init__(QRubberBand.Rectangle, parent)

        self.resizeRBTopLeft = QRubberBand(QRubberBand.Rectangle, self)
        self.resizeRBTopRight = QRubberBand(QRubberBand.Rectangle, self)
        self.resizeRBButtomLeft = QRubberBand(QRubberBand.Rectangle, self)
        self.resizeRBButtomRight = QRubberBand(QRubberBand.Rectangle, self)

        # resize rubber band
        pal = QPalette()
        pal.setBrush(QPalette.Highlight, QBrush(Qt.red))
        self.resizeRBTopLeft.setPalette(pal)
        self.resizeRBTopRight.setPalette(pal)
        self.resizeRBButtomLeft.setPalette(pal)
        self.resizeRBButtomRight.setPalette(pal)

        self.editingRBArea = 20

    def press(self, pressPos_parent):

        if self.geometry().contains(pressPos_parent):
            # get relative position for this rubber
            # Note that the coordinates of 4 resize rubber band are relative position for this rubber
            pos_this = pressPos_parent - self.pos()
            if self.resizeRBTopLeft.geometry().contains(pos_this):
                # from br to tl
                startPos_parent = self.geometry().bottomRight()
                moveActionState = MoveActionState.RESIZE
            elif self.resizeRBTopRight.geometry().contains(pos_this):
                # from bl to tr
                startPos_parent = self.geometry().bottomLeft()
                moveActionState = MoveActionState.RESIZE
            elif self.resizeRBButtomLeft.geometry().contains(pos_this):
                # from tr to bl
                startPos_parent = self.geometry().topRight()
                moveActionState = MoveActionState.RESIZE
            elif self.resizeRBButtomRight.geometry().contains(pos_this):
                # from tl to br
                startPos_parent = self.geometry().topLeft()
                moveActionState = MoveActionState.RESIZE
            else: # move
                # for move amount by;
                # move_from_center = endPosition - (pressPos_parant - center_parent)
                #                  = (endPosition - pressPos_parent)=move + center_parent
                startPos_parent = pressPos_parent - self.pos()
                moveActionState = MoveActionState.MOVE  # means moving

        else:  # create new rubberband
            startPos_parent = pressPos_parent
            moveActionState = MoveActionState.CREATE

        return startPos_parent, moveActionState


    def setGeometry(self, newRBRect):
        """
        :param newRBRect: QRect
        :return:
        """
        super().setGeometry(newRBRect)

        # calculate resize rubber band parentQSize
        if min(newRBRect.width(), newRBRect.height()) < 80:
            self.editingRBArea = min(newRBRect.width(), newRBRect.height()) * 0.25
        else:
            self.editingRBArea = 20

        tlX, tlY = self.rect().topLeft().x(), self.rect().topLeft().y()
        brX, brY = self.rect().bottomRight().x(), self.rect().bottomRight().y()
        tr = self.rect().topRight()
        tr.setY(tlY + self.editingRBArea)
        bl = self.rect().bottomLeft()
        bl.setX(tlX + self.editingRBArea)

        # create resize rubber band
        self.resizeRBTopLeft.setGeometry(QRect(tlX, tlY, self.editingRBArea, self.editingRBArea))
        self.resizeRBTopRight.setGeometry(QRect(QPoint(brX - self.editingRBArea, tlY), tr))
        self.resizeRBButtomLeft.setGeometry(QRect(QPoint(tlX, brY - self.editingRBArea), bl))
        self.resizeRBButtomRight.setGeometry(QRect(QPoint(brX - self.editingRBArea, brY - self.editingRBArea), self.rect().bottomRight()))

        # show
        self.show()
        self.resizeRBTopLeft.show()
        self.resizeRBTopRight.show()
        self.resizeRBButtomLeft.show()
        self.resizeRBButtomRight.show()

    def resetWidget(self):
        self.rubberBand.hide()
        self.resizeRBTopLeft.hide()
        self.resizeRBTopRight.hide()
        self.resizeRBButtomLeft.hide()
        self.resizeRBButtomRight.hide()

class PredictedRubber(QRubberBand):
    def __init__(self, parent=None):
        super().__init__(QRubberBand.Rectangle, parent)

        pal = QPalette()
        pal.setBrush(QPalette.Highlight, QBrush(Qt.red))
        self.setPalette(pal)


