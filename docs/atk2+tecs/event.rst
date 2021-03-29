
.. _atk2+tecs-task:

イベント ― `tEvent`
=================

イベントは、タスク－タスク間、タスク－C2ISR間での同期ための機能です。

.. todo::
    to be filled in

使用方法
--------

イベントの生成
^^^^^^^^^^^^

アプリケーション開発者は `tEvent` セルタイプのセルを生成することにより、イベントを生成することができます。次の例では ``MyEvent`` という名前のイベントセルを生成しています。

.. code-block:: tecs-cdl
  :caption: app.cdl

  celltype tMyCellType {
      call sEventMask cEventMask;
  };

  cell tMyCellType MyCell {};

  cell tEvent MyEvent {
      eEventMask = MyCell.cEventMask;
  };

.. code-block:: c
  :caption: tMyCellType.c

リファレンス
------------

セルタイプ
^^^^^^^^^^

.. tecs:celltype:: tEvent

  イベントの生成を行うコンポーネントです。

  .. tecs:attr:: char_t *name = C_EXP("$cell$")

    イベントの名前を指定します。
    指定しない場合、セルの名前が使用されます。

  .. tecs:attr:: uint32_t mask = C_EXP("AUTO")

    イベントのマスク値を指定します。
    指定しない場合、イベントマスク値は自動的に設定されます。

  .. tecs:attr:: EventMaskType p_mask = C_EXP("$cell$");


シグニチャ
^^^^^^^^^^

.. tecs:signature:: sEventMask

  
  .. tecs:sigfunction:: EventMaskType get(void)


    


