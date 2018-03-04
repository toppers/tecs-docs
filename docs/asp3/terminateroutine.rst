
.. _asp3tecs-terminateroutine:

終了処理ルーチン ― `tTerminateRoutine`
=================

終了処理ルーチンは、１ワードのデータをメッセージとして、データの優先度順で送受信するための同期・通信カーネルオブジェクトである。より大きいサイズのメッセージを送受信したい場合には、メッセージを置いたメモリ領域へのポインタを1ワードのデータとして送受信する方法がある。終了処理ルーチンは，終了処理ルーチンIDと呼ぶID番号によって識別する [:toppers3-tag:`NGKI1791`]。

.. todo::


使用方法
--------

終了処理ルーチンの生成
^^^^^^^^^^^^

アプリケーション開発者は `tTerminateRoutine` セルタイプのセルを生成することにより、終了処理ルーチンを生成することができます。次の例では ``MyTerminateRoutine`` という名前の終了処理ルーチンセルを生成し、 ``MyCell`` の ``eTaskBody`` をメインルーチンとして結合しています。

.. code-block:: tecs-cdl
  :caption: app.cdl

  celltype tMyCellType {
    call sTerminateRoutine cTerminateRoutine;
  };

  cell tMyCellType MyCell {
    cTerminateRoutine = MyTerminateRoutine.eTerminateRoutine;
  };

  cell tTerminateRoutine MyTerminateRoutine {
    attribute = C_EXP("TA_NULL");
    count = 1;
    maxDataPriority = C_EXP("TMAX_DPRI");
    pdqmb = C_EXP( "NULL" );
  };

.. code-block:: c
  :caption: tMyCellType.c

  void eTaskBody_main(CELLIDX idx)
  {
      CELLCB  *p_cellcb = GET_CELLCB(idx);
      // ...
  }

終了処理ルーチンの制御
^^^^^^^^^^^^


`tTerminateRoutine` が提供する :tecs:entry:`~t::eTerminateRoutine` という名前の受け口を利用することにより、終了処理ルーチンの制御及び状態の取得を行うことができます。

.. code-block:: tecs-cdl
  :caption: app.cdl

  cell tTerminateRoutine MyTerminateRoutine {};

  celltype tMyAnotherCellType {
      call sTerminateRoutine cTerminateRoutine;
  };

  cell tMyAnotherCellType MyAnotherCell {
      cTerminateRoutine = MyTerminateRoutine.eTerminateRoutine;
  };

.. code-block:: c
  :caption: tMyAnotherCellType.c

  // 終了処理ルーチンの送信
  intptr_t data;
  PRI dataPriority;
  cTerminateRoutine_send( data, dataPriority );

  // 終了処理ルーチンの受信
  intptr_t *p_data;
  PRI *p_dataPriority;
  cTerminateRoutine_receive( p_data, p_dataPriority );

なお、非タスクコンテキスト内では、:tecs:entry:`~tTerminateRoutine::eTerminateRoutine` の代わりに
:tecs:entry:`~tTerminateRoutine::eiTerminateRoutine` を使用する必要があります。

リファレンス
------------

セルタイプ
^^^^^^^^^^

.. tecs:celltype:: tTerminateRoutine

  終了処理ルーチンの生成、制御及び状態の取得を行うコンポーネントです。

  本コンポーネントは `CRE_PDQ` 静的API [:toppers3-tag:`NGKI1800`] により終了処理ルーチンの生成を行います。静的APIの引数の値には、一部を除き属性値が用いられます。

  .. tecs:attr:: ID id = C_EXP("PDQID_$id$");

    終了処理ルーチンのID番号の識別子 (詳しくは :ref:`asp3tecs-id` を参照) を `C_EXP` で囲んで指定します (省略可能)。

  .. tecs:attr:: ATR attribute

    終了処理ルーチン属性 [:toppers3-tag:`NGKI1795`] を `C_EXP` で囲んで指定します (省略可能)。

    .. c:macro:: TA_NULL

      デフォルト値（FIFO待ち）。

    .. c:macro:: TA_TPRI

      送信待ち行列をタスクの優先度順にする。

  .. tecs:attr:: uint32_t　count = 1;

    終了処理ルーチンの容量。

  .. tecs:attr:: PRI maxDataPriority

    終了処理ルーチンに送信できるデータ優先度の最大値。

  .. tecs:attr:: void *pdqmb = C_EXP("NULL");

    終了処理ルーチン管理領域の先頭番地。

  .. tecs:entry:: sTerminateRoutine eTerminateRoutine

    終了処理ルーチンの制御及び状態の取得を行うための受け口です。

  .. tecs:entry:: siTerminateRoutine eiTerminateRoutine

    終了処理ルーチンの制御を行うための受け口です (非タスクコンテキスト用)。


