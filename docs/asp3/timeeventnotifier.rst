
.. _asp3tecs-timeeventnotifier:

タイムイベント通知
==================

タイムイベント通知は、時間の経過 (タイムイベントの発生) をアプリケーションに通知する機能です。

タイムイベント通知には以下の2種類があり、これらを総括してタイムイベント通知と呼びます:

周期通知
    サービスコールまたは静的APIによる指定で動作開始要求が行われると、指定した周期で、繰り返し通知を行います。通知が行われる時刻は、周期通知が起動された時刻、または `TA_PHS` 属性が指定された場合は周期通知が生成された時刻を基準として、通知位相＋通知周期×(n-1) (n=1, 2, ...) と表すことができます。

アラーム通知
    サービスコールで指定した相対時間後に通知を行います。

タイムイベントの通知は、次のいずれかの方法で行うことができます [:toppers3-tag:`NGKI3689`]。

+--------------------------------+----------------------------------------------------+
|            通知方法            |                対応する(疑似)コード                |
+================================+====================================================+
| タイムイベントハンドラの呼出し | ``handler.ciHandlerBody.main();``                  |
+--------------------------------+----------------------------------------------------+
| 変数の設定                     | ``*setVariableAddress = setVariableValue;``        |
+--------------------------------+----------------------------------------------------+
| 変数のインクリメント           | ``++*incrementedVariableAddress;``                 |
+--------------------------------+----------------------------------------------------+
| タスクの起動                   | ``er = act_tsk(handler.id);``                      |
+--------------------------------+----------------------------------------------------+
| タスクの起床                   | ``er = wup_tsk(handler.id);``                      |
+--------------------------------+----------------------------------------------------+
| セマフォの資源の返却           | ``er = sig_sem(handler.id);``                      |
+--------------------------------+----------------------------------------------------+
| イベントフラグのセット         | ``er = set_flg(handler.id, flagPattern);``         |
+--------------------------------+----------------------------------------------------+
| データキューへの送信           | ``er = psnd_dtq(handler.id, dataqueueSentValue);`` |
+--------------------------------+----------------------------------------------------+

これらの通知方法のうち、最後の5つは通知のためのサービスコールがエラーを返し、タイムイベントの通知に失敗する場合があります。タイムイベントの通知に失敗した場合、エラーの通知を次のいずれかの方法で行うことができます [:toppers3-tag:`NGKI3690`]。

+------------------------+----------------------------------------------------+
|     エラー通知方法     |                対応する(疑似)コード                |
+========================+====================================================+
| なし                   |                                                    |
+------------------------+----------------------------------------------------+
| 変数の設定             | ``*setVariableAddressForError = er;``              |
+------------------------+----------------------------------------------------+
| 変数のインクリメント   | ``++*incrementedVariableAddressForError;``         |
+------------------------+----------------------------------------------------+
| タスクの起動           | ``act_tsk(errorHandler.id);``                      |
+------------------------+----------------------------------------------------+
| タスクの起床           | ``wup_tsk(errorHandler.id);``                      |
+------------------------+----------------------------------------------------+
| セマフォの資源の返却   | ``sig_sem(errorHandler.id);``                      |
+------------------------+----------------------------------------------------+
| イベントフラグのセット | ``set_flg(errorHandler.id, flagPatternForError);`` |
+------------------------+----------------------------------------------------+
| データキューへの送信   | ``psnd_dtq(errorHandler.id, er);``                 |
+------------------------+----------------------------------------------------+

エラー通知が失敗した場合、エラーは無視され、何も行われません [:toppers3-tag:`NGKI3691`]。

.. _asp3tecs-timeeventnotifier-usage:

使用方法
--------

周期通知・アラーム通知
^^^^^^^^^^^^^^^^^^^^^^

アプリケーション開発者は `tCyclicNotifier` セルタイプのセルを生成することにより、周期通知を生成することができます。

.. code-block:: tecs-cdl

  cell tCyclicNotifier Cyclic {
      attribute = C_EXP("TA_STA"); // 生成直後から動作開始
      cycleTime = 1000000; // 1,000,000 マイクロ秒 (1秒) 周期
  };

同様に、 `tAlarmNotifier` セルタイプのセルを生成することにより、アラーム通知を生成することができます。

.. code-block:: tecs-cdl

  cell tAlarmNotifier Alarm {
  };

タイムイベント通知を使用する場合、さらに通知方法を指定する必要があります。通知方法の指定について次に説明します。
以下の説明では `tAlarmNotifier` のみを使用しますが、 `tCyclicNotifier` でも同様の方法で指定することができます。

変数の設定・インクリメントによる通知
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

変数の設定により通知を行いたい場合、まずヘッダファイルで変数を宣言します。続いてヘッダファイルの変数宣言をTECS CDLから `import_C` により読込み、 :tecs:attr:`~tAlarmNotifier::setVariableAddress` 属性でその変数のアドレスを指定し、:tecs:attr:`~tAlarmNotifier::setVariableValue` で設定する値を指定します。

