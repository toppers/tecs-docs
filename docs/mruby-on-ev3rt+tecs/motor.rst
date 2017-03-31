
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

シンボル
------

* **port**

  モータポートを表すシンボル

  =======   =====
  シンボル
  ---------------
  :port_a   ポートA
  :port_b   ポートB
  :port_c   ポートC
  :port_d   ポートD
  =======   =====

* **type**

  サポートするモータタイプのシンボル

  =======   ==========
  シンボル
  --------------------
  :large    サーボモータ L
  :medium   サーボモータ M
  =======   ==========



インスタンスメソッド
----------------

.. _mruby-on-ev3rt-motor-initialize:

initialize( port, type=:large ) -> object
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

モータポートを設定する．

モータポートに接続しているモータのタイプを設定する．既に設定した場合も新しいモータタイプを指定できる．

**引数**
  `port`  モータポート番号（シンボル）

  `type`  モータタイプ （シンボル）

**戻り値**
  nil

----

.. _mruby-on-ev3rt-motor-type:

type -> Symbol
^^^^^^^^^^^^^^

モータポートのモータタイプを取得する．

**引数**
  なし

**戻り値**
  `:large`  サーボモータL

  `:medium` サーボモータM

----

.. _mruby-on-ev3rt-motor-power:

power = ( pwm ) -> nil
^^^^^^^^^^^^^^^^^^^^^^

モータのパワーを設定し，モータが回転する．

**引数**
  `pwm` モータのフルパワーのパーセント値．範囲：-100から+100．マイナスの値でモータを逆方向に回転させることができる．範囲外の場合±100が適用される．

**戻り値**
  nil

----

.. _mruby-on-ev3rt-motor-power2:

power -> Fixnum
^^^^^^^^^^^^^^^

モータのパワーを取得する．

**引数**
  なし

**戻り値**
  モータのパワー

----

.. _mruby-on-ev3rt-motor-stop:

stop( brake=true ) -> nil
^^^^^^^^^^^^^^^^^^^^^^^^^

モータを停止する．

**引数**
  `brake` ブレーキモードの指定．`true` （ブレーキモード）, `false` （フロートモード）

**戻り値**
  nil

----

.. _mruby-on-ev3rt-motor-rotate:

rotate( deg, spd, blk=false ) -> nil
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

モータを指定した角度だけ回転させる

**引数**
  `deg` 回転角度，マイナスの値でモータを逆方向に回転させることができる（小数点以下切り捨て）

  `spd` 回転速度，モータポートのフルスピードのパーセント値．範囲：-100から+100（小数点以下切り捨て）．マイナスの場合回転が逆になる．範囲外の場合±100として扱われる．

  `blk` モード指定．`true` (関数は回転が完了してからリターン)，`false` (関数は回転操作を待たずにリターン)

**戻り値**
  nil 正常終了

----

.. _mruby-on-ev3rt-motor-count:

count -> Fixnum
^^^^^^^^^^^^^^^

モータの角位置を取得する．

**引数**
  なし

**戻り値**
  モータの角位置（単位は度），マイナスの値は逆方向に回転されたことを指す．

----

.. _mruby-on-ev3rt-motor-reset-count:

reset_count -> nil
^^^^^^^^^^^^^^^^^^

モータの角位置をゼロにリセットする．

モータの角位置センサの値を設定するだけ，モータの実際のパワーと位置に影響を与えない．

**引数**
  なし

**戻り値**
  nil

----


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
