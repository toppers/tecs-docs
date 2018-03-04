
.. _asp3tecs-initializeroutine:

初期化ルーチン ― `tInitializeRoutine`
=================

初期化ルーチンは、カーネルが実行を制御する処理単位で、カーネルの動作開始の直前に、カーネル非動作状態で実行される [:toppers3-tag:`NGKI1791`]。

.. todo::


使用方法
--------

初期化ルーチンの生成
^^^^^^^^^^^^

アプリケーション開発者は `tInitializeRoutine` セルタイプのセルを生成することにより、初期化ルーチンを生成することができます。次の例では ``MyInitializeRoutine`` という名前の初期化ルーチンセルを生成し、 ``MyCell`` の ``eTaskBody`` をメインルーチンとして結合しています。

.. code-block:: tecs-cdl
  :caption: app.cdl

  celltype tMyCellType {
    call sInitializeRoutineBody cInitializeRoutine;
  };

  cell tMyCellType MyCell {
    cInitializeRoutine = MyInitializeRoutine.eInitializeRoutine;
  };

  cell tInitializeRoutine MyInitializeRoutine {
    attribute = C_EXP("TA_NULL");
  };

.. code-block:: c
  :caption: tMyCellType.c

  void eTaskBody_main(CELLIDX idx)
  {
      CELLCB  *p_cellcb = GET_CELLCB(idx);
      // ...
  }

初期化ルーチンの制御
^^^^^^^^^^^^


`tInitializeRoutine` が提供する :tecs:entry:`~t::eInitializeRoutine` という名前の受け口を利用することにより、初期化ルーチンの制御及び状態の取得を行うことができます。

.. code-block:: tecs-cdl
  :caption: app.cdl

  cell tInitializeRoutine MyInitializeRoutine {};

  celltype tMyAnotherCellType {
      call sInitializeRoutineBody cInitializeRoutine;
  };

  cell tMyAnotherCellType MyAnotherCell {
      cInitializeRoutine = MyInitializeRoutine.eInitializeRoutine;
  };

.. code-block:: c
  :caption: tMyAnotherCellType.c

  // 初期化ルーチン本体
  cInitializeRoutine_main();


なお、非タスクコンテキスト内では、:tecs:entry:`~tInitializeRoutine::eInitializeRoutine` の代わりに
:tecs:entry:`~tInitializeRoutine::eiInitializeRoutine` を使用する必要があります。

リファレンス
------------

セルタイプ
^^^^^^^^^^

.. tecs:celltype:: tInitializeRoutine

  初期化ルーチンの生成、制御及び状態の取得を行うコンポーネントです。

  本コンポーネントは `CRE_PDQ` 静的API [:toppers3-tag:`NGKI1800`] により初期化ルーチンの生成を行います。静的APIの引数の値には、一部を除き属性値が用いられます。

  .. tecs:attr:: ID id = C_EXP("PDQID_$id$");

    初期化ルーチンのID番号の識別子 (詳しくは :ref:`asp3tecs-id` を参照) を `C_EXP` で囲んで指定します (省略可能)。

  .. tecs:attr:: ATR attribute

    初期化ルーチン属性 [:toppers3-tag:`NGKI1795`] を `C_EXP` で囲んで指定します (省略可能)。

    .. c:macro:: TA_NULL

      デフォルト値（FIFO待ち）。

    .. c:macro:: TA_TPRI

      送信待ち行列をタスクの優先度順にする。

  .. tecs:attr:: uint32_t　count = 1;

    初期化ルーチンの容量。

  .. tecs:attr:: PRI maxDataPriority

    初期化ルーチンに送信できるデータ優先度の最大値。

  .. tecs:attr:: void *pdqmb = C_EXP("NULL");

    初期化ルーチン管理領域の先頭番地。

  .. tecs:entry:: sInitializeRoutineBody eInitializeRoutine

    初期化ルーチンの制御及び状態の取得を行うための受け口です。

  .. tecs:entry:: siInitializeRoutine eiInitializeRoutine

    初期化ルーチンの制御を行うための受け口です (非タスクコンテキスト用)。


