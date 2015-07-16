import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from currencymodel import *

app = QApplication(sys.argv)

currencyMap = dict([
    ("AUD", 1.3259),
    ("CHF", 1.2970),
    ("CZK", 24.510),
    ("DKK", 6.2168),
    ("EUR", 0.8333),
    ("GBP", 0.5661),
    ("HKD", 7.7562),
    ("JPY", 112.92),
    ("NOK", 6.5200),
    ("NZD", 1.4697),
    ("SEK", 7.8180),
    ("SGD", 1.6901),
    ("USD", 1.0000)
])


model = CurrencyModel()
model.setCurrencyMap(currencyMap)

view = QTableView()
view.setModel(model)
view.setAlternatingRowColors(True)
view.setWindowTitle('Currencies')
view.show()

sys.exit(app.exec_())