.. code-block:: c
  :caption: app.c

  #include "app.h"
  intptr_t foo_variable;

.. code-block:: c
  :caption: app.h

  extern intptr_t foo_variable;

.. code-block:: tecs-cdl

  import_C("app.h");
  cell tAlarmNotifier Alarm {
      setVariableAddress = C_EXP("&foo_variable");
      setVariableValue = 42;
  };

変数のインクリメントにより通知を行いたい場合は、:tecs:attr:`~tAlarmNotifier::incrementedVariableAddress` で変数のアドレスを指定します。

.. code-block:: tecs-cdl

  import_C("app.h");
  cell tAlarmNotifier Alarm {
      incrementedVariableAddress = C_EXP("&foo_variable");
  };

タスクの起動・起床による通知
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

タスクの起動により通知を行いたい場合、タイムイベント通知セルの呼び口 :tecs:call:`~tAlarmNotifier::ciNotificationHandler` を、タスクの :tecs:entry:`tTask::eiActivateNotificationHandler` に結合します。

.. code-block:: tecs-cdl

  cell tTask MyTask { /* 省略 */ };
  cell tAlarmNotifier Alarm {
      ciNotificationHandler = MyTask.eiActivateNotificationHandler;
  };

同様に、:tecs:entry:`tTask::eiWakeUpNotificationHandler` に結合することで、タスクの起床により通知を行うことができます。

セマフォの返却による通知
^^^^^^^^^^^^^^^^^^^^^^^

タスクの起動により通知を行いたい場合、タイムイベント通知セルの呼び口 :tecs:call:`~tAlarmNotifier::ciNotificationHandler` を、セマフォの :tecs:entry:`tSemaphore::eiNotificationHandler` に結合します。

.. code-block:: tecs-cdl

  cell tSemaphore MySemaphore { /* 省略 */ };
  cell tAlarmNotifier Alarm {
      ciNotificationHandler = MySemaphore.eiNotificationHandler;
  };

イベントフラグのセットによる通知
^^^^^^^^^^^^^^^^^^^^^^^

イベントフラグのセットにより通知を行いたい場合、タイムイベント通知セルの呼び口 :tecs:call:`~tAlarmNotifier::ciNotificationHandler` を、セマフォの :tecs:entry:`tEventflag::eiNotificationHandler` に結合します。セットするフラグパターンは属性 :tecs:attr:`~tAlarmNotifier::flagPattern` により指定します。

.. code-block:: tecs-cdl

  cell tEventflag MyEventFlag { /* 省略 */ };
  cell tAlarmNotifier Alarm {
      ciNotificationHandler = MyEventFlag.eiNotificationHandler;
      flagPattern = 1;
  };

データキューへの送信による通知
^^^^^^^^^^^^^^^^^^^^^^^

データキューへの送信により通知を行いたい場合、タイムイベント通知セルの呼び口 :tecs:call:`~tAlarmNotifier::ciNotificationHandler` を、セマフォの :tecs:entry:`tDataqueue::eiNotificationHandler` に結合します。セットするフラグパターンは属性 :tecs:attr:`~tAlarmNotifier::dataqueueSentValue` により指定します。

.. code-block:: tecs-cdl

  cell tDataqueue MyDataqueue { /* 省略 */ };
  cell tAlarmNotifier Alarm {
      ciNotificationHandler = MyDataqueue.eiNotificationHandler;
      dataqueueSentValue = 0xdeadbeef;
  };

ハンドラ関数による通知
^^^^^^^^^^^^^^^^^^^^^^^

ハンドラ関数により通知を行いたい場合、\ `tAlarmNotifier`, `tCyclicNotifier` の代わりに `tAlarmHandler`, `tCyclicHandler` を使用します。通知先にシグニチャ :tecs:signature:`siHandlerBody` の受け口を定義し、タイムイベント通知セルの呼び口 :tecs:call:`~tAlarmHandler::ciHandlerBody` をその受け口に結合します。

.. code-block:: c
  :caption: tMyCellType.c

  void eiHandlerBody_main(CELLIDX idx)
  {
      CELLCB  *p_cellcb = GET_CELLCB(idx);
      // ...
  }

.. code-block:: tecs-cdl

  celltype tMyCellType {
      entry siHandlerBody eiHandlerBody;
  };

  cell tMyCellType MyCell {};

  cell tAlarmHandler Alarm {
      ciHandlerBody = MyCell.eiHandlerBody;
  };

.. attention::

  タイムイベントの通知方法は複数ありますが、各タイムイベント通知に対し一度に指定できる通知方法は一つに制限されます。
  例えば、 :tecs:attr:`~tAlarmNotifier::setVariableAddress` (設定先変数) と :tecs:attr:`~tAlarmNotifier::incrementedVariableAddress` (インクリメント先変数) を同時に指定することはできず、この指定があるときにTECSジェネレータを実行すると、エラーが発生します。

  通知方法を指定しなかった場合もエラーとなります。

