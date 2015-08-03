"""
Source Editor based on QScintilla
"""
import sys
import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.Qsci import *

import MdiEditor_resources


class SourceEditor(QsciScintilla):
    sequenceNumber = 1
    ARROW_MARKER_NUM = 8
    FILETYPE_MAPPING = {
        'tex': QsciLexerTeX,
        'css': QsciLexerCSS,
        'java': QsciLexerJava,
        'yaml': QsciLexerYAML,
        'v': QsciLexerVerilog,
        'rb': QsciLexerRuby,
        'py': QsciLexerPython,
        'sv': QsciLexerVerilog,
        'xml': QsciLexerXML,
        'lua': QsciLexerLua,
        'sql': QsciLexerSQL,
        'cpp': QsciLexerCPP,
        'sh': QsciLexerBash,
        'bash': QsciLexerBash,
        'htm': QsciLexerHTML,
        'pl': QsciLexerPerl,
        'js': QsciLexerJavaScript,
        'html': QsciLexerHTML,
        'tcl': QsciLexerTCL,
        'c': QsciLexerCPP,
        'ps': QsciLexerPostScript,
        'vhd': QsciLexerVHDL,
        'cs': QsciLexerCSharp,
    }

    def __init__(self, parent=None):
        super(SourceEditor, self).__init__(parent)

        self.isUntitled = True

        # Set the default font
        #self.font_name = b'Microsoft Yahei Mono'
        #self.font_name = b'YaHei Consolas Hybrid'
        self.font_name = b'Courier'
        self.font = QFont(self.font_name.decode(), 10)
        #self.font.setFixedPitch(True)
        self.setFont(self.font)

        # Margin 0 is used for line numbers
        fontmetrics = QFontMetrics(self.font)
        self.setMarginsFont(self.font)
        self.setMarginWidth(0, fontmetrics.width("00000") + 6)
        self.setMarginLineNumbers(0, True)
        self.setMarginsBackgroundColor(QColor("#cccccc"))

        # Clickable margin 1 for showing markers
        self.setMarginSensitivity(1, True)
        self.connect(
            self,
            SIGNAL('marginClicked(int, int, Qt::KeyboardModifiers)'),
            self.on_margin_clicked
        )
        self.markerDefine(
            QsciScintilla.RightArrow,
            self.ARROW_MARKER_NUM
        )
        self.setMarkerBackgroundColor(
            QColor("#ee1111"),
            self.ARROW_MARKER_NUM
        )
        # Brace matching: enable for a brace immediately before or after
        # the current position
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)

        # Current line visible with special background color
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor("#ffe4e4"))

        self.setMinimumSize(600, 450)

    def on_margin_clicked(self, nmargin, nline, modifiers):
        # Toggle marker for the line the margin was clicked on
        if self.markersAtLine(nline) != 0:
            self.markerDelete(nline, self.ARROW_MARKER_NUM)
        else:
            self.markerAdd(nline, self.ARROW_MARKER_NUM)

    def setSyntaxColor(self, filename):
        # set syntax highlighting based on extension
        file_ext = os.path.splitext(filename)[1][1:]
        if file_ext in self.FILETYPE_MAPPING:
            lexer = self.FILETYPE_MAPPING[file_ext]()
            lexer.setDefaultFont(self.font)
            self.setLexer(lexer)
            self.SendScintilla(QsciScintilla.SCI_STYLESETFONT, 1, self.font_name)

    def newFile(self):
        self.isUntitled = True
        self.curFile = "document%d.txt" % SourceEditor.sequenceNumber
        SourceEditor.sequenceNumber += 1
        self.setWindowTitle(self.curFile + '[*]')
        self.textChanged.connect(self.documentWasModified)

    def loadFile(self, fileName):
        file = QFile(fileName)
        if not file.open(QFile.ReadOnly):
            QMessageBox.warning(
                self,
                "MDI",
                "Cannot read file %s:\n%s." % (fileName, file.errorString())
            )
            return False

        instr = QTextStream(file)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.setText(instr.readAll())
        QApplication.restoreOverrideCursor()
        self.setCurrentFile(fileName)
        self.setSyntaxColor(fileName)
        self.textChanged.connect(self.documentWasModified)
        return True

    def setCurrentFile(self, fileName):
        self.curFile = QFileInfo(fileName).canonicalFilePath()
        self.isUntitled = False
        self.setModified(False)
        self.setWindowModified(False)
        self.setWindowTitle(self.userFriendlyCurrentFile() + "[*]")

    def currentFile(self):
        return self.curFile

    def userFriendlyCurrentFile(self):
        return self.strippedName(self.curFile)

    def strippedName(self, fullFileName):
        return QFileInfo(fullFileName).fileName()

    def documentWasModified(self):
        self.setWindowModified(self.isModified())

    def maybeSave(self):
        if self.isModified():
            ret = QMessageBox.warning(
                self,
                "MDI",
                "'%s' has been modified.\nDo you want to save your "
                "changes?" % self.userFriendlyCurrentFile(),
                QMessageBox.Save | QMessageBox.Discard |
                QMessageBox.Cancel
            )
            if ret == QMessageBox.Save:
                return self.save()
            elif ret == QMessageBox.Cancel:
                return False
        return True

    def saveFile(self, fileName):
        file = QFile(fileName)

        if not file.open(QFile.WriteOnly):
            QMessageBox.warning(
                self,
                "MDI",
                "Cannot write file %s:\n%s." % (fileName, file.errorString())
            )
            return False

        outstr = QTextStream(file)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        outstr << self.text()
        QApplication.restoreOverrideCursor()

        self.setCurrentFile(fileName)
        return True

    def save(self):
        if self.isUntitled:
            return self.saveAs()
        else:
            return self.saveFile(self.curFile)

    def saveAs(self):
        fileName = QFileDialog.getSaveFileName(
            self,
            "Save As",
            self.curFile
        )
        if not fileName:
            return False
        self.setSyntaxColor(fileName)
        return self.saveFile(fileName)

    def closeEvent(self, event):
        if self.maybeSave():
            event.accept()
        else:
            event.ignore()


