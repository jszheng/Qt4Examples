require 'Qt'

app = Qt::Application.new(ARGV)

label = Qt::Label.new('Hello Qt!')
label.show

app.exec