エラー通知
^^^^^^^^^^^

以上の通知方法のうち、タスクの起動, タスクの起床, セマフォの資源の返却, イベントフラグのセット, データキューへの送信の5つは、内部的にはそれぞれ対応するサービスコールの呼出しにより実現されています。
サービスコールの呼出しが行われるとき、様々な要因によりサービスコールが失敗しエラーを返すことがあります。エラーが発生する具体的状況をいくつか挙げてみましょう (網羅的ではありません):

 * **タスクの起動** (`act_tsk`): タスク起動要求キューイングオーバーフロー (`E_QOVR`)
 * **タスクの起床** (`wup_tsk`): タスクが休止状態 (`E_OBJ`)、タスク起床要求キューイングオーバーフロー (`E_QOVR`)
 * **セマフォの資源の返却**: セマフォの資源数がすでに最大値に達している (`E_QOVR`)
 * **イベントフラグのセット**: (ASP3+TECS で発生するエラーはありません)
 * **データキューへの送信**: バッファオーバフロー (`E_TMOUT`)

タイムイベント通知には、こうした場合にもう一つの通知方法を用いてエラーを通知することができます。

エラー通知方法は、通常の通知と同様に指定することができます (ただし、ハンドラ関数をエラー通知に用いることはできません)。呼び口は :tecs:call:`~tAlarmNotifier::ciNotificationHandler` の代わりに :tecs:call:`~tAlarmNotifier::ciErrorNotificationHandler` を用い、属性は末尾に ``ForError`` を加えたものを使用しますが、いくつか例外が存在します。属性名の対応表を次に示します:

+----------------------------------------------------------+------------------------------------------------------------------+
|                         通常通知                         |                            エラー通知                            |
+==========================================================+==================================================================+
| :tecs:attr:`~tAlarmNotifier::setVariableAddress`         | :tecs:attr:`~tAlarmNotifier::setVariableAddressForError`         |
+----------------------------------------------------------+------------------------------------------------------------------+
| :tecs:attr:`~tAlarmNotifier::setVariableValue`           | --                                                               |
+----------------------------------------------------------+------------------------------------------------------------------+
| :tecs:attr:`~tAlarmNotifier::incrementedVariableAddress` | :tecs:attr:`~tAlarmNotifier::incrementedVariableAddressForError` |
+----------------------------------------------------------+------------------------------------------------------------------+
| :tecs:attr:`~tAlarmNotifier::flagPattern`                | :tecs:attr:`~tAlarmNotifier::flagPatternForError`                |
+----------------------------------------------------------+------------------------------------------------------------------+
| :tecs:attr:`~tAlarmNotifier::dataqueueSentValue`         | --                                                               |
+----------------------------------------------------------+------------------------------------------------------------------+

この表の右の列が空欄になっている属性は、対応する属性が存在せず、エラー番号が代わりの値として使用されます。

.. attention::

  通常の通知方法と同様に、エラー通知方法は複数ありますが、各タイムイベント通知に対し一度に指定できるエラー通知方法は一つに制限されます。

  エラー通知方法の指定を省略することは可能ですが、TECSジェネレータの実行時に警告が出力されます。警告を表示したくない場合は属性 :tecs:attr:`~tAlarmNotifier::ignoreErrors` を ``true`` に設定してください。

  通常の通知方法がエラーが発生しないもの (タイムイベントハンドラの呼出し, 変数の設定, 変数のインクリメント) である場合、エラー通知方法を指定することはできず、指定した場合はエラーが発生します。

周期通知を制御する
^^^^^^^^^^^^^^^^^^^

`tCyclicNotifier` が提供する :tecs:entry:`~tCyclicNotifier::eCyclic` という名前の受け口を利用することにより、周期通知の制御及び状態の取得を行うことができます。

.. code-block:: tecs-cdl
  :caption: app.cdl

  cell tCyclicNotifier Cyclic {};

  celltype tMyCellType {
      call sCyclic cCyclic;
  };

  cell tMyCellType MyCell {
      cCyclic = Cyclic.eCyclic;
  };

.. code-block:: c
  :caption: tMyCellType.c

  // 周期通知を動作開始
  cCyclic_start();

  // 周期通知の現在状態の参照
  T_RCYC cyclicStatus;
  cCyclic_refer(&cyclicStatus);

周期通知は非タスクコンテキストから操作することはできません。

アラーム通知を制御する
^^^^^^^^^^^^^^^^^^^^^^^

`tAlarmNotifier` が提供する :tecs:entry:`~tAlarmNotifier::eAlarm` という名前の受け口を利用することにより、アラーム通知の制御及び状態の取得を行うことができます。

