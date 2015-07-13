from PyQt4.QtCore import *
from PyQt4.QtGui import *

from ui_gotocelldialog import *

class GoToCellDialog(QDialog, Ui_GoToCellDialog):
    def __init__(self, parent=None):
        super(GoToCellDialog, self).__init__(parent)
        self.setupUi(self)
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

        regExp = QRegExp("[A-Za-z][1-9][0-9]{0,2}")
        self.lineEdit.setValidator(QRegExpValidator(regExp))

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    # Ui_GoToCellDialog中自动会调用
    #         QtCore.QMetaObject.connectSlotsByName(GoToCellDialog)
    # 将对应命名为【on_成员名_signal名】的slot连接到对应的信号上。
    def on_lineEdit_textChanged(self):
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(self.lineEdit.hasAcceptableInput())
