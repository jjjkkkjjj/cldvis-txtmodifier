from PySide2.QtWidgets import *
import sys

from tda.gui import MainWindowController

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = MainWindowController()
    gui.show()
    sys.exit(app.exec_())