.. code-block:: tecs-cdl
  :caption: app.cdl

  cell tAlarmNotifier Alarm {};

  celltype tMyCellType {
      call sAlarm cAlarm;
  };

  cell tMyCellType MyCell {
      cAlarm = Alarm.eAlarm;
  };

.. code-block:: c
  :caption: tMyCellType.c

  // アラーム通知を動作開始
  cAlarm_start(1000000); // 1,000,000 マイクロ秒 (1秒) 後に通知

  // アラーム通知の現在状態の参照
  T_RALM alarmStatus;
  cAlarm_refer(&alarmStatus);

非タスクコンテキスト内では、:tecs:entry:`~tAlarmNotifier::eAlarm` の代わりに :tecs:entry:`~tAlarmNotifier::eiAlarm` を使用する必要があります。

リファレンス
------------

セルタイプ
^^^^^^^^^^

.. tecs:celltype:: tAlarmNotifier

  アラーム通知の生成、制御及び状態の取得を行うコンポーネントです。

  本コンポーネントは `CRE_ALM` 静的API [:toppers3-tag:`NGKI2487`] によりアラーム通知の生成を行います。

  .. attention::

    通知方法に関係する属性はTECSのコンポーネントモデル上はすべて「省略可能」として定義されていますが、実際には専用のTECSジェネレータプラグインの働きにより、複雑な条件によって指定が制約されています。可能な指定方法については\ :ref:`asp3tecs-timeeventnotifier-usage`\ のセクションを参照して下さい。

  .. tecs:attr:: ID id = C_EXP("ALMID_$id$")

    アラーム通知のID番号の識別子 (詳しくは :ref:`asp3tecs-id` を参照) を `C_EXP` で囲んで指定します (省略可能)。

  .. tecs:attr:: ATR attribute = C_EXP("TA_NULL")

    アラーム通知属性を `C_EXP` で囲んで指定します (省略可能)。ASP3では指定できる属性はありません [:toppers3-tag:`NGKI3423`] ので、指定できる値は ``C_EXP("TA_NULL")`` のみです [:toppers3-tag:`NGKI3424`]。

  .. tecs:attr:: bool_t ignoreErrors = false

    通知方法としてエラーが発生する可能性があるもの (タスクの起動, タスクの起床, セマフォの資源の返却, イベントフラグのセット, データキューへの送信) を指定しているとき、エラー通知方法を指定しなかった場合、TECSジェネレータ実行時に警告を出力するかを指定します (省略可能)。

    デフォルト値は ``false`` で、エラー通知方法が未指定の場合に警告を出力します。

  .. tecs:attr:: intptr_t *setVariableAddress = 0

    通知方法として「変数の設定」を使用する場合に、設定先の変数を指すポインタを指定します。

    他の通知方法を使用する場合は、指定してはけません。

  .. tecs:attr:: intptr_t setVariableValue = 0

    通知方法として「変数の設定」を使用する場合に、変数に設定する値を指定します。

    他の通知方法を使用する場合は、指定してはけません。

  .. tecs:attr:: intptr_t *incrementedVariableAddress = 0

    通知方法として「変数のインクリメント」を使用する場合に、インクリメント対象の変数を指すポインタを指定します。

    他の通知方法を使用する場合は、指定してはけません。

  .. tecs:attr:: FLGPTN flagPattern = 0

    通知方法として「イベントフラグのセット」を使用する場合に、セットするフラグパターンを指定します。

    他の通知方法を使用する場合は、指定してはけません。

  .. tecs:attr:: intptr_t dataqueueSentValue = 0

    通知方法として「データキューへの送信」を使用する場合に、データキューに送信する値を指定します。

    他の通知方法を使用する場合は、指定してはけません。

  .. tecs:attr:: intptr_t *setVariableAddressForError = 0

    エラー通知方法として「変数の設定」を使用する場合に、エラーコードを設定する先の変数を指すポインタを指定します。

    他の通知方法を使用する場合は、指定してはけません。

  .. tecs:attr:: intptr_t *incrementedVariableAddressForError = 0

    エラー通知方法として「変数のインクリメント」を使用する場合に、インクリメント対象の変数を指すポインタを指定します。

    他の通知方法を使用する場合は、指定してはけません。

  .. tecs:attr:: FLGPTN flagPatternForError = 0

    エラー通知方法として「イベントフラグのセット」を使用する場合に、セットするフラグパターンを指定します。

    他の通知方法を使用する場合は、指定してはけません。

  .. tecs:call:: call siNotificationHandler ciNotificationHandler

    通知先のセルを結合します。結合可能なセルタイプ・受け口は通知方法ごとに異なります。

    +--------------------------------+--------------------------------------------------------+
    |            通知方法            |                   セルタイプ, 受け口                   |
    +================================+========================================================+
    | タイムイベントハンドラの呼出し | :tecs:entry:`tTimeEventHandler::eiNotificationHandler` |
    +--------------------------------+--------------------------------------------------------+
    | 変数の設定                     | 結合してはいけません                                   |
    +--------------------------------+--------------------------------------------------------+
    | 変数のインクリメント           | 結合してはいけません                                   |
    +--------------------------------+--------------------------------------------------------+
    | タスクの起動                   | :tecs:entry:`tTask::eiActivateNotificationHandler`     |
    +--------------------------------+--------------------------------------------------------+
    | タスクの起床                   | :tecs:entry:`tTask::eiWakeUpNotificationHandler`       |
    +--------------------------------+--------------------------------------------------------+
    | セマフォの資源の返却           | :tecs:entry:`tSemaphore::eiNotificationHandler`        |
    +--------------------------------+--------------------------------------------------------+
    | イベントフラグのセット         | :tecs:entry:`tEventflag::eiNotificationHandler`        |
    +--------------------------------+--------------------------------------------------------+
    | データキューへの送信           | :tecs:entry:`tDataqueue::eiNotificationHandler`        |
    +--------------------------------+--------------------------------------------------------+

    上記の表にないセルタイプ・受け口を結合した場合、TECSジェネレータ実行時にエラーが発生します。

  .. tecs:call:: call siNotificationHandler ciErrorNotificationHandler

    エラー通知先のセルを結合します。結合可能なセルタイプ・受け口は通知方法ごとに異なります。

    +------------------------+----------------------------------------------------+
    |     エラー通知方法     |                 セルタイプ, 受け口                 |
    +========================+====================================================+
    | なし                   | 結合してはいけません                               |
    +------------------------+----------------------------------------------------+
    | 変数の設定             | 結合してはいけません                               |
    +------------------------+----------------------------------------------------+
    | 変数のインクリメント   | 結合してはいけません                               |
    +------------------------+----------------------------------------------------+
    | タスクの起動           | :tecs:entry:`tTask::eiActivateNotificationHandler` |
    +------------------------+----------------------------------------------------+
    | タスクの起床           | :tecs:entry:`tTask::eiWakeUpNotificationHandler`   |
    +------------------------+----------------------------------------------------+
    | セマフォの資源の返却   | :tecs:entry:`tSemaphore::eiNotificationHandler`    |
    +------------------------+----------------------------------------------------+
    | イベントフラグのセット | :tecs:entry:`tEventflag::eiNotificationHandler`    |
    +------------------------+----------------------------------------------------+
    | データキューへの送信   | :tecs:entry:`tDataqueue::eiNotificationHandler`    |
    +------------------------+----------------------------------------------------+

    上記の表にないセルタイプ・受け口を結合した場合、TECSジェネレータ実行時にエラーが発生します。

  .. tecs:entry:: entry sAlarm eAlarm

    アラーム通知の制御及び状態の取得を行うための受け口です (タスクコンテキスト用)。

  .. tecs:entry:: entry siAlarm eiAlarm

    アラーム通知の制御を行うための受け口です (非タスクコンテキスト用)。

