from PyQt4.QtCore import *
from PyQt4.QtGui import *

from ui_sortdialog import *

class SortDialog(QDialog, Ui_SortDialog):
    def __init__(self, parent=None):
        super(SortDialog, self).__init__(parent)

        self.setupUi(self)

        self.secondaryGroupBox.hide()
        self.tertiaryGroupBox.hide()
        self.layout().setSizeConstraint(QLayout.SetFixedSize)

        self.setColumnRange('A', 'Z')

    def setColumnRange(self, first, last):
        self.primaryColumnCombo.clear()
        self.secondaryColumnCombo.clear()
        self.tertiaryColumnCombo.clear()
        self.secondaryColumnCombo.addItem("None")
        self.tertiaryColumnCombo.addItem("None")
        self.primaryColumnCombo.setMinimumSize(self.secondaryColumnCombo.sizeHint())

        for idx in range(ord(first), ord(last)+1):
            ch = chr(idx)
            self.primaryColumnCombo.addItem(ch)
            self.secondaryColumnCombo.addItem(ch)
            self.tertiaryColumnCombo.addItem(ch)
