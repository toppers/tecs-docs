
バランサ - `Balancer`
==============

バランス制御に関するAPIです．

特異メソッド一覧
----------------

* :ref:`Balancer.control <mruby-on-ev3rt-balancer-control>`


特異メソッド
----------------

.. _mruby-on-ev3rt-balancer-control:

Balancer.control(forward,turn,gyrosensor,gyro_offset,angle_l,angle_r,batteryvoltage) -> [Int]
^^^^^^^^^^^^^^^^^^^^

左右モータPWM出力値を取得する．

**引数**
  `forward` 前進/後退命令。100(前進最大値)～-100(後進最大値)
  
  `turn` 旋回命令。100(右旋回最大値)～-100(左旋回最大値)
  
  `gyrosensor` ジャイロセンサ値
  
  `gyro_offset` ジャイロセンサオフセット値
  
  `angle_l` 左モータエンコーダ値
  
  `angle_r` 右モータエンコーダ値
  
  `batteryvoltage` バッテリ電圧値(mV)
  
  `backlashhalf` バックラッシュの半分の値(rd)。0であればバックラッシュキャンセル処理を行わない

**戻り値**
  0. 左モータPWM出力値
  #. 右モータPWM出力値 

----


.. code-block:: ruby
  :caption: ev3way_sample.rb
