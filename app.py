from PySide2.QtWidgets import *
import sys

from tda.gui import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = MainWindow()
    gui.show()
    sys.exit(app.exec_())