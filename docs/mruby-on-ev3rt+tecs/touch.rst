
タッチセンサ - `Touch`
==============

タッチセンサに関するAPIです．

インスタンスメソッド一覧
----------------

* :ref:`initialize( port ) <mruby-on-ev3rt-touch-initialize>`
* :ref:`pressed? <mruby-on-ev3rt-touch-pressed>`

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

.. _mruby-on-ev3rt-touch-initialize:

initialize ( port ) -> nil
^^^^^^^^^^^^^^^^^^^^^^^^^^

タッチセンサポートを設定する．

**引数**
  `port` センサポートのシンボル

**戻り値**
  nil

----

.. _mruby-on-ev3rt-touch-pressed:

pressed? -> bool
^^^^^^^^^^^^^^^^^

タッチセンサの状態を検出する．

**引数**
  なし

**戻り値**
  `true`  押されている状態

  `false` 押されていない状態

----


.. code-block:: ruby
  :caption: touch_sample.rb
