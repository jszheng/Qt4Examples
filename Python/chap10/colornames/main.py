import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from colornames import *

app = QApplication(sys.argv)

cn = ColorNamesDialog()
cn.show()

sys.exit(app.exec_())