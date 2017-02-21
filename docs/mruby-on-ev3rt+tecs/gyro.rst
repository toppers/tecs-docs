
ジャイロセンサ - `Gyro`
==============

ジャイロセンサに関するAPIです．

インスタンスメソッド一覧
----------------

* :ref:`initialize( port ) <mruby-on-ev3rt-gyro-initialize>`
* :ref:`angle <mruby-on-ev3rt-gyro-angle>`
* :ref:`rate <mruby-on-ev3rt-gyro-rate>`
* :ref:`reset <mruby-on-ev3rt-gyro-reset>`
* :ref:`calibrate ( n=200 ) <mruby-on-ev3rt-gyro-calibrate>`

シンボル
------

* **port**

  センサポートを表わすシンボル

  =======   ==========
  シンボル
  --------------------
  :port_1   ポート 1
  :port_2   ポート 2
  :port_3   ポート 3
  :port_4   ポート 4
  =======   ==========



インスタンスメソッド
----------------

.. _mruby-on-ev3rt-gyro-initialize:

initialize ( port ) -> nil
^^^^^^^^^^^^^^^^^^^^^^^^^^

ジャイロセンサポートを設定する．

**引数**
  `port`  センサポートのシンボル

**戻り値**
  nil

----

.. _mruby-on-ev3rt-gyro-angle:

angle -> Fixnum
^^^^^^^^^^^^^^^^^

ジャイロセンサで角位置を測定する．

**引数**
  なし

**戻り値**
  角位置 (単位は度)

----

.. _mruby-on-ev3rt-gyro-rate:

rate -> Fixnum
^^^^^^^^^^^^^^^^^

ジャイロセンサで角速度を測定する．

**引数**
  なし

**戻り値**
  角位置 （単位は度/秒）

----

.. _mruby-on-ev3rt-gyro-reset:

reset -> nil
^^^^^^^^^^^^^^^^^

ジャイロセンサの角位置をゼロにリセットする．

**引数**
  なし

**戻り値**
  nil

----

.. _mruby-on-ev3rt-gyro-calibrate:

calibrate ( n=200 ) -> Float | Symbol
^^^^^^^^^^^^^^^^^

ジャイロセンサのキャリブレーション．
複数回測定した値の平均値

**引数**
  n 測定回数：デフォルトは200（小数点以下切り捨て）

**戻り値**
  `offset` 測定回数の平均値

  `：E_OBJ` 測定値の最大・最小の値が5以上の場合

----


.. code-block:: ruby
  :caption: gyro_sample.rb
