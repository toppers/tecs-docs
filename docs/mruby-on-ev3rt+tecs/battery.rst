
バッテリ - `Battery`
==============

バッテリに関するAPIです．

特異メソッド一覧
----------------

* :ref:`Battery.mA <mruby-on-ev3rt-battery-ma>`
* :ref:`Battery.mV <mruby-on-ev3rt-battery-mv>`


特異メソッド
----------------

.. _mruby-on-ev3rt-battery-ma:

Battery.mA -> Fixnum
^^^^^^^^^^^^^^^^^^^^

バッテリの電流を取得する．

**戻り値**
  バッテリの電流 （mA）

----

.. _mruby-on-ev3rt-battery-mv:

Battery.mV -> Fixnum
^^^^^^^^^^^^^^^^^^^^

バッテリの電圧を取得する．

**戻り値**
  バッテリの電圧 （mV）

----


.. code-block:: ruby
  :caption: battery_sample.rb
