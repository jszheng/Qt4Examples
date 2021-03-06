class LCDRange < Qt::Widget
  signals 'valueChanged(int)'
  slots 'setValue(int)', 'setRange(int, int)', 'setText(const char*)'
  
  def initialize(s, parent = nil)
    super(parent)
    init()
    setText(s)
  end
  
  def init()
    lcd = Qt::LCDNumber.new(2)
    lcd.setSegmentStyle(Qt::LCDNumber::Filled)

    @slider = Qt::Slider.new(Qt::Horizontal)
    @slider.setRange(0, 99)
    @slider.setValue(0)
    
    @label = Qt::Label.new()
    @label.setAlignment(Qt::AlignHCenter.to_i | Qt::AlignTop.to_i)
    @label.setSizePolicy(Qt::SizePolicy::Preferred, Qt::SizePolicy::Fixed)
    
    connect(@slider, SIGNAL('valueChanged(int)'),
            lcd, SLOT('display(int)'))
    connect(@slider, SIGNAL('valueChanged(int)'),
            self, SIGNAL('valueChanged(int)'))
    
    layout = Qt::VBoxLayout.new()
    layout.addWidget(lcd)
    layout.addWidget(@slider)
    layout.addWidget(@label)
    setLayout(layout)
    
    setFocusProxy(@slider)
  end
  
  def value()
    @slider.value()
  end

  def setValue(value)
    @slider.setValue(value)
  end

  def setRange(minVal, maxVal)
    if minVal < 0 || maxVal > 99 || minVal > maxVal
      qWarning("LCDRange::setRange(#{minVal}, #{maxVal})\n" +
                 "\tRange must be 0..99\n" +
                 "\tand minVal must not be greater than maxVal")
      return
    end

    @slider.setRange(minVal, maxVal)
  end

  def setText(s)
    @label.setText(s)
  end
end
