include Math

class CannonField < Qt::Widget
  signals 'hit()', 'missed()', 'angleChanged(int)', 'forceChanged(int)',
  'canShoot(bool)'

  slots   'setAngle(int)', 'setForce(int)', 'shoot()', 'moveShot()', 
  'newTarget()', 'setGameOver()', 'restartGame()'

  def initialize(parent = nil)
    super()

    @currentAngle = 45
    @currentForce = 0
    @timerCount = 0

    @autoShootTimer = Qt::Timer.new(self)
    connect(@autoShootTimer, SIGNAL('timeout()'),
            self, SLOT('moveShot()'));

    @shootAngle = 0
    @shootForce = 0
    @target = Qt::Point.new(0, 0)
    @gameEnded = false
    @barrelPressed = false

    setPalette( Qt::Palette.new(Qt::Color.new(250, 250, 200)))
    setAutoFillBackground(true)
    newTarget()
    @barrelRect = Qt::Rect.new(30, -5, 20, 10)
  end

  def angle() 
    return @currentAngle 
  end

  def force() 
    return @currentForce 
  end

  def gameOver() 
    return @gameEnded 
  end

  def setAngle(angle)
    if angle < 5
      angle = 5
    elsif angle > 70
      angle = 70
    end

    if @currentAngle == angle
      return
    end

    @currentAngle = angle
    update(cannonRect())
    emit angleChanged(@currentAngle)
  end

  def setForce(force)
    if force < 0
      force = 0
    end

    if @currentForce == force
      return
    end

    @currentForce = force
    emit forceChanged(@currentForce)
  end
  
  def shoot()
    if isShooting()
      return
    end

    @timerCount = 0
    @shootAngle = @currentAngle
    @shootForce = @currentForce
    @autoShootTimer.start(5)
    emit canShoot(false)
  end

  @@first_time = true
  
  def newTarget()
    if @@first_time
      @@first_time = false
      midnight = Qt::Time.new(0, 0, 0)
      srand(midnight.secsTo(Qt::Time.currentTime()))
    end

    @target = Qt::Point.new(200 + rand(190), 10  + rand(255))
    update()
  end
  
  def setGameOver()
    if @gameEnded
      return
    end

    if isShooting()
      @autoShootTimer.stop()
    end

    @gameEnded = true
    update()
  end

  def restartGame()
    if isShooting()
      @autoShootTimer.stop()
    end

    @gameEnded = false

    update()
    emit canShoot( true )
  end
  
  def moveShot()
    region = Qt::Region.new(shotRect())
    @timerCount += 1

    shotR = shotRect()

    if shotR.intersects(targetRect()) 
      @autoShootTimer.stop()
      emit hit()
      emit canShoot(true)
    elsif shotR.x() > width() || shotR.y() > height() || shotR.intersects(barrierRect())
      @autoShootTimer.stop()
      emit missed()
      emit canShoot(true)
    else
      region = region.unite(Qt::Region.new(shotR))
    end
    
    update(region)
  end

  def mousePressEvent(event)
    unless event.button() == Qt::LeftButton
      return
    end

    if barrelHit(event.pos())
      @barrelPressed = true
    end
  end

  def mouseMoveEvent(event)
    unless @barrelPressed
      return
    end

    pos = event.pos();

    if pos.x() <= 0
      pos.setX(1)
    end

    if pos.y() >= height()
      pos.setY(height() - 1)
    end

    rad = atan2((rect().bottom() - pos.y()), pos.x())
    setAngle((rad * 180 / 3.14159265).round())
  end

  def mouseReleaseEvent(event)
    if event.button() == Qt::LeftButton
      @barrelPressed = false
    end
  end

  def paintEvent(event)
    painter = Qt::Painter.new(self)

    if @gameEnded
      painter.setPen(Qt::black)
      painter.setFont(Qt::Font.new( "Courier", 48, Qt::Font::Bold))
      painter.drawText(rect(), Qt::AlignCenter, tr("Game Over"))
    end

    paintCannon(painter)
    paintBarrier(painter)

    if isShooting()
      paintShot(painter)
    end        

    unless @gameEnded
      paintTarget(painter)
    end

    painter.end()
  end

  def paintShot(painter)
    painter.setPen(Qt::NoPen)
    painter.setBrush(Qt::Brush.new(Qt::black))
    painter.drawRect(shotRect())
  end
  
  def paintTarget(painter)
    painter.setBrush(Qt::Brush.new(Qt::red))
    painter.setPen(Qt::Pen.new(Qt::Color.new(Qt::black)))
    painter.drawRect(targetRect())
  end
  
  def paintBarrier( painter )
    painter.setBrush(Qt::Brush.new(Qt::yellow))
    painter.setPen(Qt::Color.new(Qt::black))
    painter.drawRect(barrierRect())
  end
  
  def paintCannon(painter)                
    painter.setPen(Qt::NoPen)
    painter.setBrush(Qt::Brush.new(Qt::blue))

    painter.save()
    painter.translate(0, height())
    painter.drawPie(Qt::Rect.new(-35, -35, 70, 70), 0, 90 * 16)
    painter.rotate(-@currentAngle)
    painter.drawRect(@barrelRect)
    painter.restore()
  end

  def cannonRect()
    result = Qt::Rect.new(0, 0, 50, 50)
    result.moveBottomLeft(rect().bottomLeft())
    return result
  end
  
  def shotRect()
    gravity = 4.0

    time = @timerCount / 20.0
    velocity = @shootForce
    radians = @shootAngle * 3.14159265 / 180.0

    velx = velocity * cos(radians)
    vely = velocity * sin(radians)
    x0 = (@barrelRect.right() + 5.0) * cos(radians)
    y0 = (@barrelRect.right() + 5.0) * sin(radians)
    x = x0 + velx * time
    y = y0 + vely * time - 0.5 * gravity * time * time

    result = Qt::Rect.new(0, 0, 6, 6)
    result.moveCenter(Qt::Point.new(x.round, height() - 1 - y.round))
    return result
  end

  def targetRect()
    result = Qt::Rect.new(0, 0, 20, 10)
    result.moveCenter(Qt::Point.new(@target.x(), height() - 1 - @target.y()))
    return result
  end
  
  def barrierRect()
    return Qt::Rect.new(145, height() - 100, 15, 99)
  end

  def barrelHit(pos)
    matrix = Qt::Matrix.new()
    matrix.translate(0, height())
    matrix.rotate(-@currentAngle)
    matrix = matrix.inverted()
    return @barrelRect.contains(matrix.map(pos))
  end

  def isShooting()
    return @autoShootTimer.isActive()
  end
end
