from PyQt4.QtCore import *
from PyQt4.QtGui import *

class CoordinateSetter(QDialog):
    def __init__(self, coords, parent=None):
        super(CoordinateSetter, self).__init__(parent)

        self.coordinates = coords
        self.tableWidget = QTableWidget(0, 2)
        self.tableWidget.setHorizontalHeaderLabels(['X', 'Y'])

        row = 0
        for (x, y) in self.coordinates:
            self.addRow()
            self.tableWidget.item(row, 0).setText(str(x))
            self.tableWidget.item(row, 1).setText(str(y))
            row += 1

        self.buttonBox = QDialogButtonBox(Qt.Horizontal)
        self.buttonBox.addButton(QDialogButtonBox.Ok)
        self.buttonBox.addButton(QDialogButtonBox.Cancel)
        self.addRowButton = self.buttonBox.addButton('&Add Row', QDialogButtonBox.ActionRole)

        self.addRowButton.clicked.connect(self.addRow)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.tableWidget)
        self.mainLayout.addWidget(self.buttonBox)
        self.setLayout(self.mainLayout)

        self.setWindowTitle('Coordinate Setter')

    def addRow(self):
        row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row)
        item0 = QTableWidgetItem()
        item0.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.tableWidget.setItem(row, 0, item0)
        self.tableWidget.setCurrentItem(item0)
        item0 = QTableWidgetItem()
        item0.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.tableWidget.setItem(row, 1, item0)

    def done(self, result):
        if result == QDialog.Accepted:
            self.coordinates = []
            for row in range(0, self.tableWidget.rowCount()):
                x = float(self.tableWidget.item(row, 0).text())
                y = float(self.tableWidget.item(row, 1).text())
                self.coordinates.append((x, y))
        super(CoordinateSetter, self).done(result)
