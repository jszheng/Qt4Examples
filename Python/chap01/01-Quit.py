import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

app = QApplication(sys.argv)

button = QPushButton('Quit')
button.clicked.connect(app.quit)
button.show()

app.exec_()