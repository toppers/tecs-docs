
バランサ - `Balancer`
==============

バランス制御に関するAPIです．

特異メソッド一覧
----------------

* :ref:`Balancer.control <mruby-on-ev3rt-balancer-control>`


特異メソッド
----------------

.. _mruby-on-ev3rt-balancer-control:

Balancer.control -> Array
^^^^^^^^^^^^^^^^^^^^

左右モータPWM出力値を取得する．

**戻り値**
  0. 左モータPWM出力値
  #. 右モータPWM出力値 

----


.. code-block:: ruby
  :caption: ev3way_sample.rb
