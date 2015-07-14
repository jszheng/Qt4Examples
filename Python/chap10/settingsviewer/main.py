import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from settingsviewer import  *
app = QApplication(sys.argv)

setting = SettingsViewer()
setting.show()

sys.exit(app.exec_())
