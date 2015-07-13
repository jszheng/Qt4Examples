require 'Qt'

app = Qt::Application.new(ARGV)

button = Qt::PushButton.new('Quit')
Qt::Object.connect(button, SIGNAL('clicked()'),
                   app,    SLOT('quit()'))
button.show

app.exec