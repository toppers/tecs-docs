
.. _asp3tecs-semaphore:

セマフォ ― `tSemaphore`
=================

セマフォは、使用されていない資源の有無や数量を数値で表現することにより、その資源を使用する際の排他制御や同期を行うためのオブジェクトである。

.. todo::


使用方法
--------

セマフォの生成
^^^^^^^^^^^^

アプリケーション開発者は `tSemaphore` セルタイプのセルを生成することにより、セマフォを生成することができます。次の例では ``MySemaphore`` という名前のセマフォセルを生成し、 ``MyCell`` の ``eTaskBody`` をメインルーチンとして結合しています。

.. code-block:: tecs-cdl
  :caption: app.cdl

  celltype tMyCellType {
    call sSemaphore cSemaphore;
  };

  cell tMyCellType MyCell {
    cSemaphore = MySemaphore.eSemaphore;
  };

  cell tSemaphore MySemaphore {
    attribute = C_EXP("TA_NULL");
    count = 0;
    max = 1;
  };

.. code-block:: c
  :caption: tMyCellType.c

  void eTaskBody_main(CELLIDX idx)
  {
      CELLCB  *p_cellcb = GET_CELLCB(idx);
      // ...
  }

セマフォの制御
^^^^^^^^^^^^


`tSemaphore` が提供する :tecs:entry:`~tSemaphore::eSemaphore` という名前の受け口を利用することにより、セマフォの制御及び状態の取得を行うことができます。

.. code-block:: tecs-cdl
  :caption: app.cdl

  cell tSemaphore MySemaphore {};

  celltype tMyAnotherCellType {
      call sSemaphore cSemaphore;
  };

  cell tMyAnotherCellType MyAnotherCell {
      cSemaphore = MySemaphore.eSemaphore;
  };

.. code-block:: c
  :caption: tMyAnotherCellType.c

  // セマフォ資源の返却
  cSemaphore_signal();

  // セマフォの現在状態の参照
  T_RSEM *pk_semaphoreStatus;
  cSemaphorek_refer(pk_semaphoreStatus);

なお、非タスクコンテキスト内では、:tecs:entry:`~tSemaphore::eSemaphore` の代わりに
:tecs:entry:`~tSemaphore::eiSemaphore` を使用する必要があります。

リファレンス
------------

セルタイプ
^^^^^^^^^^

.. tecs:celltype:: tSemaphore

  セマフォの生成、制御及び状態の取得を行うコンポーネントです。

  本コンポーネントは `CRE_SEM` 静的API [:toppers3-tag:`NGKI1452`] によりセマフォの生成を行います。静的APIの引数の値には、一部を除き属性値が用いられます。

  .. tecs:attr:: ID id = C_EXP("SEMID_$id$");

    セマフォのID番号の識別子 (詳しくは :ref:`asp3tecs-id` を参照) を `C_EXP` で囲んで指定します (省略可能)。

  .. tecs:attr:: ATR attribute

    セマフォ属性 [:toppers3-tag:`NGKI1448`] を `C_EXP` で囲んで指定します (省略可能)。

    .. c:macro:: TA_NULL

      デフォルト値（FIFO待ち）。

    .. c:macro:: TA_TPRI

      待ち行列をタスクの優先度順にする。

  .. tecs:attr:: uint32_t　count

    セマフォの初期資源数。

  .. tecs:attr:: uint32_t max = 1;

    セマフォの最大資源数。

  .. tecs:entry:: sSemaphore eSemaphore

    セマフォの制御及び状態の取得を行うための受け口です。

  .. tecs:entry:: siSemaphore eiSemaphore

    セマフォの制御を行うための受け口です (非タスクコンテキスト用)。


シグニチャ
^^^^^^^^^^

