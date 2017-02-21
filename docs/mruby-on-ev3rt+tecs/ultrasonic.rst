
超音波センサ - `Ultrasonic`
==============

超音波センサに関するAPIです．

インスタンスメソッド一覧
----------------

* :ref:`initialize( port ) <mruby-on-ev3rt-ultrasonic-initialize>`
* :ref:`distance <mruby-on-ev3rt-ultrasonic-distance>`
* :ref:`listen <mruby-on-ev3rt-ultrasonic-listen>`

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

.. _mruby-on-ev3rt-ultrasonic-initialize:

initialize ( port ) -> nil
^^^^^^^^^^^^^^^^^^^^^^^^^^

超音波センサポートを設定する．

**引数**
  `port`  センサポートのシンボル
**戻り値**
  nil

----

.. _mruby-on-ev3rt-ultrasonic-distance:

distance -> Fixnum
^^^^^^^^^^^^^^^^^

超音波センサで距離を測定する．

**引数**
  なし
**戻り値**
  距離 (単位はセンチ）

----

.. _mruby-on-ev3rt-ultrasonic-listen:

listen-> bool
^^^^^^^^^^^^^^^^^

超音波センサで超音波信号を検出する．

**引数**
  なし
**戻り値**
  `true` 超音波信号を検出した
  `false` 超音波信号を検出しなかった

----

.. code-block:: ruby
  :caption: ultrasonic_sample.rb
