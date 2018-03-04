
.. _asp3tecs-isr:

割込みサブルーチン ― `tISR`
=================

割込みサブルーチンは、カーネルが実行を制御する処理単位である。割込みサブルーチンは，割込みサブルーチンIDと呼ぶID番号によって識別する [:toppers3-tag:`NGKI2947`]。

.. todo::


使用方法
--------

割込みサブルーチンの生成
^^^^^^^^^^^^

アプリケーション開発者は `tISR` セルタイプのセルを生成することにより、割込みサブルーチンを生成することができます。次の例では ``MyISR`` という名前の割込みサブルーチンセルを生成し、 ``MyCell`` の ``eTaskBody`` をメインルーチンとして結合しています。

.. code-block:: tecs-cdl
  :caption: app.cdl

  celltype tMyCellType {
    call siHandlerBody ciBody;
  };

  cell tMyCellType MyCell {
    ciBody = MyISR.eISR;
  };

  cell tISR MyISR {
    attribute = C_EXP( "TA_NULL" );
    interruptNumber = TODO;
    priority = 1;
  };

.. code-block:: c
  :caption: tMyCellType.c

  void eTaskBody_main(CELLIDX idx)
  {
      CELLCB  *p_cellcb = GET_CELLCB(idx);
      // ...
  }

割込みサブルーチンの制御
^^^^^^^^^^^^


`tISR` が提供する :tecs:entry:`~t::eISR` という名前の受け口を利用することにより、割込みサブルーチンの制御及び状態の取得を行うことができます。

.. code-block:: tecs-cdl
  :caption: app.cdl

  cell tISR MyISR {};

  celltype tMyAnotherCellType {
      call siHandlerBody ciBody;
  };

  cell tMyAnotherCellType MyAnotherCell {
      ciBody = MyISR.eISR;
  };

.. code-block:: c
  :caption: tMyAnotherCellType.c

  // 割込みの許可
  ciBody_enable();

  // 割込みの禁止
  ciBody_disable();

なお、非タスクコンテキスト内では、:tecs:entry:`~tISR::eISR` の代わりに
:tecs:entry:`~tISR::eiISR` を使用する必要があります。

リファレンス
------------

セルタイプ
^^^^^^^^^^

.. tecs:celltype:: tISR

  割込みサブルーチンの生成、制御及び状態の取得を行うコンポーネントです。

  本コンポーネントは `CRE_PDQ` 静的API [:toppers3-tag:`NGKI1800`] により割込みサブルーチンの生成を行います。静的APIの引数の値には、一部を除き属性値が用いられます。

  .. tecs:attr:: ID id = C_EXP("PDQID_$id$");

    割込みサブルーチンのID番号の識別子 (詳しくは :ref:`asp3tecs-id` を参照) を `C_EXP` で囲んで指定します (省略可能)。

  .. tecs:attr:: ATR attribute

    割込みサブルーチン属性 [:toppers3-tag:`NGKI1795`] を `C_EXP` で囲んで指定します (省略可能)。

    .. c:macro:: TA_NULL

      デフォルト値（FIFO待ち）。

    .. c:macro:: TA_TPRI

      送信待ち行列をタスクの優先度順にする。

  .. tecs:attr:: uint32_t　count = 1;

    割込みサブルーチンの容量。

  .. tecs:attr:: PRI maxDataPriority

    割込みサブルーチンに送信できるデータ優先度の最大値。

  .. tecs:attr:: void *pdqmb = C_EXP("NULL");

    割込みサブルーチン管理領域の先頭番地。

  .. tecs:entry:: siHandlerBody eISR

    割込みサブルーチンの制御及び状態の取得を行うための受け口です。

  .. tecs:entry:: siISR eiISR

    割込みサブルーチンの制御を行うための受け口です (非タスクコンテキスト用)。


シグニチャ
^^^^^^^^^^

