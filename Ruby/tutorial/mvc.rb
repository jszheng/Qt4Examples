#!/usr/bin/ruby
=begin
**
** mvc.rb
** 15/AUG/2007
** ETD-Software
**  - Daniel Martin Gomez <etd[-at-]nomejortu.com>
**
** Desc:
**   Ruby script that shows how to split Model and View in a GUI application
**  using the Qt libraries.
**   More complex situations may require the use of a Controller component.
**  
**
** Version:
**  v1.0 [15/Aug/2007]: first released
**
=end

require 'Qt4'

#
# Model component, it stores the *data* of our application. It defines _slots_
# that can be used by other components to modify the data and it also emits
# _signals_ when data is modified.
#
# In this simple example the *data* consists only of a _counter_ whose value
# can be increased or decreased.
#
class Model < Qt::Object
  slots 'increase()', 'decrease()'
  signals 'modified()'
  
  attr :counter
  
  def initialize 
    super
    @counter = 0
  end
  
  def increase
    @counter += 1
    emit modified()
  end
  
  def decrease
    @counter -= 1
    emit modified()
  end
end

#
# View component, it defines the elements of the GUI and their disposition.
# When the user interacts with these elements _signals_ are sent to the Model
# component to alter the data.
#
# _Signals_ are also received from the Model when data has been modified in
# order to properly update the GUI elements.
#
class View < Qt::Widget
  slots 'counter_modified()'
  
  def initialize(model)
    super(nil)
    
    # keep a reference to the model
    @model = model
    
    # define widgets and layout
    grid = Qt::GridLayout.new
    @btn1 = Qt::PushButton.new('+1')
    @btn2 = Qt::PushButton.new('-1')
    @lcd = Qt::LCDNumber.new
    grid.addWidget(@btn1)
    grid.addWidget(@btn2)
    grid.addWidget(@lcd)
    self.setLayout(grid)
    
    # connect signals and slots between the Model and the View
    connect @btn1, SIGNAL('clicked()'), @model, SLOT('increase()')
    connect @btn2, SIGNAL('clicked()'), @model, SLOT('decrease()')
    connect @model, SIGNAL('modified()'), self, SLOT('counter_modified()')
  end
  

  def counter_modified
    @lcd.display(@model.counter)
  end
end

if $0 == __FILE__
  app = Qt::Application.new(ARGV)
  view = View.new(Model.new)
  view.show
  app.exec
end
