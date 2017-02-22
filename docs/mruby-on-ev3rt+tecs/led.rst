
LEDライト - `LED`
==============

LEDライトに関するAPIです．

特異メソッド一覧
----------------

* :ref:`LED.color = (clr) <mruby-on-ev3rt-led-color>`
* :ref:`LED.off <mruby-on-ev3rt-led-off>`


シンボル
------

* **clr**

  設定できるLEDライトのカラーを表わすシンボル

  =======   =====
  シンボル
  ---------------
  :off      オフにする
  :red      赤
  :green    緑
  :orange   オレンジ
  =======   =====


特異メソッド
----------------

.. _mruby-on-ev3rt-led-color:

LED.color = ( clr ) -> nil
^^^^^^^^^^^^^^^^^^^^

LEDライトのカラーを設定する.
不正の設定値を指定した場合，LEDライトのカラーを変えない．

**引数**
  `clr` LEDカラーの設定値 （シンボル）

**戻り値**
  nil

----

.. _mruby-on-ev3rt-led-off:

LED.off -> nil
^^^^^^^^^^^^^^^^^^^^

LEDをオフにする．

**引数**
  なし

**戻り値**
  nil

----


.. code-block:: ruby
  :caption: led_sample.rb