.. tecs:celltype:: tCyclicNotifier

  周期通知の生成、制御及び状態の取得を行うコンポーネントです。

  本コンポーネントは `CRE_CYC` 静的API [:toppers3-tag:`NGKI3727`] により周期通知の生成を行います。

  周期通知は、動作している状態と動作していない状態のいずれかをとり [:toppers3-tag:`NGKI2366`]、動作している状態にすることを動作開始、動作していない状態にすることを動作停止と呼びます。

  周期通知による通知は、基準時刻を基準として、 ``cyclePhase+cyclicTime*(n-1)`` (n=1, 2, ...) で表される時刻に行われます。基準時刻は属性 `TA_PHS` を指定した場合は周期通知の生成がされた時刻、指定されなかった場合は周期通知が最後に動作開始した時刻が用いられます [:toppers3-tag:`NGKI2365`]。

  .. attention::

    通知方法に関係する属性はTECSのコンポーネントモデル上はすべて「省略可能」として定義されていますが、実際には専用のTECSジェネレータプラグインの働きにより、複雑な条件によって指定が制約されています。可能な指定方法については\ :ref:`asp3tecs-timeeventnotifier-usage`\ のセクションを参照して下さい。

  .. tecs:attr:: ID id = C_EXP("CYCID_$id$")

    周期通知のID番号の識別子 (詳しくは :ref:`asp3tecs-id` を参照) を `C_EXP` で囲んで指定します (省略可能)。

  .. tecs:attr:: ATR attribute = C_EXP("TA_NULL")

    周期通知属性を `C_EXP` で囲んで指定します [:toppers3-tag:`NGKI2370`] (省略可能)。複数個指定する場合、ビット毎の論理和演算子を用いて ``C_EXP("TA_STA | TA_PHS")`` のようにして指定します。

    .. c:macro:: TA_STA

      周期通知の生成時に周期通知を動作開始します。

    .. c:macro:: TA_PHS

      周期通知を生成した時刻を基準時刻とします。

  .. tecs:attr:: RELTIM cycleTime

    周期通知の通知周期をマイクロ秒単位で指定します。

  .. tecs:attr:: RELTIM cyclePhase = 0

    周期通知の通知位相をマイクロ秒単位で指定します (省略可能)。

  .. tecs:attr:: bool_t ignoreErrors = false

    通知方法としてエラーが発生する可能性があるもの (タスクの起動, タスクの起床, セマフォの資源の返却, イベントフラグのセット, データキューへの送信) を指定しているとき、エラー通知方法を指定しなかった場合、TECSジェネレータ実行時に警告を出力するかを指定します (省略可能)。

    デフォルト値は ``false`` で、エラー通知方法が未指定の場合に警告を出力します。

  .. tecs:attr:: intptr_t *setVariableAddress = 0

    通知方法として「変数の設定」を使用する場合に、設定先の変数を指すポインタを指定します。

    他の通知方法を使用する場合は、指定してはけません。

  .. tecs:attr:: intptr_t setVariableValue = 0

    通知方法として「変数の設定」を使用する場合に、変数に設定する値を指定します。

    他の通知方法を使用する場合は、指定してはけません。

  .. tecs:attr:: intptr_t *incrementedVariableAddress = 0

    通知方法として「変数のインクリメント」を使用する場合に、インクリメント対象の変数を指すポインタを指定します。

    他の通知方法を使用する場合は、指定してはけません。

  .. tecs:attr:: FLGPTN flagPattern = 0

    通知方法として「イベントフラグのセット」を使用する場合に、セットするフラグパターンを指定します。

    他の通知方法を使用する場合は、指定してはけません。

  .. tecs:attr:: intptr_t dataqueueSentValue = 0

    通知方法として「データキューへの送信」を使用する場合に、データキューに送信する値を指定します。

    他の通知方法を使用する場合は、指定してはけません。

  .. tecs:attr:: intptr_t *setVariableAddressForError = 0

    エラー通知方法として「変数の設定」を使用する場合に、エラーコードを設定する先の変数を指すポインタを指定します。

    他の通知方法を使用する場合は、指定してはけません。

  .. tecs:attr:: intptr_t *incrementedVariableAddressForError = 0

    エラー通知方法として「変数のインクリメント」を使用する場合に、インクリメント対象の変数を指すポインタを指定します。

    他の通知方法を使用する場合は、指定してはけません。

  .. tecs:attr:: FLGPTN flagPatternForError = 0

    エラー通知方法として「イベントフラグのセット」を使用する場合に、セットするフラグパターンを指定します。

    他の通知方法を使用する場合は、指定してはけません。

  .. tecs:call:: call siNotificationHandler ciNotificationHandler

    通知先のセルを結合します。結合可能なセルタイプ・受け口は通知方法ごとに異なります。

    +--------------------------------+--------------------------------------------------------+
    |            通知方法            |                   セルタイプ, 受け口                   |
    +================================+========================================================+
    | タイムイベントハンドラの呼出し | :tecs:entry:`tTimeEventHandler::eiNotificationHandler` |
    +--------------------------------+--------------------------------------------------------+
    | 変数の設定                     | 結合してはいけません                                   |
    +--------------------------------+--------------------------------------------------------+
    | 変数のインクリメント           | 結合してはいけません                                   |
    +--------------------------------+--------------------------------------------------------+
    | タスクの起動                   | :tecs:entry:`tTask::eiActivateNotificationHandler`     |
    +--------------------------------+--------------------------------------------------------+
    | タスクの起床                   | :tecs:entry:`tTask::eiWakeUpNotificationHandler`       |
    +--------------------------------+--------------------------------------------------------+
    | セマフォの資源の返却           | :tecs:entry:`tSemaphore::eiNotificationHandler`        |
    +--------------------------------+--------------------------------------------------------+
    | イベントフラグのセット         | :tecs:entry:`tEventflag::eiNotificationHandler`        |
    +--------------------------------+--------------------------------------------------------+
    | データキューへの送信           | :tecs:entry:`tDataqueue::eiNotificationHandler`        |
    +--------------------------------+--------------------------------------------------------+

    上記の表にないセルタイプ・受け口を結合した場合、TECSジェネレータ実行時にエラーが発生します。

  .. tecs:call:: call siNotificationHandler ciErrorNotificationHandler

    エラー通知先のセルを結合します。結合可能なセルタイプ・受け口は通知方法ごとに異なります。

    +------------------------+----------------------------------------------------+
    |     エラー通知方法     |                 セルタイプ, 受け口                 |
    +========================+====================================================+
    | なし                   | 結合してはいけません                               |
    +------------------------+----------------------------------------------------+
    | 変数の設定             | 結合してはいけません                               |
    +------------------------+----------------------------------------------------+
    | 変数のインクリメント   | 結合してはいけません                               |
    +------------------------+----------------------------------------------------+
    | タスクの起動           | :tecs:entry:`tTask::eiActivateNotificationHandler` |
    +------------------------+----------------------------------------------------+
    | タスクの起床           | :tecs:entry:`tTask::eiWakeUpNotificationHandler`   |
    +------------------------+----------------------------------------------------+
    | セマフォの資源の返却   | :tecs:entry:`tSemaphore::eiNotificationHandler`    |
    +------------------------+----------------------------------------------------+
    | イベントフラグのセット | :tecs:entry:`tEventflag::eiNotificationHandler`    |
    +------------------------+----------------------------------------------------+
    | データキューへの送信   | :tecs:entry:`tDataqueue::eiNotificationHandler`    |
    +------------------------+----------------------------------------------------+

    上記の表にないセルタイプ・受け口を結合した場合、TECSジェネレータ実行時にエラーが発生します。

  .. tecs:entry:: entry sCyclic eCyclic

    周期通知の制御及び状態の取得を行うための受け口です (タスクコンテキスト用)。

    非タスクコンテキスト用の受け口はありません。

