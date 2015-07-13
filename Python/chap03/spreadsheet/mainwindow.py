from PyQt4 import QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from spreadsheet import *

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        # local variables
        self.findDialog = 0
        self.MaxRecentFiles = 5
        self.recentFileActions = list(range(0, self.MaxRecentFiles))

        self.spreadsheet = Spreadsheet()
        self.setCentralWidget(self.spreadsheet)

        self.createActions()
        self.createMenus()
        self.createContextMenu()
        self.createToolBars()
        self.createStatusBar()

        self.readSettings()

        self.setWindowIcon(QIcon(':/images/icon.png'))
        self.setCurrentFile('')


    def createActions(self):
        # New
        self.newAction = QAction('&New', self)
        self.newAction.setIcon(QIcon(':images/new.png'))
        self.newAction.setShortcut(QKeySequence.New)
        self.newAction.setStatusTip('Create a new spreadsheet file')
        self.newAction.triggered.connect(self.newFile)
        # Open
        self.openAction = QAction(
            '&Open...', self,
            shortcut=QKeySequence.Open,
            statusTip='Open an existing spreadsheet file',
            triggered=self.open,
            icon=QIcon(":/images/open.png")
        )
        self.saveAction = QAction(
            '&Save', self,
            shortcut=QKeySequence.Save,
            statusTip='Save the spreadsheet to disk',
            icon=QIcon(':images/save.png'),
            triggered=self.save
        )
        self.saveAsAction = QAction(
            'Save &As...', self,
            statusTip='Save the spreadsheet under a new name',
            triggered=self.saveAs
        )
        for i in range(0, self.MaxRecentFiles):
            self.recentFileActions[i] = QAction(self)
            self.recentFileActions[i].setVisible(False)
            self.recentFileActions[i].triggered.connect(self.openRecentFile)

        self.exitAction = QAction(
            'E&xit', self,
            shortcut='Ctrl+Q',
            statusTip='Exit the application',
            triggered=self.close
        )

        self.cutAction = QAction(
            'Cu&t', self,
            shortcut=QKeySequence.Cut,
            statusTip='Cut current selection\'s contents to the clipboard',
            triggered=self.cut,
            icon=QIcon(':/images/cut.png')
        )

        self.copyAction = QAction(
            '&Copy', self,
            shortcut=QKeySequence.Copy,
            statusTip='Copy current selection\'s contents to the clipboard',
            triggered=self.copy,
            icon=QIcon(':/images/copy.png')
        )

        self.pasteAction = QAction(
            '&Paste', self,
            shortcut=QKeySequence.Paste,
            statusTip='Paste the clipboard\'s contents into current selection',
            triggered=self.paste,
            icon=QIcon(':/images/paste.png')
        )

        self.deleteAction = QAction(
            '&Delete', self,
            shortcut=QKeySequence.Delete,
            statusTip='Delete current selection\'s contents',
            triggered=self.delete
        )

        self.aboutAction = QAction(
            '&About', self,
            statusTip="Show the appications\'s About box",
            triggered=self.about
        )

        self.aboutQtAction = QAction(
            'About &Qt', self,
            statusTip="Show the Qt library's About box",
            triggered=QtGui.qApp.aboutQt
        )

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu('&File')
        self.fileMenu.addAction(self.newAction)
        self.fileMenu.addAction(self.openAction)
        self.fileMenu.addAction(self.saveAction)
        self.fileMenu.addAction(self.saveAsAction)
        self.separatorAction = self.fileMenu.addSeparator()
        for recent in self.recentFileActions:
            self.fileMenu.addAction(recent)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAction)

        self.editMenu = self.menuBar().addMenu('&Edit')
        self.editMenu.addAction(self.cutAction)
        self.editMenu.addAction(self.copyAction)
        self.editMenu.addAction(self.pasteAction)
        self.editMenu.addAction(self.deleteAction)

        # ... more ...
        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu('&Help')
        self.helpMenu.addAction(self.aboutAction)
        self.helpMenu.addAction(self.aboutQtAction)

    def createContextMenu(self):
        self.spreadsheet.addAction(self.cutAction)
        self.spreadsheet.addAction(self.copyAction)
        self.spreadsheet.addAction(self.pasteAction)
        self.spreadsheet.setContextMenuPolicy(Qt.ActionsContextMenu)

    def createToolBars(self):
        self.fileToolBar = self.addToolBar('&File')
        self.fileToolBar.addAction(self.newAction)
        self.fileToolBar.addAction(self.openAction)
        self.fileToolBar.addAction(self.saveAction)


    def createStatusBar(self):
        self.locationLabel = QLabel(' W999 ')
        self.locationLabel.setAlignment(Qt.AlignHCenter)
        self.locationLabel.setMinimumSize(self.locationLabel.sizeHint())
        self.formulaLabel = QLabel()
        self.formulaLabel.setIndent(3)

        self.statusBar().addWidget(self.locationLabel)
        self.statusBar().addWidget(self.formulaLabel, 1)

    def readSettings(self):
        pass

    def writeSettings(self):
        pass

    def okToContinue(self):
        if self.isWindowModified():
            r = QMessageBox.warning(
                self,
                'Spreadsheet',
                "The document has been modified.\nDo you want to save your changes",
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
                )
            if r == QMessageBox.Yes:
                return self.save()
            elif r == QMessageBox.Cancel:
                return False
        return True

    def loadFile(self, filename):
        pass

    def saveFile(self, filename):
        pass

    def setCurrentFile(self, file):
        pass

    def updateRecentFileActions(self):
        pass

    def strippedName(self, fullFileName):
        pass

    # slots
    def newFile(self):
        pass

    def open(self):
        pass

    def save(self):
        pass

    def saveAs(self):
        pass

    def find_in_file(self):
        pass

    def goToCell(self):
        pass

    def sort(self):
        pass

    def openRecentFile(self):
        pass

    def updateStatusBar(self):
        pass

    def spreadsheetModified(self):
        pass

    def cut(self):
        pass

    def copy(self):
        pass

    def paste(self):
        pass

    def delete(self):
        pass

    def about(self):
        QMessageBox.about(
            self, 'About Spreadsheet',
            self.tr("""<h2>Spreadsheet 1.1</h2>
               <p>Copyright &copy; 2008 Software Inc.
               <p>Spreadsheet is a small application that
               demonstrates QAction, QMainWindow, QMenuBar,
               QStatusBar, QTableWidget, QToolBar, and many other
               Qt classes.""")
        )


