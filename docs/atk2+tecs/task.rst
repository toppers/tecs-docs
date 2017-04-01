
.. _atk2+tecs-task:

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

  cell tMyCellType MyCell {};

  cell tMyAnotherCellType MyAnotherCell {
      cTask = MyTask.eTask;
  };

.. code-block:: c
  :caption: tMyAnotherCellType.c

  // タスクの起動
  cTask_activate();

  // タスクの現在状態の参照
  TaskRefType　taskStatus;
  cTask_getState(&taskStatus);

リファレンス
------------

セルタイプ
^^^^^^^^^^

.. tecs:celltype:: tTask

  タスクの生成、制御及び状態の取得を行うコンポーネントです。

  .. tecs:attr:: TaskType idx = C_EXP("$cell$")

    タスクのIDの識別子を指定します。

    指定しない場合、 セルの名前が使用されます。

  .. tecs:attr:: bool_t autoStart

    タスクを自動起動させるか指定します。

    .. c:macro:: True

      タスクを自動起動します。

    .. c:macro:: False

      タスクを自動起動しません。

  .. tecs:attr:: char_t *appMode[]

    タスクの自動起動を設定した場合、appMode[]で指定したappModeでタスクを自動起動させる（複数選択可能）。　　

  .. tecs:attr:: uint32_t priority

    タスクの起動時優先度を指定します。

  .. tecs:attr:: uint32_t activation
    
    タスクの最大起動要求回数を指定します。

  .. tecs:attr:: char_t *schedule
    
    タスクのスケジューリングポリシを指定します。

    .. c:macro:: Full

      フルプリエンプティブスケジューリング

    .. c:macro:: Non

      ノンプリエンプティブスケジューリング 

  .. tecs:attr:: char_t *event[]

    タスクの持つイベントを指定します（複数指定可能）。

  .. tecs:attr:: char_t *resource[]

    タスクが獲得するリソースを指定します（複数選択可能）。

  .. tecs:attr:: uint32_t stackSize

    タスク用のスタックサイズを指定します。

  .. tecs:entry:: sTask eTask

    タスクの制御及び状態の取得を行うための受け口です。

  .. tecs:call:: sTaskBody cBody

    タスクの本体として呼び出される受け口をこの呼び口に結合します。

  .. tecs:entry:: sTaskISR2 eTaskISR2

  .. tecs:entry:: sTaskHook eTaskHook

  .. tecs:entry:: sTaskEvent eTaskEvent


    
シグニチャ
^^^^^^^^^^

.. tecs:signature:: sTask

  タスクの制御、及び状態の取得を行うためのシグニチャです。

    .. tecs:sigfunction:: StatusType activate(void)
    タスクに対して起動要求を行います。
    この関数は `ActivateTask(TalskType TaskID）` のラッパーです。
    :return: 正常終了 (`E_OK`) またはエラーコード。

    .. tecs:sigfunction:: StatusType terminate(void)
    タスクを終了します。
    この関数は `TermmateTask(void）` のラッパーです。
    :return: 正常終了 (`E_OK`) またはエラーコード。

  .. tecs:sigfunction:: StatusType chain(void)
    自タスクを終了し、指定したタスクを起動します。 todo
    この関数は `ChainTask(TaskType TaskID）` のラッパーです。
    :return: 正常終了 (`E_OK`) またはエラーコード。

  .. tecs:sigfunction:: StatusType getId([out] TaskRefType p_tskid)
    実行中のタスクIDを取得します。
    結果はp_tskidに格納されます。
    :return: 正常終了 (`E_OK`) またはエラーコード。
    この関数は `GetTasklD(TaskRefType TasklD）` のラッパーです。

  .. tecs:sigfunction:: StatusType getState([out] TaskStateRefType p_state)
    タスクの状態を取得します。
    結果はp_stateに格納されます。
    :return: 正常終了 (`E_OK`) またはエラーコード。
    この関数は `GetTaskState(TaskType TaskID,TaskStateRefType State）` のラッパーです。


.. tecs:signature:: sTaskISR2
  タスクを操作するためのシグニチャISR2用

  .. tecs:sigfunction:: StatusType activate(void)
    タスクに対して起動要求を行います。
    この関数は `ActivateTask(TalskType TaskID）` のラッパーです。
    :return: 正常終了 (`E_OK`) またはエラーコード。 

  .. tecs:sigfunction:: StatusType getId(out] TaskRefType p_tskid)
    実行中のタスクIDを取得します。
    結果はp_tskidに格納されます。
    :return: 正常終了 (`E_OK`) またはエラーコード。
    この関数は `GetTasklD(TaskRefType TasklD）` のラッパーです。


  .. tecs:sigfunction:: StatusType getState([out] TaskStateRefType p_state)
    タスクの状態を取得します。
    結果はp_stateに格納されます。
    :return: 正常終了 (`E_OK`) またはエラーコード。
    この関数は `GetTaskState(TaskType TaskID,TaskStateRefType State）` のラッパーです。




.. tecs:signature:: sTaskHook
  タスクを操作するためのシグニチャ各Hook用

  .. tecs:sigfunction:: StatusType getId(out] TaskRefType p_tskid)
    実行中のタスクIDを取得します。
    結果はp_tskidに格納されます。
    :return: 正常終了 (`E_OK`) またはエラーコード。
    この関数は `GetTasklD(TaskRefType TasklD）` のラッパーです。


  .. tecs:sigfunction:: StatusType getState([out] TaskStateRefType p_state)
    タスクの状態を取得します。
    結果はp_stateに格納されます。
    :return: 正常終了 (`E_OK`) またはエラーコード。
    この関数は `GetTaskState(TaskType TaskID,TaskStateRefType State）` のラッパーです。


.. tecs:signature:: sEventTask
  イベントを操作するためのシグニチャ（Task用）

  .. tecs:sigfunction:: StatusType set([in] EventMaskType mask)
    TaskID で指定されたタスクに Mask で指定されたイベントを設定する。
    :return: 正常終了 (`E_OK`) またはエラーコード。

  .. tecs:sigfunction:: StatusType clear([in] EventMaskType mask)
    Mask で指定されたイベントをクリアする。
    :return: 正常終了 (`E_OK`) またはエラーコード。

  .. tecs:sigfunction:: StatusType get([out] EventMaskRefType p_mask)
    TaskID で指定されたタスクが保持しているイベントマスク値を取得する。
    :return: 正常終了 (`E_OK`) またはエラーコード。

  .. tecs:sigfunction:: StatusType wait([in] EventMaskType mask)
    本関数を呼び出したタスクを待ち状態とする。
    :return: 正常終了 (`E_OK`) またはエラーコード。


.. tecs:signature:: sTaskEvent
  イベントを操作するためのシグニチャTask用

  .. tecs:sigfunction:: StatusType set([in] TaskType tskid, [in] EventMaskType mask)
    TaskID で指定されたタスクに Mask で指定されたイベントを設定する。
    :return: 正常終了 (`E_OK`) またはエラーコード。

  .. tecs:sigfunction:: StatusType get([in] TaskType tskid, [out] EventMaskRefType p_mask)
    TaskID で指定されたタスクが保持しているイベントマスク値を取得する。
    :return: 正常終了 (`E_OK`) またはエラーコード。