シグニチャ
^^^^^^^^^^

.. tecs:signature:: sTerminateRoutine

  終了処理ルーチンの制御、及び状態の取得を行うためのシグニチャです。

  .. tecs:sigfunction:: ER send([in] intptr_t data, [in] PRI dataPriority)

    対象終了処理ルーチンに、dataで指定したデータを、dataPriorityで指定した優先度で送信します。対象終了処理ルーチンの受信待ち行列にタスクが存在する場合には、受信待ち行列の先頭のタスクが、dataで指定したデータを受信し、待ち解除されます。待ち解除されたタスクに待ち状態となったサービスコールからE_OKが返ります。

    この関数は `snd_pdq` サービスコール [:toppers3-tag:`NGKI1855`] のラッパーです。

    :param data: 送信データ。
    :param dataPriority: 送信データの優先度。
    :return: 正常終了 (`E_OK`) またはエラーコード。

  .. tecs:sigfunction:: ER sendPolling([in] intptr_t data, [in] PRI dataPriority)

    対象終了処理ルーチンに、dataで指定したデータを、dataPriorityで指定した優先度で送信します（ポーリング）。対象終了処理ルーチンの受信待ち行列にタスクが存在する場合には、受信待ち行列の先頭のタスクが、dataで指定したデータを受信し、待ち解除されます。待ち解除されたタスクに待ち状態となったサービスコールからE_OKが返ります。

    この関数は `psnd_pdq` サービスコール [:toppers3-tag:`NGKI3537`] のラッパーです。

    :param data: 送信データ。
    :param dataPriority: 送信データの優先度。
    :return: 正常終了 (`E_OK`) またはエラーコード。

  .. tecs:sigfunction:: ER sendTimeout([in] intptr_t data, [in] PRI dataPriority, [in] TMO timeout)

    対象終了処理ルーチンに、dataで指定したデータを、dataPriorityで指定した優先度で送信します（タイムアウト付き）。対象終了処理ルーチンの受信待ち行列にタスクが存在する場合には、受信待ち行列の先頭のタスクが、dataで指定したデータを受信し、待ち解除されます。待ち解除されたタスクに待ち状態となったサービスコールからE_OKが返ります。

    この関数は `tsnd_pdq` サービスコール [:toppers3-tag:`NGKI1858`] のラッパーです。

    :param data: 送信データ。
    :param dataPriority: 送信データの優先度。
    :param timeout: タイムアウト時間。
    :return: 正常終了 (`E_OK`) またはエラーコード。

  .. tecs:sigfunction:: ER receive([out] intptr_t *p_data, [in] PRI *p_dataPriority)

    対象終了処理ルーチンからデータを受信します。データの受信に成功した場合、受信したデータはp_dataが指すメモリ領域に、その優先度はp_dataPriorityが指すメモリ領域に返されます。

    この関数は `rcv_pdq` サービスコール [:toppers3-tag:`NGKI1877`] のラッパーです。

    :param p_data: 受信データを入れるメモリ領域へのポインタ。
    :param p_dataPriority: 受信データの優先度を入れるメモリ領域へのポインタ。
    :return: 正常終了 (`E_OK`) またはエラーコード。

  .. tecs:sigfunction:: ER receivePolling([out] intptr_t *p_data, [in] PRI *p_dataPriority)

    対象終了処理ルーチンからデータを受信します（ポーリング）。データの受信に成功した場合、受信したデータはp_dataが指すメモリ領域に、その優先度はp_dataPriorityが指すメモリ領域に返されます。

    この関数は `prcv_pdq` サービスコール [:toppers3-tag:`NGKI1878`] のラッパーです。

    :param p_data: 受信データを入れるメモリ領域へのポインタ。
    :param p_dataPriority: 受信データの優先度を入れるメモリ領域へのポインタ。
    :return: 正常終了 (`E_OK`) またはエラーコード。

  .. tecs:sigfunction:: ER receiveTimeout([out] intptr_t *p_data, [in] PRI *p_dataPriority, [in] TMO timeout)

    対象終了処理ルーチンからデータを受信します（タイムアウト付き）。データの受信に成功した場合、受信したデータはp_dataが指すメモリ領域に、その優先度はp_dataPriorityが指すメモリ領域に返されます。

    この関数は `trcv_pdq` サービスコール [:toppers3-tag:`NGKI1879`] のラッパーです。

    :param p_data: 受信データを入れるメモリ領域へのポインタ。
    :param p_dataPriority: 受信データの優先度を入れるメモリ領域へのポインタ。
    :param timeout: タイムアウト時間。
    :return: 正常終了 (`E_OK`) またはエラーコード。

  .. tecs:sigfunction:: ER initialize(void);

    対象終了処理ルーチンを再終了処理します。対象終了処理ルーチンの終了処理ルーチン管理領域は、格納されているデータがない状態に終了処理されます。

    この関数は `ini_pdq` サービスコール [:toppers3-tag:`NGKI1902`] のラッパーです。

    :return: 正常終了 (`E_OK`) またはエラーコード。

  .. tecs:sigfunction:: ER refer([out] T_RSEM *pk_terminateRoutineStatus);

    終了処理ルーチンの現在状態を参照します。

    この関数は `ref_pdq` サービスコール [:toppers3-tag:`NGKI1911`] のラッパーです。

    :param pk_terminateRoutineStatus: 終了処理ルーチンの現在状態を入れるメモリ領域へのポインタ。
    :return: 正常終了 (`E_OK`) またはエラーコード。