class MainWindows(QMainWindow):
    def __init__(self):
        super(MainWindows, self).__init__()

        # central is MDI
        self.mdiArea = QMdiArea()
        self.mdiArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setCentralWidget(self.mdiArea)

        self.mdiArea.subWindowActivated.connect(self.updateMenus)
        self.windowMapper = QSignalMapper(self)
        self.windowMapper.mapped[QWidget].connect(self.setActiveSubWindow)

        # create GUI components
        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.updateMenus()

        self.readSettings()

        self.setWindowTitle("Source Editor")

    def closeEvent(self, event):
        self.mdiArea.closeAllSubWindows()
        if self.mdiArea.currentSubWindow():
            event.ignore()
        else:
            self.writeSettings()
            event.accept()

    def createActions(self):
        self.newAct = QAction(
            QIcon(':/images/new.png'),
            "&New",
            self,
            shortcut=QKeySequence.New,
            statusTip="Create a new file",
            triggered=self.newFile)

        self.openAct = QAction(
            QIcon(':/images/open.png'),
            "&Open...",
            self,
            shortcut=QKeySequence.Open,
            statusTip="Open an existing file",
            triggered=self.open)

        self.saveAct = QAction(
            QIcon(':/images/save.png'),
            "&Save",
            self,
            shortcut=QKeySequence.Save,
            statusTip="Save the document to disk",
            triggered=self.save)

        self.saveAsAct = QAction(
            "Save &As...",
            self,
            shortcut=QKeySequence.SaveAs,
            statusTip="Save the document under a new name",
            triggered=self.saveAs)

        self.exitAct = QAction(
            "E&xit",
            self,
            shortcut=QKeySequence.Quit,
            statusTip="Exit the application",
            triggered=qApp.closeAllWindows)

        self.cutAct = QAction(
            QIcon(':/images/cut.png'),
            "Cu&t",
            self,
            shortcut=QKeySequence.Cut,
            statusTip="Cut the current selection's contents to the clipboard",
            triggered=self.cut)

        self.copyAct = QAction(
            QIcon(':/images/copy.png'),
            "&Copy",
            self,
            shortcut=QKeySequence.Copy,
            statusTip="Copy the current selection's contents to the clipboard",
            triggered=self.copy)

        self.pasteAct = QAction(
            QIcon(':/images/paste.png'),
            "&Paste",
            self,
            shortcut=QKeySequence.Paste,
            statusTip="Paste the clipboard's contents into the current selection",
            triggered=self.paste)

        self.closeAct = QAction(
            "Cl&ose",
            self,
            statusTip="Close the active window",
            triggered=self.mdiArea.closeActiveSubWindow)

        self.closeAllAct = QAction(
            "Close &All",
            self,
            statusTip="Close all the windows",
            triggered=self.mdiArea.closeAllSubWindows)

        self.tileAct = QAction(
            "&Tile",
            self,
            statusTip="Tile the windows",
            triggered=self.mdiArea.tileSubWindows)

        self.cascadeAct = QAction(
            "&Cascade",
            self,
            statusTip="Cascade the windows",
            triggered=self.mdiArea.cascadeSubWindows)

        self.nextAct = QAction(
            "Ne&xt",
            self,
            shortcut=QKeySequence.NextChild,
            statusTip="Move the focus to the next window",
            triggered=self.mdiArea.activateNextSubWindow)

        self.previousAct = QAction(
            "Pre&vious",
            self,
            shortcut=QKeySequence.PreviousChild,
            statusTip="Move the focus to the previous window",
            triggered=self.mdiArea.activatePreviousSubWindow)

        self.separatorAct = QAction(self)
        self.separatorAct.setSeparator(True)

        self.aboutAct = QAction(
            "&About",
            self,
            statusTip="Show the application's About box",
            triggered=self.about)

        self.aboutQtAct = QAction(
            "About &Qt",
            self,
            statusTip="Show the Qt library's About box",
            triggered=qApp.aboutQt)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.newAct)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addAction(self.saveAsAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.editMenu = self.menuBar().addMenu("&Edit")
        self.editMenu.addAction(self.cutAct)
        self.editMenu.addAction(self.copyAct)
        self.editMenu.addAction(self.pasteAct)

        self.windowMenu = self.menuBar().addMenu("&Window")
        self.updateWindowMenu()
        self.windowMenu.aboutToShow.connect(self.updateWindowMenu)

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

    def createToolBars(self):
        self.fileToolBar = self.addToolBar("File")
        self.fileToolBar.addAction(self.newAct)
        self.fileToolBar.addAction(self.openAct)
        self.fileToolBar.addAction(self.saveAct)

        self.editToolBar = self.addToolBar("Edit")
        self.editToolBar.addAction(self.cutAct)
        self.editToolBar.addAction(self.copyAct)
        self.editToolBar.addAction(self.pasteAct)

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def readSettings(self):
        settings = QSettings('JSZHENG', 'SourceEditor')
        pos = settings.value('pos', QPoint(200, 200))
        size = settings.value('size', QSize(400, 400))
        self.move(pos)
        self.resize(size)

    def writeSettings(self):
        settings = QSettings('JSZHENG', 'SourceEditor')
        settings.setValue('pos', self.pos())
        settings.setValue('size', self.size())

    def activeMdiChild(self):
        activeSubWindow = self.mdiArea.activeSubWindow()
        if activeSubWindow:
            return activeSubWindow.widget()
        return None

    def findMdiChild(self, fileName):
        canonicalFilePath = QFileInfo(fileName).canonicalFilePath()
        for window in self.mdiArea.subWindowList():
            if window.widget().currentFile() == canonicalFilePath:
                return window
        return None

    def setActiveSubWindow(self, window):
        if window:
            self.mdiArea.setActiveSubWindow(window)

    def updateMenus(self):
        hasMdiChild = (self.activeMdiChild() is not None)
        self.saveAct.setEnabled(hasMdiChild)
        self.saveAsAct.setEnabled(hasMdiChild)
        self.pasteAct.setEnabled(hasMdiChild)
        self.closeAct.setEnabled(hasMdiChild)
        self.closeAllAct.setEnabled(hasMdiChild)
        self.tileAct.setEnabled(hasMdiChild)
        self.cascadeAct.setEnabled(hasMdiChild)
        self.nextAct.setEnabled(hasMdiChild)
        self.previousAct.setEnabled(hasMdiChild)
        self.separatorAct.setVisible(hasMdiChild)

        hasSelection = (self.activeMdiChild() is not None and
                        self.activeMdiChild().hasSelectedText())
        self.cutAct.setEnabled(hasSelection)
        self.copyAct.setEnabled(hasSelection)

    def updateWindowMenu(self):
        self.windowMenu.clear()
        self.windowMenu.addAction(self.closeAct)
        self.windowMenu.addAction(self.closeAllAct)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.tileAct)
        self.windowMenu.addAction(self.cascadeAct)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.nextAct)
        self.windowMenu.addAction(self.previousAct)
        self.windowMenu.addAction(self.separatorAct)

        windows = self.mdiArea.subWindowList()
        self.separatorAct.setVisible(len(windows) != 0)

        for i, window in enumerate(windows):
            child = window.widget()

            text = "%d %s" % (i + 1, child.userFriendlyCurrentFile())
            if i < 9:
                text = '&' + text

            action = self.windowMenu.addAction(text)
            action.setCheckable(True)
            action.setChecked(child is self.activeMdiChild())
            action.triggered.connect(self.windowMapper.map)
            self.windowMapper.setMapping(action, window)

    def newFile(self):
        child = self.createMdiChild()
        child.newFile()
        child.show()

    def open(self):
        fileName = QFileDialog.getOpenFileName(self)
        if fileName:
            existing = self.findMdiChild(fileName)
            if existing:
                self.mdiArea.setActiveSubWindow(existing)
                return

            child = self.createMdiChild()
            if child.loadFile(fileName):
                self.statusBar().showMessage("File loaded", 2000)
                child.show()
            else:
                child.close()

    def save(self):
        if self.activeMdiChild() and self.activeMdiChild().save():
            self.statusBar().showMessage("File saved", 2000)

    def saveAs(self):
        if self.activeMdiChild() and self.activeMdiChild().saveAs():
            self.statusBar().showMessage("File saved", 2000)

    def cut(self):
        if self.activeMdiChild():
            self.activeMdiChild().cut()

    def copy(self):
        if self.activeMdiChild():
            self.activeMdiChild().copy()

    def paste(self):
        if self.activeMdiChild():
            self.activeMdiChild().paste()

    def about(self):
        QMessageBox.about(
            self,
            "About Source Code Editor",
            "The <b>Source Code Editor</b> is a collection of in-house tool for designers"
            "It is written with PyQt and could be easily extended with new features")

    def createMdiChild(self):
        child = SourceEditor()
        self.mdiArea.addSubWindow(child)

        child.copyAvailable.connect(self.cutAct.setEnabled)
        child.copyAvailable.connect(self.copyAct.setEnabled)

        return child

    def findMdiChild(self, fileName):
        canonicalFilePath = QFileInfo(fileName).canonicalFilePath()

        for window in self.mdiArea.subWindowList():
            if window.widget().currentFile() == canonicalFilePath:
                return window
        return None


if __name__ == '__main__':
    app = QApplication(sys.argv)

    mw = MainWindows()
    mw.show()

    sys.exit(app.exec_())