
.. _asp3tecs-dataqueue:

データキュー― `tDataqueue`
=================

データキューは、1ワードのデータをメッセージとして、FIFO順で送受信するための同期・通信オブジェクトである。
より大きいサイズのメッセージを送受信したい場合には、メッセージを置いたメモリ領域へのポインタを1ワードのデータとして送受信する方法がある。
データキューは，データキューIDと呼ぶID番号によって識別する[:toppers3-tag:`NGKI1657`]．

.. todo::
    to be filled in

.. 使用方法
  --------

  データキューの生成
  ^^^^^^^^^^^^

  アプリケーション開発者は `tDataqueue` セルタイプのセルを生成することにより、データキューを生成することができます。次の例では ``MyTask`` という名前のタスクセルを生成し、 ``MyCell`` の ``eTaskBody`` をメインルーチンとして結合しています。

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


  データキューの制御
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

      なお、非タスクコンテキスト内では、:tecs:entry:`~tDataqueue::eDataqueue` の代わりに :tecs:entry:`~tDataqueue::eiDataqueue` を使用する必要があります。

リファレンス
------------

セルタイプ
^^^^^^^^^^

.. tecs:celltype:: tDataqueue

  データキューの生成、制御及び状態の取得を行うコンポーネントです。

  本コンポーネントは `CRE_DTQ` 静的API [:toppers3-tag:`NGKI1665`] によりデータキュー    の生成を行います。静的APIの引数の値には、一部を除き属性値が用いられます。

  .. tecs:attr:: ID id = C_EXP("DTQID_$id$");

    データキューのID番号の識別子 (詳しくは :ref:`asp3tecs-id` を参照) を `C_EXP` で囲んで指定します (省略可能)。

  .. tecs:attr:: ATR attribute = C_EXP("TA_NULL")

    タスク属性 [:toppers3-tag:`NGKI3526`] を `C_EXP` で囲んで指定します (省略可能)。

    .. c:macro:: TA_TPRI 

       送信待ち行列をタスクの優先度順にする

    .. c:macro:: TA_NULL

      送信待ち行列はFIFO順になる[:toppers3-tag:`NGKI1662`]。

  .. tecs:attr:: uint_t dataCount = 1;

    データキュー管理領域に格納できるデータ数です。デフォルトは１に設定されます。

  .. tecs:attr:: void *dataqueueManagementBuffer = C_EXP("NULL");

    データキュー管理領域の先頭番地。デフォルトは C_EXP("NULL")に設定されます。
    NULLとした場合，dtqcntで指定した数のデータを格納できるデータキュー管理領域が，
    コンフィギュレータまたはカーネルにより確保される[:toppers3-tag:`NGKI1682`]。

  .. tecs:entry:: sDataqueue eDataqueue

    データキューの制御及び状態の取得を行うための受け口です。

  .. tecs:entry:: siDataqueue eiDataqueue

    データキューの制御を行うための受け口です (非タスクコンテキスト用)。

  .. tecs:entry:: entry siNotificationHandler eiNotificationHandler;

    :ref:`タイムイベント通知 <asp3tecs-timeeventnotifier>` の通知方法として「データキューへの送信による通知」を用いる場合に結合する受け口です。


シグニチャ
^^^^^^^^^^

