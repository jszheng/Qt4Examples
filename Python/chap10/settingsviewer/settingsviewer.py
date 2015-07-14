from PyQt4.QtCore import *
from PyQt4.QtGui import *

class SettingsViewer(QDialog):
    def __init__(self, parent=None):
        super(SettingsViewer, self).__init__(parent)
        self.organization = 'Trolltech'
        self.application = 'Designer'

        self.treeWidget = QTreeWidget()
        self.treeWidget.setColumnCount(2)
        self.treeWidget.setHeaderLabels(['Key', 'Value'])
        self.treeWidget.header().setResizeMode(0, QHeaderView.Stretch)
        self.treeWidget.header().setResizeMode(1, QHeaderView.Stretch)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Open |
                                     QDialogButtonBox.Close)
        self.buttonBox.accepted.connect(self.open)
        self.buttonBox.rejected.connect(self.close)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.treeWidget)
        self.mainLayout.addWidget(self.buttonBox)
        self.setLayout(self.mainLayout)

        self.setWindowTitle('Setting Viewer')
        self.readSettings()

    def open(self):
        dlg = QDialog(self)

        orgLabel = QLabel("&Organization:")
        orgLineEdit = QLineEdit(self.organization)
        orgLabel.setBuddy(orgLineEdit)

        appLabel = QLabel('&Application:')
        appLineEdit = QLineEdit(self.application)
        appLabel.setBuddy(appLineEdit)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok |
                                     QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(dlg.accept)
        buttonBox.rejected.connect(dlg.reject)

        layout = QGridLayout()
        layout.addWidget(orgLabel,    0, 0)
        layout.addWidget(orgLineEdit, 0, 1)
        layout.addWidget(appLabel,    1, 0)
        layout.addWidget(appLineEdit, 1, 1)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(layout)
        mainLayout.addWidget(buttonBox)
        dlg.setLayout(mainLayout)

        dlg.setWindowTitle('Choose Settings')

        if dlg.exec_():
            self.organization = orgLineEdit.text()
            self.application  = appLineEdit.text()
            self.readSettings()

    def readSettings(self):
        settings = QSettings(self.organization, self.application)
        self.treeWidget.clear()
        self.addChildSettings(settings, None, '')
        self.treeWidget.sortByColumn(0)
        self.treeWidget.setFocus()
        self.setWindowTitle("Setting Viewer - {} by {}".format(self.application, self.organization))

    def addChildSettings(self, settings: QSettings, parent, group):
        if parent is None:
            parent = self.treeWidget.invisibleRootItem()
        settings.beginGroup(group)
        for key in settings.childKeys():
            item = QTreeWidgetItem(parent)
            item.setText(0, key)
            item.setText(1, str(settings.value(key)))
        for group in settings.childGroups():
            item = QTreeWidgetItem(parent)
            item.setText(0, group)
            self.addChildSettings(settings, item, group)
        settings.endGroup()
