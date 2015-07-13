from PyQt4.QtCore import *
from PyQt4.QtGui import *

from cell import *

class Spreadsheet(QTableWidget):
    # signal definition
    modified = pyqtSignal()

    def __init__(self, parent=None):
        super(Spreadsheet, self).__init__(parent)
        self.autoRecalc = True

        self.setItemPrototype(Cell())
        self.setSelectionMode(self.ContiguousSelection)

        self.MagicNumber = 0x7F51C883
        self.RowCount    = 999
        self.ColumnCount = 26

        self.itemChanged.connect(self.somethingChanged)
        self.clear()

    def clear(self):
        self.setRowCount(0)
        self.setColumnCount(0)
        self.setRowCount(self.RowCount)
        self.setColumnCount(self.ColumnCount)
        for col in range(0, self.ColumnCount):
            item = QTableWidgetItem()
            item.setText(chr(ord('A')+col))
            self.setHorizontalHeaderItem(col, item)

        self.setCurrentCell(0, 0)

    def autoRecalculate(self):
        return self.autoRecalc

    def currentFormula(self):
        pass

    def readFile(self, filename):
        pass

    def writeFile(self, filename):
        pass

    def sort(self):
        pass

    def selectedRange(self):
        ranges = self.selectedRanges()
        if ranges.isEmpty():
            return QTableWidgetSelectionRange()
        return ranges[0]

    def currentLocation(self):
        return chr(ord('A')+self.currentColumn()) + str(self.currentRow()+1)

    # slots
    def somethingChanged(self):
        if self.autoRecalc:
            self.recalculate()
        self.modified.emit()

    def recalculate(self):
        pass

    def cut(self):
        pass

    def copy(self):
        pass

    def paste(self):
        pass

    def delete(self):
        pass

    def selectCurrentRow(self):
        pass

    def selectCurrentColumn(self):
        pass

    def setAutoRecalculate(self, recalc):
        pass

    def findNext(self, text, case_sensitive):
        pass

    def findPrevious(self, text, case_sensitive):
        pass

    # private methods
    def cell(self, row, column):
        pass

    def text(self, row, column):
        pass

    def formula(self, row, column):
        pass

    def setFormula(self, row, colum, formula):
        pass


class SpreadsheetCompare:
    def __init__(self):
        self.KeyCount = 3
        self.keys = []
        self.ascending = []

    def __call__(self, *args, **kwargs):
        pass
