.. _atk2+tecs-alarm:

アラーム ― `tAlarm`
=================

アラームは繰り返し処理用のオブジェクトです。
アラームはカウンタに接続して、カウンタの起動によって動作します。

.. todo::
    to be filled in

使用方法
--------

アラームの生成
^^^^^^^^^^^^

アプリケーション開発者は `tAlarm` セルタイプのセルを生成することにより、アラームを生成することができます。次の例では ``MyAlarm`` という名前のアラームセルを生成し、 ``MyCell`` の ``eAlarmHandlerBody`` をメインルーチンとして結合しています。

.. code-block:: tecs-cdl
  :caption: app.cdl

  celltype tMyCellType {
      entry sHandlerBody eAlarmHandlerBody;
  };

  cell tMyCellType MyCell {};

  cell tAlarm MyAlarm {
  	  alarmTime = 10;
  	  cycleTime = 10;
      cBody = MyCell.eAlarmHandlerBody;
  };

.. code-block:: c
  :caption: tMyCellType.c

  void eAlarmHandlerBody_main()
  {
  }

リファレンス
------------

セルタイプ
^^^^^^^^^^

.. tecs:celltype:: tAlarm

  アラームの生成を行うココンポーネントです。

  .. tecs:attr:: char_t *name = C_EXP("$cell$")

  アラームの名前を指定します。
  指定しない場合、セルの名前が使用されます。

