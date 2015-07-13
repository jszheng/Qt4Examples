import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Enter Your Age")

spinbox = QSpinBox()
slider = QSlider(Qt.Horizontal)
spinbox.setRange(0, 130)
slider.setRange(0,130)
spinbox.valueChanged.connect(slider.setValue)
slider.valueChanged.connect(spinbox.setValue)
spinbox.setValue(35)

layout = QHBoxLayout()
layout.addWidget(spinbox)
layout.addWidget(slider)

window.setLayout(layout)
window.show()

app.exec_()