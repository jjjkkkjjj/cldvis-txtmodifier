from PySide2.QtWidgets import *
import sys

import os, argparse
# to avoid not working in MAC Big sur
os.environ['QT_MAC_WANTS_LAYER'] = '1'

from tda_mvc.main import MainViewController

parser = argparse.ArgumentParser(description='Run the tda application.')
parser.add_argument('-d', '--debug', default=False, action='store_true',
                    help='Whether to run as debug mode or not, default is False.')

parser.add_argument('-s', '--save-debug', default=False, action='store_true',
                    help='Whether to save files for debug, default is False.'
                         'This option is valid in non-debug mode only.')

args = parser.parse_args()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainViewController.debug = args.debug
    MainViewController.saveForDebug = (not args.debug) and args.save_debug
    gui = MainViewController()
    gui.show()
    sys.exit(app.exec_())