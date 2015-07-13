from PyQt4.QtCore import *
from PyQt4.QtGui import *

from ui_gotocelldialog import *

class GoToCellDialog(QDialog, Ui_GoToCellDialog):
    def __init__(self, parent=None):
        super(GoToCellDialog, self).__init__(parent)
        self.setupUi(self)
        regExp = QRegExp("[A-Za-z][1-9][0-9]{0,2}")
        self.lineEdit.setValidator(QRegExpValidator(regExp))

        self.okButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)
        #self.lineEdit.textChanged.connect(self.on_lineEdit_textChanged)

    # Ui_GoToCellDialog中自动会调用
    #         QtCore.QMetaObject.connectSlotsByName(GoToCellDialog)
    # 将对应命名为【on_成员名_signal名】的slot连接到对应的信号上。
    def on_lineEdit_textChanged(self):
        self.okButton.setEnabled(self.lineEdit.hasAcceptableInput())