.. tecs:signature:: siHandlerBody

  割込みサブルーチンの制御、及び状態の取得を行うためのシグニチャです。

  .. tecs:sigfunction:: ER send([in] intptr_t data, [in] PRI dataPriority)

    対象割込みサブルーチンに、dataで指定したデータを、dataPriorityで指定した優先度で送信します。対象割込みサブルーチンの受信待ち行列にタスクが存在する場合には、受信待ち行列の先頭のタスクが、dataで指定したデータを受信し、待ち解除されます。待ち解除されたタスクに待ち状態となったサービスコールからE_OKが返ります。

    この関数は `snd_pdq` サービスコール [:toppers3-tag:`NGKI1855`] のラッパーです。

    :param data: 送信データ。
    :param dataPriority: 送信データの優先度。
    :return: 正常終了 (`E_OK`) またはエラーコード。

  .. tecs:sigfunction:: ER sendPolling([in] intptr_t data, [in] PRI dataPriority)

    対象割込みサブルーチンに、dataで指定したデータを、dataPriorityで指定した優先度で送信します（ポーリング）。対象割込みサブルーチンの受信待ち行列にタスクが存在する場合には、受信待ち行列の先頭のタスクが、dataで指定したデータを受信し、待ち解除されます。待ち解除されたタスクに待ち状態となったサービスコールからE_OKが返ります。

    この関数は `psnd_pdq` サービスコール [:toppers3-tag:`NGKI3537`] のラッパーです。

    :param data: 送信データ。
    :param dataPriority: 送信データの優先度。
    :return: 正常終了 (`E_OK`) またはエラーコード。

  .. tecs:sigfunction:: ER sendTimeout([in] intptr_t data, [in] PRI dataPriority, [in] TMO timeout)

    対象割込みサブルーチンに、dataで指定したデータを、dataPriorityで指定した優先度で送信します（タイムアウト付き）。対象割込みサブルーチンの受信待ち行列にタスクが存在する場合には、受信待ち行列の先頭のタスクが、dataで指定したデータを受信し、待ち解除されます。待ち解除されたタスクに待ち状態となったサービスコールからE_OKが返ります。

    この関数は `tsnd_pdq` サービスコール [:toppers3-tag:`NGKI1858`] のラッパーです。

    :param data: 送信データ。
    :param dataPriority: 送信データの優先度。
    :param timeout: タイムアウト時間。
    :return: 正常終了 (`E_OK`) またはエラーコード。

  .. tecs:sigfunction:: ER receive([out] intptr_t *p_data, [in] PRI *p_dataPriority)

    対象割込みサブルーチンからデータを受信します。データの受信に成功した場合、受信したデータはp_dataが指すメモリ領域に、その優先度はp_dataPriorityが指すメモリ領域に返されます。

    この関数は `rcv_pdq` サービスコール [:toppers3-tag:`NGKI1877`] のラッパーです。

    :param p_data: 受信データを入れるメモリ領域へのポインタ。
    :param p_dataPriority: 受信データの優先度を入れるメモリ領域へのポインタ。
    :return: 正常終了 (`E_OK`) またはエラーコード。

  .. tecs:sigfunction:: ER receivePolling([out] intptr_t *p_data, [in] PRI *p_dataPriority)

    対象割込みサブルーチンからデータを受信します（ポーリング）。データの受信に成功した場合、受信したデータはp_dataが指すメモリ領域に、その優先度はp_dataPriorityが指すメモリ領域に返されます。

    この関数は `prcv_pdq` サービスコール [:toppers3-tag:`NGKI1878`] のラッパーです。

    :param p_data: 受信データを入れるメモリ領域へのポインタ。
    :param p_dataPriority: 受信データの優先度を入れるメモリ領域へのポインタ。
    :return: 正常終了 (`E_OK`) またはエラーコード。

  .. tecs:sigfunction:: ER receiveTimeout([out] intptr_t *p_data, [in] PRI *p_dataPriority, [in] TMO timeout)

    対象割込みサブルーチンからデータを受信します（タイムアウト付き）。データの受信に成功した場合、受信したデータはp_dataが指すメモリ領域に、その優先度はp_dataPriorityが指すメモリ領域に返されます。

    この関数は `trcv_pdq` サービスコール [:toppers3-tag:`NGKI1879`] のラッパーです。

    :param p_data: 受信データを入れるメモリ領域へのポインタ。
    :param p_dataPriority: 受信データの優先度を入れるメモリ領域へのポインタ。
    :param timeout: タイムアウト時間。
    :return: 正常終了 (`E_OK`) またはエラーコード。

  .. tecs:sigfunction:: ER initialize(void);

    対象割込みサブルーチンを再割込みサブします。対象割込みサブルーチンの割込みサブルーチン管理領域は、格納されているデータがない状態に割込みサブされます。

    この関数は `ini_pdq` サービスコール [:toppers3-tag:`NGKI1902`] のラッパーです。

    :return: 正常終了 (`E_OK`) またはエラーコード。

  .. tecs:sigfunction:: ER refer([out] T_RSEM *pk_isrStatus);

    割込みサブルーチンの現在状態を参照します。

    この関数は `ref_pdq` サービスコール [:toppers3-tag:`NGKI1911`] のラッパーです。

    :param pk_isrStatus: 割込みサブルーチンの現在状態を入れるメモリ領域へのポインタ。
    :return: 正常終了 (`E_OK`) またはエラーコード。

.. tecs:signature:: siISR

  割込みサブルーチンの制御を行うためのシグニチャです (非タスクコンテキスト用)。

  .. tecs:sigfunction:: ER sendPolling([in]intptr_t data, [in] PRI dataPriority);

    この関数は `snd_pdq` サービスコール [:toppers3-tag:`NGKI1855`] のラッパーです。

    :return: 正常終了 (`E_OK`) またはエラーコード。


実装の詳細
----------

割込みサブルーチンの生成
^^^^^^^^^^^^

`tISR` による割込みサブルーチンの生成は、以下に示しているようなファクトリ記述により静的 API 記述を生成することで実現されています。

.. code-block:: tecs-cdl
  :caption: kernel.cdl (抜粋)

  factory {
  		write( "tecsgen.cfg", "CRE_PDQ( %s, { %s, %s, %s, %s} );",
  			   id, attribute, count, maxDataPriority, pdqmb);
  };

最初の ``MyISR`` を用いた例の場合、以下のような静的API記述が生成されます。

.. code-block:: c
  :caption: tecsgen.cfg

  CRE_PDQ( PDQID_tISR_MyISR, { TA_NULL, 1, TMAX_DPRI, NULL });

`tISR` が持つ属性は、 :tecs:attr:`~tISR::id` を除き実行時にはすべて未使用である為、``[omit]`` 指定を行うことでこれらの属性値へのメモリ割り当てが行われないようにしています。


サービスコール
^^^^^^^^^^^^^^
:tecs:entry:`~tISR::eISR` 及び :tecs:entry:`~tISR::eiISR` に対する呼出しは、以下に示すような受け口関数により TOPPERS/ASP3 カーネルのサービスコールへの呼出しに変換されます。

.. code-block:: c
  :caption: tISR_inline.h

  Inline ER
  eISR_send(CELLIDX idx)
  {
      CELLCB  *p_cellcb = GET_CELLCB(idx);
      return(snd_pdq(ATTR_id));
  }
