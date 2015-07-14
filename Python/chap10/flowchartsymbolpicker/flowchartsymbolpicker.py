from PyQt4.QtCore import *
from PyQt4.QtGui import *

class FlowChartSymbolPicker(QDialog):
    def __init__(self, symbolMap, parent=None):
        super(FlowChartSymbolPicker, self).__init__(parent)
        self.id = -1
        self.listWidget = QListWidget()
        self.listWidget.setIconSize(QSize(60, 60))

        for (key, value) in symbolMap.items():
            item = QListWidgetItem(value, self.listWidget)
            item.setIcon(self.iconForSymbol(value))
            item.setData(Qt.UserRole, key)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.listWidget)
        mainLayout.addWidget(self.buttonBox)
        self.setLayout(mainLayout)

        self.setWindowTitle('Flowchart Symbol Picker')

    def selectId(self):
        return self.id

    def done(self, result):
        self.id = -1
        if result == QDialog.Accepted:
            item = self.listWidget.currentItem()
            print(item.text())
            if item:
                self.id = item.data(Qt.UserRole)
                print(self.id)
        super(FlowChartSymbolPicker, self).done(result)

    def iconForSymbol(self, symbolName:str):
        filename = ':/images/' + symbolName.lower()
        filename = filename.replace(' ', '-')
        return QIcon(filename)
