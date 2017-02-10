
.. _asp3tecs-task:

タスク ― `tTask`
=================

タスクはプログラムの並行実行の単位です。

.. todo::
    to be filled in

使用方法
--------

タスクの生成
^^^^^^^^^^^^

アプリケーション開発者は `tTask` セルタイプのセルを生成することにより、タスクを生成することができます。次の例では ``MyTask`` という名前のタスクセルを生成し、 ``MyCell`` の ``eTaskBody`` をメインルーチンとして結合しています。

.. code-block:: tecs-cdl
  :caption: app.cdl

  celltype tMyCellType {
      entry sTaskBody eTaskBody;
  };

  cell tMyCellType MyCell {};

  cell tTask MyTask {
      attribute = C_EXP("TA_ACT");
      stackSize = 1024;
      priority = 42;

      cTaskBody = MyCell.eTaskBody;
  };

.. code-block:: c
  :caption: tMyCellType.c

  void eTaskBody_main(CELLIDX idx)
  {
      CELLCB  *p_cellcb = GET_CELLCB(idx);
      // ...
  }


タスクの制御
^^^^^^^^^^^^

`tTask` が提供する :tecs:entry:`~tTask::eTask` という名前の受け口を利用することにより、タスクの制御及び状態の取得を行うことができます。

.. code-block:: tecs-cdl
  :caption: app.cdl

  cell tTask MyTask {};

  celltype tMyAnotherCellType {
      call sTask cTask;
  };

  cell tMyAnotherCellType MyAnotherCell {
      cTask = MyTask.eTask;
  };

.. code-block:: c
  :caption: tMyAnotherCellType.c

  // タスクの起動
  cTask_activate();

  // タスクの現在状態の参照
  T_RTSK taskStatus;
  cTask_refer(&taskStatus);

なお、非タスクコンテキスト内では、:tecs:entry:`~tTask::eTask` の代わりに :tecs:entry:`~tTask::eiTask` を使用する必要があります。

リファレンス
------------

セルタイプ
^^^^^^^^^^

.. tecs:celltype:: tTask

  タスクの生成、制御及び状態の取得を行うコンポーネントです。

  本コンポーネントは `CRE_TSK` 静的API [:toppers3-tag:`NGKI1023`] によりタスクの生成を行います。静的APIの引数の値には、一部を除き属性値が用いられます。

  .. tecs:attr:: ID id = C_EXP("TSKID_$id$")

    タスクのID番号の識別子 (詳しくは :ref:`asp3tecs-id` を参照) を `C_EXP` で囲んで指定します (省略可能)。

  .. tecs:attr:: ATR attribute = C_EXP("TA_NULL")

    タスク属性 [:toppers3-tag:`NGKI3526`] を `C_EXP` で囲んで指定します (省略可能)。複数個指定する場合、ビット毎の論理和演算子を用いて ``C_EXP("TA_ACT | TA_NOACTQUE")`` のようにして指定します。

    .. c:macro:: TA_ACT

      タスクの生成時にタスクを起動します。

    .. c:macro:: TA_NOACTQUE

      タスクに対する起動要求をキューイングしません。

    .. c:macro:: TA_RSTR

      生成するタスクを制約タスクとします。

      .. attention::

        ASP3 カーネルでは、制約タスクはサポートしません [:toppers3-tag:`ASPS0102`]。
        ただし、制約タスク拡張パッケージを用いることで、制約タスクの機能を追加することができます [:toppers3-tag:`NGKI1022`]。

  .. tecs:attr:: PRI priority

    タスクの起動時優先度を指定します。

  .. tecs:attr:: size_t stackSize

    スタック領域のサイズを指定します (バイト数)。

  .. tecs:entry:: sTask eTask

    タスクの制御及び状態の取得を行うための受け口です。

  .. tecs:entry:: siTask eiTask

    タスクの制御を行うための受け口です (非タスクコンテキスト用)。

  .. tecs:call:: sTaskBody cTaskBody

    タスクの本体として呼び出される受け口をこの呼び口に結合します。

  .. tecs:entry:: siNotificationHandler eiActivateNotificationHandler

    :ref:`タイムイベント通知 <asp3tecs-timeeventnotifier>` の通知方法として「タスクの起動による通知」を用いる場合に結合する受け口です。

  .. tecs:entry:: siNotificationHandler eiWakeUpNotificationHandler

    :ref:`タイムイベント通知 <asp3tecs-timeeventnotifier>` の通知方法として「タスクの起床による通知」を用いる場合に結合する受け口です。

