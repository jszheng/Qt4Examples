import sys
from PyQt4.QtGui import *
from gotocelldialog import GoToCellDialog


app = QApplication(sys.argv)

dialog = GoToCellDialog()
dialog.show()

app.exec_()
