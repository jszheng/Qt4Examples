"""
Diaglog class
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *


class FindDialog(QDialog):
    # define signals
    findNext = pyqtSignal(str, int)
    findPrevious = pyqtSignal(str, int)

    def __init__(self, parent=None):
        super(FindDialog, self).__init__(parent)
        # init members
        self.label = QLabel("Find &what")
        self.lineEdit = QLineEdit()
        self.label.setBuddy(self.lineEdit)

        self.caseCheckBox = QCheckBox("Match &Case")
        self.backwardCheckBox = QCheckBox("Search &backward")

        self.findButton = QPushButton("&Find")
        self.findButton.setDefault(True)
        self.findButton.setEnabled(False)

        self.closeButton = QPushButton("Close")

        # connect signals/slots
        self.lineEdit.textChanged.connect(self.enableFindButton)
        self.findButton.clicked.connect(self.findClicked)
        self.closeButton.clicked.connect(self.close)

        # layout
        self.topLeftLayout = QHBoxLayout()
        self.topLeftLayout.addWidget(self.label)
        self.topLeftLayout.addWidget(self.lineEdit)

        self.leftLayout = QVBoxLayout()
        self.leftLayout.addLayout(self.topLeftLayout)
        self.leftLayout.addWidget(self.caseCheckBox)
        self.leftLayout.addWidget(self.backwardCheckBox)

        self.rightLayout = QVBoxLayout()
        self.rightLayout.addWidget(self.findButton)
        self.rightLayout.addWidget(self.closeButton)

        self.mainLayout = QHBoxLayout()
        self.mainLayout.addLayout(self.leftLayout)
        self.mainLayout.addLayout(self.rightLayout)

        self.setLayout(self.mainLayout)

        self.setWindowTitle("Find")
        self.setFixedHeight(self.sizeHint().height())

    @pyqtSlot()
    def findClicked(self):
        text = self.lineEdit.text()
        cs = Qt.CaseSensitive if self.caseCheckBox.isChecked() else Qt.CaseInsensitive
        if self.backwardCheckBox.isChecked():
            self.findPrevious.emit(text, cs)
        else:
            self.findNext.emit(text, cs)

    @pyqtSlot(str)
    def enableFindButton(self, text):
        self.findButton.setEnabled(text!='')


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)

    dlg = FindDialog()
    dlg.show()

    app.exec_()