.. tecs:signature:: sSemaphore

  セマフォの制御、及び状態の取得を行うためのシグニチャです。

  .. tecs:sigfunction:: ER signal(void)

    対象セマフォに資源を返却します。対象セマフォの待ち行列にタスクが存在する場合には、待ち行列の先頭のタスクが待ち解除されます。

    この関数は `sig_sem` サービスコール [:toppers3-tag:`NGKI3533`] のラッパーです。

    :return: 正常終了 (`E_OK`) またはエラーコード。


  .. tecs:sigfunction:: ER wait(void);

    対象セマフォから資源を獲得します。対象セマフォの資源数が１以上の場合には、資源数から１が減ぜられます。

    この関数は `wai_sem` サービスコール [:toppers3-tag:`NGKI1510`] のラッパーです。

    :return: 正常終了 (`E_OK`) またはエラーコード。

  .. tecs:sigfunction:: ER waitPolling(void);

    対象セマフォから資源を獲得します(ポーリング)。対象セマフォの資源数が１以上の場合には、資源数から１が減ぜられます。

    この関数は `pol_sem` サービスコール [:toppers3-tag:`NGKI1511`] のラッパーです。

    :return: 正常終了 (`E_OK`) またはエラーコード。

  .. tecs:sigfunction:: ER waitTimeout([in] TMO timeout);

    対象セマフォから資源を獲得します(タイムアウト付き)。対象セマフォの資源数が１以上の場合には、資源数から１が減ぜられます。

    この関数は `twai_sem` サービスコール [:toppers3-tag:`NGKI1512`] のラッパーです。

    :param timeout: タイムアウト時間
    :return: 正常終了 (`E_OK`) またはエラーコード。

  .. tecs:sigfunction:: ER initialize(void);

    対象セマフォを再初期化します。対象セマフォの資源数は初期資源数に初期化されます。

    この関数は `ini_sem` サービスコール [:toppers3-tag:`NGKI1526`] のラッパーです。

    :return: 正常終了 (`E_OK`) またはエラーコード。

  .. tecs:sigfunction:: ER refer([out] T_RSEM *pk_semaphoreStatus);

    セマフォの現在状態を参照します。

    この関数は `ref_sem` サービスコール [:toppers3-tag:`NGKI1535`] のラッパーです。

    :param pk_semaphoreStatus: セマフォの現在状態を入れるメモリ領域へのポインタ。
    :return: 正常終了 (`E_OK`) またはエラーコード。

.. tecs:signature:: siSemaphore

  セマフォの制御を行うためのシグニチャです (非タスクコンテキスト用)。

  .. tecs:sigfunction:: ER signal();

    この関数は `sig_sem` サービスコール [:toppers3-tag:`NGKI3533`] のラッパーです。

    :return: 正常終了 (`E_OK`) またはエラーコード。


実装の詳細
----------

セマフォの生成
^^^^^^^^^^^^

`tSemaphore` によるセマフォの生成は、以下に示しているようなファクトリ記述により静的 API 記述を生成することで実現されています。

.. code-block:: tecs-cdl
  :caption: kernel.cdl (抜粋)

  factory {
    write( "tecsgen.cfg", "CRE_SEM(%s, { %s, %s, %s });", id, attribute, count, max);
  };

最初の ``MySemaphore`` を用いた例の場合、以下のような静的API記述が生成されます。

.. code-block:: c
  :caption: tecsgen.cfg

  CRE_SEM( SEMID_tSemaphore_MySemaphore, { TA_NULL, 0, 1 });

`tSemaphore` が持つ属性は、 :tecs:attr:`~tSemaphore::id` を除き実行時にはすべて未使用である為、``[omit]`` 指定を行うことでこれらの属性値へのメモリ割り当てが行われないようにしています。


サービスコール
^^^^^^^^^^^^^^
:tecs:entry:`~tSemaphore::eSemaphore` 及び :tecs:entry:`~tSemaphore::eiSemaphore` に対する呼出しは、以下に示すような受け口関数により TOPPERS/ASP3 カーネルのサービスコールへの呼出しに変換されます。

.. code-block:: c
  :caption: tSemaphore_inline.h

  Inline ER
  eSemaphore_signal(CELLIDX idx)
  {
      CELLCB  *p_cellcb = GET_CELLCB(idx);
      return(sig_sem(ATTR_id));
  }
