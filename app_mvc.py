from PySide2.QtWidgets import *
import sys

import os
# to avoid not working in MAC Big sur
os.environ['QT_MAC_WANTS_LAYER'] = '1'

from tda_mvc.main import MainViewController

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = MainViewController()
    gui.show()
    sys.exit(app.exec_())