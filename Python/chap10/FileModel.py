import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

app = QApplication(sys.argv)

splitter = QSplitter()

model = QFileSystemModel()
model.setRootPath(QDir.currentPath())

tree = QTreeView(splitter)
tree.setModel(model)
tree.setRootIndex(model.index(QDir.currentPath()))
treeheader = tree.header()
treeheader.setStretchLastSection(True)
treeheader.setSortIndicator(0, Qt.AscendingOrder)
treeheader.setSortIndicatorShown(True)
treeheader.setClickable(True)

list = QListView(splitter)
list.setModel(model)
list.setRootIndex(model.index(QDir.currentPath()))

splitter.setWindowTitle("Two views on the same file system")
splitter.show()

sys.exit(app.exec_())