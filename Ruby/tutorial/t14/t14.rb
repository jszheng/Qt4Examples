#!/usr/bin/env ruby
$:.unshift File.dirname($0)

require 'Qt4'
require 'gamebrd.rb'

app = Qt::Application.new(ARGV)

gb = GameBoard.new()
#gb.setGeometry(100, 100, 500, 355)
gb.resize(500, 355)

gb.show()
app.exec()