.. tecs:celltype:: tTimeEventHandler

  タイムイベント通知セルで、通知方法「タイムイベントハンドラの呼出し」により通知を行いたい場合に使用するセルタイプです。

  一般的なアプリケーションではこのセルタイプを直接する必要はなく、 `tAlarmHandler` または `tCyclicHandler` を使用することが推奨されます。

  .. tecs:entry:: entry siNotificationHandler eiNotificationHandler

    通知元のタイムイベント通知セルの :tecs:call:`tAlarmNotifier::ciNotificationHandler` または :tecs:call:`tCyclicNotifier::ciNotificationHandler` に結合します。

  .. tecs:call:: call siHandlerBody ciHandlerBody

    タイムイベントハンドラの本体となる受け口を結合します。

.. tecs:celltype:: tAlarmHandler

  アラーム通知の生成、制御及び状態の取得を行うコンポーネントです。このセルタイプはハンドラ関数により通知を行う場合に使用します。他の通知方法を使用したい場合、 `tAlarmNotifier` を使用して下さい。

  本コンポーネントは `CRE_ALM` 静的API [:toppers3-tag:`NGKI2487`] によりアラーム通知の生成を行います。

  .. tecs:attr:: ID id = C_EXP("ALMID_$id$")

    アラーム通知のID番号の識別子 (詳しくは :ref:`asp3tecs-id` を参照) を `C_EXP` で囲んで指定します (省略可能)。

  .. tecs:attr:: ATR attribute = C_EXP("TA_NULL")

    アラーム通知属性を `C_EXP` で囲んで指定します (省略可能)。ASP3では指定できる属性はありません [:toppers3-tag:`NGKI3423`] ので、指定できる値は ``C_EXP("TA_NULL")`` のみです [:toppers3-tag:`NGKI3424`]。

  .. tecs:entry:: entry sAlarm eAlarm

    アラーム通知の制御及び状態の取得を行うための受け口です (タスクコンテキスト用)。

  .. tecs:entry:: entry siAlarm eiAlarm

    アラーム通知の制御を行うための受け口です (非タスクコンテキスト用)。

  .. tecs:call:: call siHandlerBody ciHandlerBody

