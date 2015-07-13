import sys
from PyQt4.QtGui import *
from sortdialog import SortDialog


app = QApplication(sys.argv)

dialog = SortDialog()
dialog.setColumnRange('C', 'F')
dialog.show()

app.exec_()
