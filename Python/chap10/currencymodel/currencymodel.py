from PyQt4.QtGui import *
from PyQt4.QtCore import *

class CurrencyModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super(CurrencyModel, self).__init__(parent)
        self.currencyMap = dict()

    def setCurrencyMap(self, map):
        self.currencyMap = map
        self.reset()

    def rowCount(self, parent:QModelIndex=None, *args, **kwargs):
        return len(self.currencyMap)

    def columnCount(self, parent:QModelIndex=None, *args, **kwargs):
        return len(self.currencyMap)

    def data(self, index:QModelIndex, role=None):
        if not index.isValid():
            return
        if role == Qt.TextAlignmentRole:
            return int(Qt.AlignRight | Qt.AlignVCenter)
        elif role == Qt.DisplayRole:
            rowCurrency = self.currencyAt(index.row())
            columnCurrency = self.currencyAt(index.column())
            if self.currencyMap[rowCurrency] == 0.0:
                return '####'
            amount = self.currencyMap[columnCurrency] / self.currencyMap[rowCurrency]
            return "%.4f" % amount
        else:
            return

    def headerData(self, section, orientation, role=None):
        if role == Qt.DisplayRole:
            hdr = self.currencyAt(section)
            return hdr
        else:
            super(CurrencyModel, self).headerData(section, orientation, role)

    def currencyAt(self, offset):
        keys = list(self.currencyMap.keys())
        return keys[offset]