シグニチャ
^^^^^^^^^^

.. tecs:signature:: sTask

  タスクの制御、及び状態の取得を行うためのシグニチャです。

  .. tecs:sigfunction:: ER activate(void)

    タスクに対して起動要求を行います。

    この関数は `act_tsk` サービスコール [:toppers3-tag:`NGKI3529`] のラッパーです。

    :return: 正常終了 (`E_OK`) またはエラーコード。

  .. tecs:sigfunction:: ER_UINT cancelActivate(void)

    タスクに対する処理されていない起動要求をすべてキャンセルし、キャンセルした起動要求の数を返します。

    この関数は `can_act` サービスコール [:toppers3-tag:`NGKI1138`] のラッパーです。

    :return: キューイングされていた起動要求の数 (正の値または0) またはエラーコード。

  .. tecs:sigfunction:: ER getTaskState([out] STAT *p_tskstat)

    タスクの状態を参照します。

    この関数は `get_tst` サービスコール [:toppers3-tag:`NGKI3613`] のラッパーです。

    :param p_tskstat: タスク状態を入れるメモリ領域へのポインタ
    :return: 正常終了 (`E_OK`) またはエラーコード。

  .. tecs:sigfunction:: ER changePriority([in] PRI priority)

    タスクのベース優先度を、 ``priority`` で指定した優先度に変更します。

    この関数は `chg_pri` サービスコール [:toppers3-tag:`NGKI1183`] のラッパーです。

    :param priority: ベース優先度。
    :return: 正常終了 (`E_OK`) またはエラーコード。

  .. tecs:sigfunction:: ER getPriority([out] PRI *p_priority)

    タスクの現在優先度を参照します。

    この関数は `get_pri` サービスコール [:toppers3-tag:`NGKI1202`] のラッパーです。

    :param p_priority: 現在優先度を入れるメモリ領域へのポインタ
    :return: 正常終了 (`E_OK`) またはエラーコード。

  .. tecs:sigfunction:: ER refer([out] T_RTSK *pk_taskStatus)

    タスクの現在状態を参照します。

    この関数は `ref_tsk` サービスコール [:toppers3-tag:`NGKI1217`] のラッパーです。

    :param pk_taskStatus: タスクの現在状態を入れるメモリ領域へのポインタ
    :return: 正常終了 (`E_OK`) またはエラーコード。

  .. tecs:sigfunction:: ER wakeup(void)

    タスクを起床します。

    この関数は `wup_tsk` サービスコール [:toppers3-tag:`NGKI3531`] のラッパーです。

    :return: 正常終了 (`E_OK`) またはエラーコード。

  .. tecs:sigfunction:: ER_UINT cancelWakeup(void)

    タスクに対する処理されていない起床要求をすべてキャンセルし、キャンセルした起床要求の数を返します。

    この関数は `can_wup` サービスコール [:toppers3-tag:`NGKI1276`] のラッパーです。

    :return: キューイングされていた起床要求の数 (正の値または0) またはエラーコード。

  .. tecs:sigfunction:: ER releaseWait(void)

    タスクを強制的に待ち解除します。

    この関数は `rel_wai` サービスコール [:toppers3-tag:`NGKI3532`] のラッパーです。

    :return: 正常終了 (`E_OK`) またはエラーコード。

  .. tecs:sigfunction:: ER suspend(void)

    タスクを強制待ちにします。

    この関数は `sus_tsk` サービスコール [:toppers3-tag:`NGKI1298`] のラッパーです。

    :return: 正常終了 (`E_OK`) またはエラーコード。

  .. tecs:sigfunction:: ER resume(void)

    タスクを強制待ちから再開します。

    この関数は `rsm_tsk` サービスコール [:toppers3-tag:`NGKI1312`] のラッパーです。

    :return: 正常終了 (`E_OK`) またはエラーコード。

  .. tecs:sigfunction:: ER raiseTerminate(void)

    タスクに終了要求を行います。

    この関数は `ras_ter` サービスコール [:toppers3-tag:`NGKI3469`] のラッパーです。

    :return: 正常終了 (`E_OK`) またはエラーコード。

  .. tecs:sigfunction:: ER terminate(void)

    タスクを終了させます。

    この関数は `ter_tsk` サービスコール [:toppers3-tag:`NGKI1170`] のラッパーです。

    :return: 正常終了 (`E_OK`) またはエラーコード。


