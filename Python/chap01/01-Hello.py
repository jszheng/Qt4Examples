import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

app = QApplication(sys.argv)

label = QLabel("Hello Qt!")
label.show()

app.exec_()