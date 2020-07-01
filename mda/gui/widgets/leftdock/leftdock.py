from .button import Button
from ...functions.dialogs import *

class LeftDockWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()

        self.button_openfolder = Button('folder.png')
        self.button_openfolder.clicked.connect(lambda: self.openDialog('folder'))
        vbox.addWidget(self.button_openfolder)

        self.button_openfile = Button('file.png')
        self.button_openfile.clicked.connect(lambda: self.openDialog('file'))
        vbox.addWidget(self.button_openfile)

        self.setLayout(vbox)

    def openDialog(self, opentype):
        if opentype == 'folder':
            filenames = openDir(self)
        elif opentype == 'file':
            filenames = openFiles(self)
        else:
            assert False, "Invalid Error"

        if len(filenames) == 0:
            _ = QMessageBox.warning(self, 'Warning', 'No image files!!', QMessageBox.Ok)
            return