.. tecs:celltype:: tCyclicHandler

  周期通知の生成、制御及び状態の取得を行うコンポーネントです。このセルタイプはハンドラ関数により通知を行う場合に使用します。他の通知方法を使用したい場合、 `tCyclicNotifier` を使用して下さい。

  本コンポーネントは `CRE_CYC` 静的API [:toppers3-tag:`NGKI3727`] により周期通知の生成を行います。

  周期通知は、動作している状態と動作していない状態のいずれかをとり [:toppers3-tag:`NGKI2366`]、動作している状態にすることを動作開始、動作していない状態にすることを動作停止と呼びます。

  周期通知による通知は、基準時刻を基準として、 ``cyclePhase+cyclicTime*(n-1)`` (n=1, 2, ...) で表される時刻に行われます。基準時刻は属性 `TA_PHS` を指定した場合は周期通知の生成がされた時刻、指定されなかった場合は周期通知が最後に動作開始した時刻が用いられます [:toppers3-tag:`NGKI2365`]。

  .. tecs:attr:: ID id = C_EXP("CYCID_$id$")

    周期通知のID番号の識別子 (詳しくは :ref:`asp3tecs-id` を参照) を `C_EXP` で囲んで指定します (省略可能)。

  .. tecs:attr:: ATR attribute = C_EXP("TA_NULL")

    周期通知属性を `C_EXP` で囲んで指定します [:toppers3-tag:`NGKI2370`] (省略可能)。複数個指定する場合、ビット毎の論理和演算子を用いて ``C_EXP("TA_STA | TA_PHS")`` のようにして指定します。

    .. c:macro:: TA_STA

      周期通知の生成時に周期通知を動作開始します。

    .. c:macro:: TA_PHS

      周期通知を生成した時刻を基準時刻とします。

  .. tecs:attr:: RELTIM cycleTime

    周期通知の通知周期をマイクロ秒単位で指定します。

  .. tecs:attr:: RELTIM cyclePhase = 0

    周期通知の通知位相をマイクロ秒単位で指定します (省略可能)。

  .. tecs:entry:: entry sCyclic eCyclic

    周期通知の制御及び状態の取得を行うための受け口です (タスクコンテキスト用)。

    非タスクコンテキスト用の受け口はありません。

  .. tecs:call:: call siHandlerBody ciHandlerBody

