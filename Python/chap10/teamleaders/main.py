import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from teamleaders import  *
app = QApplication(sys.argv)

teamleaders = [
    "Stooge Viller",
    "Littleface",
    "B-B Eyes",
    "Pruneface",
    "Mrs. Pruneface",
    "The Brow",
    "Vitamin Flintheart",
    "Flattop Sr.",
    "Shakey",
    "Breathless Mahoney",
    "Mumbles",
    "Shoulders",
    "Sketch Paree"
]

tl = TeamLeaderDialog(teamleaders)
tl.show()

sys.exit(app.exec_())

