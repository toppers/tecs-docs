.. _atk2+tecs-counter:

カウンタ ― `tCounter`
=================

カウンタは処理タイミング通知用のオブジェクトです。
ティックという単位で事象をカウントします。
カウンタは2種類あります。
ソフトウェアカウンタ
  システムサービスでティックをインクリメントする
ハードウェアカウンタ
  ハードウェア（タイマなど）がティックをインクリメントする

主にアラーム、スケジュールテーブルに接続して使用する。
.. todo::
    to be filled in

使用方法
--------

カウンタの生成
^^^^^^^^^^^^

アプリケーション開発者は `tCounter` セルタイプのセルを生成することにより、カウンタを生成することができます。次の例では ``MyCounter`` という名前のカウンタセルを生成します。

.. code-block:: tecs-cdl
  :caption: app.cdl

  cell tCounter MyCounter {
      *counterType = "SOFTWARE"
      minimumCycle = 10;
      maximumAllowedValue = "100";
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

.. tecs:celltype:: tCouter

    カウンタの生成を行うココンポーネントです。


  .. tecs:attr:: uint8_t id = C_EXP("$ID$")

    カウンタのIDの識別子を指定します。


  .. tecs:attr:: char_t *name = C_EXP("$cell$")

   カウンタの名前を指定します。
   指定しない場合、セルの名前が使用されます。


  .. tecs:attr:: char_t   *counterType = "SOFTWARE"
    カウンタのタイプを指定します。

    .. c:macro:: HARDWARE

      ハードウェアカウンタ

    .. c:macro:: SOFTWARE

      ソフトウェアカウンタ




  .. tecs:attr:: uint32_t minimumCycle

    接続されたアラームがカウンタに指定できる最小周期値を指定します。


  .. tecs:attr:: uint32_t maximumAllowedValue

    カウンタのティックの最大値を指定します。


  .. tecs:attr::　uint32_t ticksPerBase

    カウンタ固有の値（OSは不使用）


シグニチャ
^^^^^^^^^^

.. tecs:signature:: sCounter

  カウンタを操作するためのシグニチャ

  .. tecs:sigfunction:: StatusType signal(void)


