
モータ - `Motor`
==============

モータを制御するためのAPIです．

インスタンスメソッド一覧
----------------

* :ref:`initialize( port, type=:large ) <mruby-on-ev3rt-motor-initialize>`
* :ref:`type <mruby-on-ev3rt-motor-type>`
* :ref:`power = ( pwm ) <mruby-on-ev3rt-motor-power>`
* :ref:`power <mruby-on-ev3rt-motor-power2>`
* :ref:`stop( brake ) <mruby-on-ev3rt-motor-stop>`
* :ref:`rotate( deg, spd, blk ) <mruby-on-ev3rt-motor-rotate>`
* :ref:`count <mruby-on-ev3rt-motor-count>`
* :ref:`reset_count <mruby-on-ev3rt-motor-reset-count>`

.. _mruby-on-ev3rt-motor-initialize:

initialize( port, type=:large ) -> nil
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

モータポートを設定します．

.. _mruby-on-ev3rt-motor-type:

type -> Symbol
^^^^^^^^^^^^^^

モータポートのタイプの値を返します．

.. _mruby-on-ev3rt-motor-power:

power = ( pwm ) -> nil
^^^^^^^^^^^^^^^^^^^^^^

モータのパワーを設定し，モータを回転させます．

.. _mruby-on-ev3rt-motor-power2:

power -> Fixnum
^^^^^^^^^^^^^^^

モータのパワーの値を返します．

.. _mruby-on-ev3rt-motor-stop:

stop( brake=true ) -> nil
^^^^^^^^^^^^^^^^^^^^^^^^^

モータを停止させます．

.. _mruby-on-ev3rt-motor-rotate:

rotate( deg, spd, blk=false ) -> nil
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

モータを指定した角度だけ回転させます．

.. _mruby-on-ev3rt-motor-count:

count -> Fixnum
^^^^^^^^^^^^^^^

モータの各位置の値を返します．

.. _mruby-on-ev3rt-motor-reset-count:

reset_count -> nil
^^^^^^^^^^^^^^^^^^

モータの各位置をゼロにリセットします．



.. code-block:: ruby
  :caption: motor_sample.rb

  include EV3RT_TECS
  begin
    LCD.font=:medium
    LCD.draw("motor sample", 0, 0)
    # Sensors and Actuators
    left_port= :port_a
    right_port= :port_b
    ultrasonic_port= :port_3
    LCD.draw("left motor:#{left_port} ", 0, 2)
    LCD.draw("right motor:#{right_port} ", 0, 3)
    LCD.draw("ultrasonic :#{ultrasonic_port}", 0, 4)
    $left_motor= Motor.new(left_port)
    $right_motor= Motor.new(right_port)
    $ultrasonic_sensor= UltrasonicSensor.new(ultrasonic_port)include EV3RT_TECS
    loop{
      distance= $ultrasonic_sensor.distance
      LCD.draw("distance = #{distance} ", 0, 6)
      if distance < 15 then
        $left_motor.stop
        $right_motor.stop
      else
        $left_motor.power=30
        $right_motor.power=30
      end
    }
  rescue=> e
    LCD.error_putse
  end
