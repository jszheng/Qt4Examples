#!/usr/bin/env ruby
$:.unshift File.dirname($0)

require 'Qt4'
require 'lcdrange.rb'
require 'cannon.rb'

class MyWidget < Qt::Widget
  def initialize(parent = nil)
    super()
    quit = Qt::PushButton.new(tr('Quit'))
    quit.setFont(Qt::Font.new('Times', 18, Qt::Font::Bold))
    
    connect(quit, SIGNAL('clicked()'), $qApp, SLOT('quit()'))
    
    angle = LCDRange.new()
    angle.setRange(5, 70)

    cannonField = CannonField.new()

    connect(angle, SIGNAL('valueChanged(int)'),
            cannonField, SLOT('setAngle(int)'))
    connect(cannonField, SIGNAL('angleChanged(int)'),
            angle, SLOT('setValue(int)'))

    gridLayout = Qt::GridLayout.new()
    gridLayout.addWidget(quit, 0, 0)
    gridLayout.addWidget(angle, 1, 0)
    gridLayout.addWidget(cannonField, 1, 1, 2, 1)
    gridLayout.setColumnStretch(1, 10)
    setLayout(gridLayout)

    angle.setValue(60)
    angle.setFocus()
  end
end    

app = Qt::Application.new(ARGV)

widget = MyWidget.new()
#widget.setGeometry(100, 100, 500, 355)
widget.resize(500, 355)

widget.show()
app.exec()
