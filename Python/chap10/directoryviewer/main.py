import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from directoryviewer import *

app = QApplication(sys.argv)

dv = DirectoryViewer()
dv.show()

sys.exit(app.exec_())