.. tecs:signature:: siTask

  タスクの制御を行うためのシグニチャです (非タスクコンテキスト用)。

  .. tecs:sigfunction:: ER activate(void)

    タスクに対して起動要求を行います。

    この関数は `iact_tsk` サービスコール [:toppers3-tag:`NGKI3529`][:toppers3-tag:`NGKI0562`] のラッパーです。

    :return: 正常終了 (`E_OK`) またはエラーコード。

  .. tecs:sigfunction:: ER wakeup(void)

    タスクを起床します。

    この関数は `iwup_tsk` サービスコール [:toppers3-tag:`NGKI3531`][:toppers3-tag:`NGKI0562`] のラッパーです。

    :return: 正常終了 (`E_OK`) またはエラーコード。

  .. tecs:sigfunction:: ER releaseWait(void)

    タスクを強制的に待ち解除します。

    この関数は `irel_wai` サービスコール [:toppers3-tag:`NGKI3532`][:toppers3-tag:`NGKI0562`] のラッパーです。

    :return: 正常終了 (`E_OK`) またはエラーコード。


.. tecs:signature:: sTaskBody

  タスクのメインルーチンとして呼び出される受け口に使用するシグニチャです。

  .. tecs:sigfunction:: void main(void)

    タスクのメインルーチンとして呼び出されます。

実装の詳細
----------

タスクの生成
^^^^^^^^^^^^

`tTask` によるタスクの生成は、以下に示しているようなファクトリ記述により静的 API 記述を生成することで実現されています。

.. code-block:: tecs-cdl
  :caption: kernel.cdl (抜粋)

  factory {
      write("tecsgen.cfg",
        "CRE_TSK(%s, { %s, $cbp$, tTask_start, %s, %s, NULL });",
                  id, attribute, priority, stackSize);
  };

最初の ``MyTask`` を用いた例の場合、以下のような静的API記述が生成されます。

.. code-block:: c
  :caption: tecsgen.cfg

  CRE_TSK(TSKID_tTask_MyTask, { TA_ACT, &tTask_CB_tab[0], tTask_start, 42, 1024, NULL });

`tTask` が持つ属性は、 :tecs:attr:`~tTask::id` を除き実行時にはすべて未使用である為、``[omit]`` 指定を行うことでこれらの属性値へのメモリ割り当てが行われないようにしています。

メインルーチン
^^^^^^^^^^^^^^

上で示した静的 API 記述では、メインルーチンとして ``tTask_start`` という名前の関数が指定されています。この関数では以下に示すコードにより TECS への橋渡しを行います。

.. code-block:: c
  :caption: tTask.c

  void
  tTask_start(intptr_t exinf)
  {
      CELLCB  *p_cellcb = (CELLCB *) exinf;

      cTaskBody_main();
  }

サービスコール
^^^^^^^^^^^^^^

:tecs:entry:`~tTask::eTask` 及び :tecs:entry:`~tTask::eiTask` に対する呼出しは、以下に示すような受け口関数により TOPPERS/ASP3 カーネルのサービスコールへの呼出しに変換されます。

.. code-block:: c
  :caption: tTask_inline.h

  Inline ER
  eTask_activate(CELLIDX idx)
  {
      CELLCB  *p_cellcb = GET_CELLCB(idx);
      return(act_tsk(ATTR_id));
  }

