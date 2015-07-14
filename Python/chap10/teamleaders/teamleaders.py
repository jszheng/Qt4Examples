from PyQt4.QtGui import *
from PyQt4.QtCore import *

class TeamLeaderDialog(QDialog):
    def __init__(self, leaders, parent=None):
        super(TeamLeaderDialog, self).__init__(parent)
        self.model = QStringListModel(self)
        self.model.setStringList(leaders)

        self.listView = QListView()
        self.listView.setModel(self.model)
        self.listView.setEditTriggers(QAbstractItemView.AnyKeyPressed |
                                      QAbstractItemView.DoubleClicked)

        self.buttonBox = QDialogButtonBox()
        self.insertButton = self.buttonBox.addButton('&Insert',
                                                     QDialogButtonBox.ActionRole)
        self.deleteButton = self.buttonBox.addButton('&Delete',
                                                     QDialogButtonBox.ActionRole)
        self.buttonBox.addButton(QDialogButtonBox.Ok)
        self.buttonBox.addButton(QDialogButtonBox.Cancel)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.insertButton.clicked.connect(self.insert)
        self.deleteButton.clicked.connect(self.delete)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.listView)
        self.mainLayout.addWidget(self.buttonBox)
        self.setLayout(self.mainLayout)

        self.setWindowTitle('Team Leaders')

    def leaders(self):
        return self.model.stringList()

    @pyqtSlot()
    def insert(self):
        row = self.listView.currentIndex().row()
        self.model.insertRow(row)
        index = self.model.index(row)
        self.listView.setCurrentIndex(index)
        self.listView.edit(index)

    @pyqtSlot()
    def delete(self):
        self.model.removeRow(self.listView.currentIndex().row())

