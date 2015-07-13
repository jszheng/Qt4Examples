import sys
from PyQt4.QtGui import *

from mainwindow import *
import qrc_spreadsheet

app = QApplication(sys.argv)

mw = MainWindow()
mw.show()

app.exec_()