シグニチャ
^^^^^^^^^^

.. tecs:signature:: siHandlerBody

  タイムイベントハンドラの本体の呼出しに用いるシグニチャです。

  .. tecs:sigfunction:: void main(void)

    ハンドラの本体です。タイムイベントが発生した際に、カーネルによって呼び出されます。

.. tecs:signature:: sAlarm

  アラーム通知の制御、及び状態の取得を行うためのシグニチャです (タスクコンテキスト用)。

  .. tecs:sigfunction:: ER start([in] RELTIM alarmTime)

    アラーム通知を動作開始します。既に動作している状態である場合、通知時刻の再設定のみが行われます。

    この関数は `sta_alm` サービスコール [:toppers3-tag:`NGKI3543`] のラッパーです。

    :param alarmTime: 通知時刻 (現在時刻からの相対時間, マイクロ秒単位)
    :return: 正常終了 (`E_OK`) またはエラーコード。

  .. tecs:sigfunction:: ER stop(void)

    アラーム通知を動作停止します。動作していない状態である場合、何も行われずに正常終了します。

    この関数は `stp_alm` サービスコール [:toppers3-tag:`NGKI3545`] のラッパーです。

    :return: 正常終了 (`E_OK`) またはエラーコード。

  .. tecs:sigfunction:: ER refer([out]T_RALM *pk_alarmStatus)

    アラーム通知の現在状態を参照します。

    この関数は `ref_alm` サービスコール [:toppers3-tag:`NGKI2572`] のラッパーです。

    :param pk_alarmStatus: アラーム通知の現在状態を入れるメモリ領域へのポインタ
    :return: 正常終了 (`E_OK`) またはエラーコード。

.. tecs:signature:: siAlarm

  アラーム通知の制御、及び状態の取得を行うためのシグニチャです (非タスクコンテキスト用)。

  .. tecs:sigfunction:: ER start([in] RELTIM alarmTime)

    アラーム通知を動作開始します。既に動作している状態である場合、通知時刻の再設定のみが行われます。

    この関数は `ista_alm` サービスコール [:toppers3-tag:`NGKI3543`][:toppers3-tag:`NGKI0562`]  のラッパーです。

    :param alarmTime: 通知時刻 (現在時刻からの相対時間, マイクロ秒単位)
    :return: 正常終了 (`E_OK`) またはエラーコード。

  .. tecs:sigfunction:: ER stop(void)

    アラーム通知を動作停止します。動作していない状態である場合、何も行われずに正常終了します。

    この関数は `istp_alm` サービスコール [:toppers3-tag:`NGKI3545`][:toppers3-tag:`NGKI0562`]  のラッパーです。

    :return: 正常終了 (`E_OK`) またはエラーコード。

.. tecs:signature:: sCyclic

  周期通知の制御、及び状態の取得を行うためのシグニチャです (タスクコンテキスト用)。

  非タスクコンテキスト用のシグニチャはありません。

  .. tecs:sigfunction:: ER start(void)

    周期通知を動作開始します。既に動作している状態である場合、次回通知時刻の再設定のみが行われます。

    この関数は `sta_cyc` サービスコール [:toppers3-tag:`NGKI2431`] のラッパーです。

    :return: 正常終了 (`E_OK`) またはエラーコード。

  .. tecs:sigfunction:: ER stop(void)

    周期通知を動作停止します。動作していない状態である場合、何も行われずに正常終了します。

    この関数は `stp_cyc` サービスコール [:toppers3-tag:`NGKI2455`] のラッパーです。

    :return: 正常終了 (`E_OK`) またはエラーコード。

  .. tecs:sigfunction:: ER refer([out]T_RCYC *pk_cyclicHandlerStatus)

    周期通知の現在状態を参照します。

    この関数は `ref_cyc` サービスコール [:toppers3-tag:`NGKI2463`] のラッパーです。

    :param pk_cyclicHandlerStatus: 周期通知の現在状態を入れるメモリ領域へのポインタ
    :return: 正常終了 (`E_OK`) またはエラーコード。

実装の詳細
----------

.. todo::
    to be filled in