.. tecs:signature:: sDataqueue

  データキューの制御、及び状態の取得を行うためのシグニチャです。

  .. tecs:sigfunction:: ER send([in] intptr_t data)

    データキューへの送信。

    この関数は `snd_dtq` サービスコール [:toppers3-tag:`NGKI1718`] のラッパーです。

    :param data: 送信データ。
    :return: 正常終了（E_OK）またはエラーコード。

  .. tecs:sigfunction:: ER sendPolling([in] intptr_t data)

    データキューへの送信（ポーリング）。

    この関数は `psnd_dtq` サービスコール [:toppers3-tag:`NGKI3535`] のラッパーです。

    :param data: 送信データ。
    :return: 正常終了（E_OK）またはエラーコード。

  .. tecs:sigfunction:: ER sendTimeout([in] intptr_t data, [in] TMO timeout)

    データキューへの送信（タイムアウト付き）。

    この関数は `tsnd_dtq` サービスコール [:toppers3-tag:`NGKI1721`] のラッパーです。

    :param data: 送信データ。
    :param timeout: タイムアウト時間。
    :return:  またはエラーコード。 

  .. tecs:sigfunction:: ER sendForce([in] intptr_t data)

    データキューへの強制送信。

    この関数は `fsnd_dtq` サービスコール [:toppers3-tag:`NGKI3536`] のラッパーです。

    :param data: 送信データ。
    :return: 正常終了（E_OK）またはエラーコード。

  .. tecs:sigfunction:: ER receive([out] intptr_t *p_data)

    データキューからの受信。

    この関数は `rcv_dtq` サービスコール [:toppers3-tag:`NGKI1751`] のラッパーです。

    :param p_data: 受信データを入れるメモリ領域へのポインタ。
    :return: 正常終了（E_OK）またはエラーコード。

  .. tecs:sigfunction:: ER receivePolling([out] intptr_t *p_data)

    データキューからの受信（ポーリング）。

    この関数は `prcv_dtq` サービスコール [:toppers3-tag:`NGKI1752`] のラッパーです。

    :param p_data: 受信データを入れるメモリ領域へのポインタ。
    :return: 正常終了（E_OK）またはエラーコード。 

  .. tecs:sigfunction:: ER receiveTimeout([out] intptr_t *p_data, [in] TMO timeout)

    データキューからの受信（タイムアウト付き）。

    この関数は `trcv_dtq` サービスコール [:toppers3-tag:`NGKI1753`] のラッパーです。

    :param p_data: 受信データを入れるメモリ領域へのポインタ。。
    :param timeout: 。
    :return: 正常終了（E_OK）またはエラーコード。

  .. tecs:sigfunction:: ER initialize(void)

    データキューの再初期。

    この関数は `ini_dtq` サービスコール [:toppers3-tag:`NGKI1772`] のラッパーです。

    :return:  正常終了（E_OK）またはエラーコード。

  .. tecs:sigfunction:: ER refer([out] T_RDTQ *pk_dataqueueStatus)

    データキューの状態参照。

    この関数は `` サービスコール [:toppers3-tag:`NGKI1781`] のラッパーです。

    :param pk_dataqueueStatus: データキューの現在状態を入れるパケットへのポインタ。
    :return:  正常終了（E_OK）またはエラーコード。


.. tecs:signature:: siDataqueue

  データキューの制御を行うためのシグニチャです (非タスクコンテキスト用)。

  .. tecs:sigfunction:: ER sendPolling([in] intptr_t data);

    タスクに対して起動要求を行います。

    この関数は `iact_tsk` サービスコール [:toppers3-tag:`NGKI3529`][:toppers3-tag:`NGKI0562`] のラッパーです。

    :return: 正常終了 (`E_OK`) またはエラーコード。

  .. tecs:sigfunction:: ER sendForce([in] intptr_t data);

    タスクを起床します。

    この関数は `iwup_tsk` サービスコール [:toppers3-tag:`NGKI3531`][:toppers3-tag:`NGKI0562`] のラッパーです。

    :return: 正常終了 (`E_OK`) またはエラーコード。
    

実装の詳細
----------

データキューの生成
^^^^^^^^^^^^

`tDataqueue` によるデータキューの生成は、以下に示しているようなファクトリ記述により静的 API 記述を生成することで実現されています。

.. code-block:: tecs-cdl
  :caption: kernel.cdl (抜粋)

  factory {
      write("tecsgen.cfg", "CRE_DTQ(%s, { %s, %s, %s });",
            id, attribute, dataCount, dataqueueManagementBuffer);
  };

最初の ``MyDataqueue`` を用いた例の場合、以下のような静的API記述が生成されます。

.. code-block:: c
  :caption: tecsgen.cfg

  CRE_DTQ(DTQID__tDataqueue_Dataqueue, { TA_NULL, 1 ,C_EXP("NULL") });

`tDataqueue` が持つ属性は、 :tecs:attr:`~tCRE_DTQ::id` を除き実行時にはすべて未使用である為、``[omit]`` 指定を行うことでこれらの属性値へのメモリ割り当てが行われないようにしています。


サービスコール
^^^^^^^^^^^^^^

:tecs:entry:`~tDataqueue::eDataqueue` 及び :tecs:entry:`~tDataqueue::eiDataqueue` に対する呼出しは、以下に示すような受け口関数により TOPPERS/ASP3 カーネルのサービスコールへの呼出しに変換されます。


.. code-block:: c
  :caption: tDataqueue_inline.h

  Inline ER
  eDataqueue_send(CELLIDX idx, intptr_t data)
  {
     CELLCB  *p_cellcb = GET_CELLCB(idx);
     return(snd_dtq(ATTR_id, data));
  }
