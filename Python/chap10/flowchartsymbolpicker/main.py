import sys
from PyQt4.QtGui import *

from flowchartsymbolpicker import *
import qrc_flowchartsymbolpicker

app = QApplication(sys.argv)

symbolMap = {
    132: 'Data',
    135: 'Decision',
    137: 'Document',
    138: 'Manual Input',
    139: 'Manual Operation',
    141: 'On Page Reference',
    142: 'Predefined Process',
    145: 'Preparation',
    150: 'Printer',
    152: 'Process'
}

picker = FlowChartSymbolPicker(symbolMap)
picker.show()

app.exec_()
