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


  .. tecs:attr:: uint8_t id = C_EXP("$ID$")

  アラームのIDを指定します。


  .. tecs:attr:: char_t *counter

  アラームに接続するカウンタを指定します。



  .. tecs:attr:: char_t *action

  アラームアクションを指定します。


    .. c:macro:: SETEVENT

    イベントのセット。


    .. c:macro:: ACTIVATETASK

    タスクの起動。


    .. c:macro:: ALARMCALLBACK

    コールバックの呼び出し。


  .. tecs:attr:: char_t *task = "OMISSIBLE"

  アラームのアクションで起動するタスクを指定します。


  .. tecs:attr:: char_t *event = "OMISSIBLE"

  アラームのアクションでセットするイベントを指定します。


  .. tecs:attr:: char_t *callbackName = "OMISSIBLE"

  アラームのアクションで呼び出すコールバックを指定します。

  .. tecs:attr:: bool_t autoStart

  アラームの自動起動設定。

    .. c:macro:: True

    自動起動する。

    .. c:macro:: False

    自動起動しない。

  .. tecs:attr:: uint32_t alarmTime = 0

  アラーム自動起動時の初回満了時刻を指定します。


  .. tecs:attr:: uint32_t cycleTime = 0

  アラーム自動起動時の周期時間を指定します。0の場合は単発アラームとなります。


  .. tecs:attr:: char_t *appMode[] = { "OMISSIBLE" }

  自動起動するアプリケーションモードを指定します。


シグニチャ
^^^^^^^^^^

.. tecs:signature:: sAlarm

  アラームを操作するためのシグニチャ（Task,ISR2用）。

  .. tecs:sigfunction:: StatusType getBase([out] AlarmBaseRefType p_info)

    アラームの情報を取得する。
    アラーム情報は p_info で示す構造体(AlarmBaseRefType)に格納される。

  .. tecs:sigfunction::　StatusType get([out] TickRefType p_tick)

    アラームが満了するまでのティック数を取得し、 p_tick の領域に格納する。

  .. tecs:sigfunction:: StatusType setRelative([in] TickType incr, [in] TickType cycle)

    アラームが現在のティックから incr で指定された相対時刻が経過した後に満了するよう設定する。
    初回の満了後、cycle が 0 でない場合は、cycle の周期でアラームを満了させる。 

  .. tecs:sigfunction:: StatusType setAbsolute([in] TickType start, [in] TickType cycle)

    アラームが start で指定された絶対時刻に達した際に満了するよう設定する。
    初回の満了後、cycle が 0 でない場合は cycle の周期でアラームを満了させる。

  .. tecs:sigfunction::　StatusType cancel(void)

    アラームを停止する。



.. tecs:signature:: sAlarmHook

  アラームを操作するためのシグニチャ（Hook用）。

  .. tecs:sigfunction:: StatusType getBase([out] AlarmBaseRefType p_info)

    アラームの情報を取得する。
    アラーム情報は p_info で示す構造体(AlarmBaseRefType)に格納される。

  .. tecs:sigfunction::　StatusType get([out] TickRefType p_tick)

    アラームが満了するまでのティック数を取得し、 p_tick の領域に格納する。


