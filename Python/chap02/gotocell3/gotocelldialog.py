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

    # Ui_GoToCellDialog���Զ������
    #         QtCore.QMetaObject.connectSlotsByName(GoToCellDialog)
    # ����Ӧ����Ϊ��on_��Ա��_signal������slot���ӵ���Ӧ���ź��ϡ�
    def on_lineEdit_textChanged(self):
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(self.lineEdit.hasAcceptableInput())