.. tecs:signature:: siTerminateRoutine

  終了処理ルーチンの制御を行うためのシグニチャです (非タスクコンテキスト用)。

  .. tecs:sigfunction:: ER sendPolling([in]intptr_t data, [in] PRI dataPriority);

    この関数は `snd_pdq` サービスコール [:toppers3-tag:`NGKI1855`] のラッパーです。

    :return: 正常終了 (`E_OK`) またはエラーコード。


実装の詳細
----------

終了処理ルーチンの生成
^^^^^^^^^^^^

`tTerminateRoutine` による終了処理ルーチンの生成は、以下に示しているようなファクトリ記述により静的 API 記述を生成することで実現されています。

.. code-block:: tecs-cdl
  :caption: kernel.cdl (抜粋)

  factory {
  		write( "tecsgen.cfg", "CRE_PDQ( %s, { %s, %s, %s, %s} );",
  			   id, attribute, count, maxDataPriority, pdqmb);
  };

最初の ``MyTerminateRoutine`` を用いた例の場合、以下のような静的API記述が生成されます。

.. code-block:: c
  :caption: tecsgen.cfg

  CRE_PDQ( PDQID_tTerminateRoutine_MyTerminateRoutine, { TA_NULL, 1, TMAX_DPRI, NULL });

`tTerminateRoutine` が持つ属性は、 :tecs:attr:`~tTerminateRoutine::id` を除き実行時にはすべて未使用である為、``[omit]`` 指定を行うことでこれらの属性値へのメモリ割り当てが行われないようにしています。


サービスコール
^^^^^^^^^^^^^^
:tecs:entry:`~tTerminateRoutine::eTerminateRoutine` 及び :tecs:entry:`~tTerminateRoutine::eiTerminateRoutine` に対する呼出しは、以下に示すような受け口関数により TOPPERS/ASP3 カーネルのサービスコールへの呼出しに変換されます。

.. code-block:: c
  :caption: tTerminateRoutine_inline.h

  Inline ER
  eTerminateRoutine_send(CELLIDX idx)
  {
      CELLCB  *p_cellcb = GET_CELLCB(idx);
      return(snd_pdq(ATTR_id));
  }