シグニチャ
^^^^^^^^^^

.. tecs:signature:: sInitializeRoutineBody

  初期化ルーチンの制御、及び状態の取得を行うためのシグニチャです。

  .. tecs:sigfunction:: ER send([in] intptr_t data, [in] PRI dataPriority)

    対象初期化ルーチンに、dataで指定したデータを、dataPriorityで指定した優先度で送信します。対象初期化ルーチンの受信待ち行列にタスクが存在する場合には、受信待ち行列の先頭のタスクが、dataで指定したデータを受信し、待ち解除されます。待ち解除されたタスクに待ち状態となったサービスコールからE_OKが返ります。

    この関数は `snd_pdq` サービスコール [:toppers3-tag:`NGKI1855`] のラッパーです。

    :param data: 送信データ。
    :param dataPriority: 送信データの優先度。
    :return: 正常終了 (`E_OK`) またはエラーコード。

  .. tecs:sigfunction:: ER sendPolling([in] intptr_t data, [in] PRI dataPriority)

    対象初期化ルーチンに、dataで指定したデータを、dataPriorityで指定した優先度で送信します（ポーリング）。対象初期化ルーチンの受信待ち行列にタスクが存在する場合には、受信待ち行列の先頭のタスクが、dataで指定したデータを受信し、待ち解除されます。待ち解除されたタスクに待ち状態となったサービスコールからE_OKが返ります。

    この関数は `psnd_pdq` サービスコール [:toppers3-tag:`NGKI3537`] のラッパーです。

    :param data: 送信データ。
    :param dataPriority: 送信データの優先度。
    :return: 正常終了 (`E_OK`) またはエラーコード。

  .. tecs:sigfunction:: ER sendTimeout([in] intptr_t data, [in] PRI dataPriority, [in] TMO timeout)

    対象初期化ルーチンに、dataで指定したデータを、dataPriorityで指定した優先度で送信します（タイムアウト付き）。対象初期化ルーチンの受信待ち行列にタスクが存在する場合には、受信待ち行列の先頭のタスクが、dataで指定したデータを受信し、待ち解除されます。待ち解除されたタスクに待ち状態となったサービスコールからE_OKが返ります。

    この関数は `tsnd_pdq` サービスコール [:toppers3-tag:`NGKI1858`] のラッパーです。

    :param data: 送信データ。
    :param dataPriority: 送信データの優先度。
    :param timeout: タイムアウト時間。
    :return: 正常終了 (`E_OK`) またはエラーコード。

  .. tecs:sigfunction:: ER receive([out] intptr_t *p_data, [in] PRI *p_dataPriority)

    対象初期化ルーチンからデータを受信します。データの受信に成功した場合、受信したデータはp_dataが指すメモリ領域に、その優先度はp_dataPriorityが指すメモリ領域に返されます。

    この関数は `rcv_pdq` サービスコール [:toppers3-tag:`NGKI1877`] のラッパーです。

    :param p_data: 受信データを入れるメモリ領域へのポインタ。
    :param p_dataPriority: 受信データの優先度を入れるメモリ領域へのポインタ。
    :return: 正常終了 (`E_OK`) またはエラーコード。

  .. tecs:sigfunction:: ER receivePolling([out] intptr_t *p_data, [in] PRI *p_dataPriority)

    対象初期化ルーチンからデータを受信します（ポーリング）。データの受信に成功した場合、受信したデータはp_dataが指すメモリ領域に、その優先度はp_dataPriorityが指すメモリ領域に返されます。

    この関数は `prcv_pdq` サービスコール [:toppers3-tag:`NGKI1878`] のラッパーです。

    :param p_data: 受信データを入れるメモリ領域へのポインタ。
    :param p_dataPriority: 受信データの優先度を入れるメモリ領域へのポインタ。
    :return: 正常終了 (`E_OK`) またはエラーコード。

  .. tecs:sigfunction:: ER receiveTimeout([out] intptr_t *p_data, [in] PRI *p_dataPriority, [in] TMO timeout)

    対象初期化ルーチンからデータを受信します（タイムアウト付き）。データの受信に成功した場合、受信したデータはp_dataが指すメモリ領域に、その優先度はp_dataPriorityが指すメモリ領域に返されます。

    この関数は `trcv_pdq` サービスコール [:toppers3-tag:`NGKI1879`] のラッパーです。

    :param p_data: 受信データを入れるメモリ領域へのポインタ。
    :param p_dataPriority: 受信データの優先度を入れるメモリ領域へのポインタ。
    :param timeout: タイムアウト時間。
    :return: 正常終了 (`E_OK`) またはエラーコード。

  .. tecs:sigfunction:: ER initialize(void);

    対象初期化ルーチンを再初期化します。対象初期化ルーチンの初期化ルーチン管理領域は、格納されているデータがない状態に初期化されます。

    この関数は `ini_pdq` サービスコール [:toppers3-tag:`NGKI1902`] のラッパーです。

    :return: 正常終了 (`E_OK`) またはエラーコード。

  .. tecs:sigfunction:: ER refer([out] T_RSEM *pk_initializeRoutineStatus);

    初期化ルーチンの現在状態を参照します。

    この関数は `ref_pdq` サービスコール [:toppers3-tag:`NGKI1911`] のラッパーです。

    :param pk_initializeRoutineStatus: 初期化ルーチンの現在状態を入れるメモリ領域へのポインタ。
    :return: 正常終了 (`E_OK`) またはエラーコード。

