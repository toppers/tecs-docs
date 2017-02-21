
RTOS機能 - `RTOS`
==============

RTOS機能に関するAPIです．

特異メソッド一覧
----------------

* :ref:`RTOS.delay( msec ) <mruby-on-ev3rt-rtos-delay>`
* :ref:`RTOS.usec <mruby-on-ev3rt-rtos-usec>`
* :ref:`RTOS.msec <mruby-on-ev3rt-rtos-msec>`


特異メソッド
----------------

.. _mruby-on-ev3rt-rtos-delay:

RTOS.delay ( msec ) -> nil
^^^^^^^^^^^^^^^^^^^^^^^^^^

指定された時間遅延する （指定された時間後に実行が再開される）．

**引数**
  msec  遅延時間 (ミリ秒)

**戻り値**
  nil

----

.. _mruby-on-ev3rt-rtos-usec:

RTOS.usec -> Fixnum
^^^^^^^^^^^^^^^^^

性能評価用システム時刻の参照．

**引数**
  なし

**戻り値**
  性能評価用システム時刻の現在値 （マイクロ秒）

----

.. _mruby-on-ev3rt-rtos-msec:

RTOS.msec-> Fixnum
^^^^^^^^^^^^^^^^^

システム時刻の参照．

**引数**
  なし

**戻り値**
  システム時刻の現在値 （ミリ秒）

----

.. code-block:: ruby
  :caption: rtos_sample.rb
