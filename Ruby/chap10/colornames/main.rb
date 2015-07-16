require 'Qt'
require './colornames.rb'

app = Qt::Application.new(ARGV)

dlg = ColorNamesDialog.new()
dlg.show()

app.exec