import sys
from PyQt4.QtGui import *

from coordinatesetter import *

app = QApplication(sys.argv)

coords = [
    (0.0, 0.9),
    (0.2, 11.0),
    (0.4, 15.4),
    (0.6, 12.9),
    (0.8, 8.5),
    (1.0, 7.1),
    (1.2, 4.0),
    (1.4, 13.6),
    (1.6, 22.2),
    (1.8, 22.2)
]

cs = CoordinateSetter(coords)
cs.show()

app.exec_()
