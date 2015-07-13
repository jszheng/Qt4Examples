require  'Qt'

app = Qt::Application.new(ARGV)

window = Qt::Widget.new
window.setWindowTitle("Enter Your Age")

spinbox = Qt::SpinBox.new
slider  = Qt::Slider.new(Qt::Horizontal)
spinbox.setRange(0, 130)
spinbox.setValue(35)
slider.setRange(0, 130)
Qt::Object.connect(spinbox, SIGNAL('valueChanged(int)'),
                   slider, SLOT('setValue(int)') )
Qt::Object.connect(slider, SIGNAL('valueChanged(int)'),
                   spinbox, SLOT('setValue(int)'))

layout = Qt::HBoxLayout.new
layout.addWidget(spinbox)
layout.addWidget(slider)

window.setLayout(layout)
window.show

app.exec