.. tecs:signature:: siInitializeRoutine

  初期化ルーチンの制御を行うためのシグニチャです (非タスクコンテキスト用)。

  .. tecs:sigfunction:: ER sendPolling([in]intptr_t data, [in] PRI dataPriority);

    この関数は `snd_pdq` サービスコール [:toppers3-tag:`NGKI1855`] のラッパーです。

    :return: 正常終了 (`E_OK`) またはエラーコード。


実装の詳細
----------

初期化ルーチンの生成
^^^^^^^^^^^^

`tInitializeRoutine` による初期化ルーチンの生成は、以下に示しているようなファクトリ記述により静的 API 記述を生成することで実現されています。

.. code-block:: tecs-cdl
  :caption: kernel.cdl (抜粋)

  factory {
  		write( "tecsgen.cfg", "CRE_PDQ( %s, { %s, %s, %s, %s} );",
  			   id, attribute, count, maxDataPriority, pdqmb);
  };

最初の ``MyInitializeRoutine`` を用いた例の場合、以下のような静的API記述が生成されます。

.. code-block:: c
  :caption: tecsgen.cfg

  CRE_PDQ( PDQID_tInitializeRoutine_MyInitializeRoutine, { TA_NULL, 1, TMAX_DPRI, NULL });

`tInitializeRoutine` が持つ属性は、 :tecs:attr:`~tInitializeRoutine::id` を除き実行時にはすべて未使用である為、``[omit]`` 指定を行うことでこれらの属性値へのメモリ割り当てが行われないようにしています。


サービスコール
^^^^^^^^^^^^^^
:tecs:entry:`~tInitializeRoutine::eInitializeRoutine` 及び :tecs:entry:`~tInitializeRoutine::eiInitializeRoutine` に対する呼出しは、以下に示すような受け口関数により TOPPERS/ASP3 カーネルのサービスコールへの呼出しに変換されます。

.. code-block:: c
  :caption: tInitializeRoutine_inline.h

  Inline ER
  eInitializeRoutine_send(CELLIDX idx)
  {
      CELLCB  *p_cellcb = GET_CELLCB(idx);
      return(snd_pdq(ATTR_id));
  }
