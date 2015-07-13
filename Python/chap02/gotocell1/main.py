import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from ui_gotocelldialog import *

app = QApplication(sys.argv)

dialog = QDialog()
ui = Ui_GoToCellDialog()
ui.setupUi(dialog)
dialog.show()

app.exec_()