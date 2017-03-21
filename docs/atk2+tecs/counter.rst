.. _atk2+tecs-counter:

カウンタ ― `tCountet`
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

