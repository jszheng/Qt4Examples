from PyQt4.QtGui import *
from PyQt4.QtCore import *
import os

class DirectoryViewer(QDialog):
    def __init__(self, parent=None):
        super(DirectoryViewer, self).__init__(parent)
        self.model = QDirModel()
        self.model.setReadOnly(False)
        self.model.setSorting(QDir.DirsFirst |
                              QDir.IgnoreCase |
                              QDir.Name)

        self.treeview = QTreeView()
        self.treeview.setModel(self.model)
        header = self.treeview.header()
        header.setStretchLastSection(True)
        header.setSortIndicator(0, Qt.AscendingOrder)
        header.setSortIndicatorShown(True)
        header.setClickable(True)

        index = self.model.index(QDir.currentPath())
        self.treeview.expand(index)
        self.treeview.scrollTo(index)
        self.treeview.resizeColumnToContents(0)

        self.buttonBox = QDialogButtonBox(Qt.Horizontal)
        self.mkdirButton = self.buttonBox.addButton('&Create Directory...',
                                                    QDialogButtonBox.ActionRole)
        self.removeButton = self.buttonBox.addButton('&Remove',
                                                      QDialogButtonBox.ActionRole)
        self.buttonBox.addButton(QDialogButtonBox.Ok)
        self.buttonBox.addButton(QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.mkdirButton.clicked.connect(self.createDirectory)
        self.removeButton.clicked.connect(self.remove)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.treeview)
        self.mainLayout.addWidget(self.buttonBox)
        self.setLayout(self.mainLayout)

        self.setWindowTitle('Dirctory Viewer')

    def createDirectory(self):
        index = self.treeview.currentIndex()
        if not index.isValid():
            return

        # Missing, if index point to a file, should fix the index to its parent
        if not self.model.fileInfo(index).isDir():
            index = self.model.parent(index)
        dirName, ok = QInputDialog.getText(self,
                                       'Create Directory',
                                       'Directory Name')
        if ok:
            if not self.model.mkdir(index, dirName).isValid():
                QMessageBox.information(self,
                                        'Create Directory',
                                        'Failed to create the directory!')

    def remove(self):
        index = self.treeview.currentIndex()
        if not index.isValid():
            return
        ok = False
        if self.model.fileInfo(index).isDir():
            ok = self.model.rmdir(index)
        else:
            ok = self.model.remove(index)
        if not ok:
            QMessageBox.information(self,
                                    'Remove',
                                    "Failed to remove {}".format(self.model.fileName((index))))