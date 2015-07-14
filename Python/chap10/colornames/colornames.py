from PyQt4.QtGui import *
from PyQt4.QtCore import *

class ColorNamesDialog(QDialog):
    def __init__(self, parent=None):
        super(ColorNamesDialog, self).__init__(parent)

        self.sourceModel = QStringListModel(self)
        self.sourceModel.setStringList(QColor.colorNames())

        self.proxyModel = QSortFilterProxyModel(self)
        self.proxyModel.setSourceModel(self.sourceModel)
        self.proxyModel.setFilterKeyColumn(0)

        self.listView = QListView()
        self.listView.setModel(self.proxyModel)
        self.listView.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.filterLabel = QLabel('&Filter:')
        self.filterLineEdit = QLineEdit()
        self.filterLabel.setBuddy(self.filterLineEdit)

        self.syntaxLabel = QLabel('&Pattern syntax:')
        combo = self.syntaxLComboBox = QComboBox()
        combo.addItem('Regular expression', QRegExp.RegExp)
        combo.addItem('Wildcard', QRegExp.Wildcard)
        combo.addItem('Fixed String', QRegExp.FixedString)
        self.syntaxLabel.setBuddy(combo)

        self.filterLineEdit.textChanged.connect(self.reApplyFilter)
        self.syntaxLComboBox.currentIndexChanged.connect(self.reApplyFilter)

        grid = self.mainLayout = QGridLayout()
        grid.addWidget(self.listView, 0, 0, 1, 2)
        grid.addWidget(self.filterLabel,    1, 0)
        grid.addWidget(self.filterLineEdit, 1, 1)
        grid.addWidget(self.syntaxLabel,    2, 0)
        grid.addWidget(self.syntaxLComboBox,2, 1)
        self.setLayout(grid)

        self.setWindowTitle('Color Names')

    def reApplyFilter(self):
        combo = self.syntaxLComboBox
        index = combo.currentIndex()
        syntax = QRegExp.PatternSyntax(combo.itemData(index))
        regexp = QRegExp(self.filterLineEdit.text(),
                         Qt.CaseInsensitive,
                         syntax)
        self.proxyModel.setFilterRegExp(regexp)
