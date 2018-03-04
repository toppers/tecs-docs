
.. _asp3tecs-eventflag:

イベントフラグ ― `tEventflag`
=================

イベントフラグは、イベントの有無をビットごとのフラグで表現することにより、同期を行うためのオブジェクトです。

.. todo::

使用方法
--------

イベントフラグの生成
^^^^^^^^^^^^

アプリケーション開発者は `tEventflag` セルタイプのセルを生成することにより、イベントフラグを生成することができます。次の例では ``MyEventflag`` という名前のイベントフラグセルを生成し、 ``MyCell`` の ``eTaskBody`` をメインルーチンとして結合しています。

.. code-block:: tecs-cdl
  :caption: app.cdl

  celltype tMyCellType {
    call sEventflag cEventflag;
  };

  cell tMyCellType MyCell {
    cEventflag = MyEventflag.eEventflag;
  };

  cell tEventflag MyEventflag {
    attribute = C_EXP("TA_NULL");
    flagPattern = 0;
  };

.. code-block:: c
  :caption: tMyCellType.c

  void eTaskBody_main(CELLIDX idx)
  {
      CELLCB  *p_cellcb = GET_CELLCB(idx);
      // ...
  }

イベントフラグの制御
^^^^^^^^^^^^

todo
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

  // フラグのセット
  FLGPTN setPattern;
  cEventflag_set(setPattern);

  // フラグの現在状態の参照
  T_RFLG *pk_eventflagStatus;
  cEventflag_refer(pk_eventflagStatus);

なお、非タスクコンテキスト内では、:tecs:entry:`~tEventflag::eEventflag` の代わりに
:tecs:entry:`~tEventflag::eiEventflag` を使用する必要があります。

リファレンス
------------

セルタイプ
^^^^^^^^^^

.. tecs:celltype:: tEventflag

  イベントフラグの生成、制御及び状態の取得を行うコンポーネントです。

  本コンポーネントは `CRE_FLG` 静的API [:toppers3-tag:`NGKI1558`] によりイベントフラグの生成を行います。静的APIの引数の値には、一部を除き属性値が用いられます。

  .. tecs:attr:: ID id = C_EXP("FLGID_$id$");

    イベントフラグのID番号の識別子 (詳しくは :ref:`asp3tecs-id` を参照) を `C_EXP` で囲んで指定します (省略可能)。

  .. tecs:attr:: ATR attribute = C_EXP("TA_NULL");

    イベントフラグ属性 [:toppers3-tag:`NGKI1550`] を `C_EXP` で囲んで指定します (省略可能)。

    .. c:macro:: TA_NULL

      デフォルト値（FIFO待ち）。

    .. c:macro:: TA_TPRI

      待ち行列をタスクの優先度順にする。

    .. c:macro:: TA_WMUL

      複数のタスクが待つのを許す。

    .. c:macro:: TA_CLR

      タスクの待ち解除時にイベントフラグをクリアする。

  .. tecs:attr:: FLGPTN　flagPattern

    イベントフラグのビットパターン（符号なし整数）。

  .. tecs:attr:: ACPTN accessPattern[4]

    todo

  .. tecs:entry:: sEventflag eEventflag

    イベントフラグの制御及び状態の取得を行うための受け口です。

  .. tecs:entry:: siEventflag eiEventflag

    イベントフラグの制御を行うための受け口です (非タスクコンテキスト用)。


シグニチャ
^^^^^^^^^^

.. tecs:signature:: sEventflag

  イベントフラグの制御、及び状態の取得を行うためのシグニチャです。

  .. tecs:sigfunction:: ER set([in] FLGPTN setPattern)

    イベントフラグに対して、setPatternで指定されるビットをセットします。サービスコール呼び出し前のビットパターンとsetPatternの値のビット毎の論理和に更新します。

    この関数は `set_flg` サービスコール [:toppers3-tag:`NGKI3534`] のラッパーです。

    :param setPattern: セットするビットパターン。
    :return: 正常終了 (`E_OK`) またはエラーコード。


  .. tecs:sigfunction:: ER clear([in] FLGPTN clearPattern);

    イベントフラグに対して、clearPatternが対応するビットが０になっているビットをクリアします。

    この関数は `clr_flg` サービスコール [:toppers3-tag:`NGKI1611`] のラッパーです。

    :param clearPattern: クリアするビットパターン（ビット毎の反転値）。
    :return: 正常終了 (`E_OK`) またはエラーコード。


  .. tecs:sigfunction:: ER wait([in] FLGPTN waitPattern, [in] MODE waitFlagMode, [out] FLGPTN *p_flagPattern);

    イベントフラグのビットパターンがwaitPatternとWaitFlagModeで指定される待ち解除条件満たすのを待ちます。

    この関数は `wai_flg` サービスコール [:toppers3-tag:`NGKI1618`] のラッパーです。

    :param waitPattern: 待ちビットパターン。
    :param waitFlagMode: 待ちモード。
    :param p_flagPattern: 待ち解除時のビットパターンを入れるメモリ領域へのポインタ。
    :return: 正常終了 (`E_OK`) またはエラーコード。


  .. tecs:sigfunction:: ER waitPolling([in] FLGPTN waitPattern, [in] MODE waitFlagMode, [out] FLGPTN *p_flagPattern);

    イベントフラグのビットパターンがwaitPatternとWaitFlagModeで指定される待ち解除条件満たすのを待ちます（ポーリング）。

    この関数は `pol_flg` サービスコール [:toppers3-tag:`NGKI1619`] のラッパーです。

    :param waitPattern: 待ちビットパターン。
    :param waitFlagMode: 待ちモード。
    :param p_flagPattern: 待ち解除時のビットパターンを入れるメモリ領域へのポインタ。
    :return: 正常終了 (`E_OK`) またはエラーコード。


  .. tecs:sigfunction:: ER waitTimeout([in] FLGPTN waitPattern, [in] MODE waitFlagMode, [out] FLGPTN *p_flagPattern, [in] TMO timeout);

    イベントフラグのビットパターンがwaitPatternとWaitFlagModeで指定される待ち解除条件満たすのを待ちます（タイムアウトあり）。

    この関数は `twai_flg` サービスコール [:toppers3-tag:`NGKI1620`] のラッパーです。

    :param waitPattern: 待ちビットパターン。
    :param waitFlagMode: 待ちモード。
    :param p_flagPattern: 待ち解除時のビットパターンを入れるメモリ領域へのポインタ。
    :param timeout: タイムアウト指定。
    :return: 正常終了 (`E_OK`) またはエラーコード。

  .. tecs:sigfunction:: ER initialize(void);

    対象イベントフラグを再初期化します。対象イベントフラグのビットパターンは初期ビットパターンに初期化されます。

    この関数は `ini_flg` サービスコール [:toppers3-tag:`NGKI1639`] のラッパーです。

    :return: 正常終了 (`E_OK`) またはエラーコード。

  .. tecs:sigfunction:: ER refer([out] T_RFLG *pk_eventflagStatus);

    イベントフラグの現在状態を参照します。

    この関数は `ref_flg` サービスコール [:toppers3-tag:`NGKI1648`] のラッパーです。

    :param pk_eventflagStatus: イベントフラグの現在状態を入れるメモリ領域へのポインタ。
    :return: 正常終了 (`E_OK`) またはエラーコード。

.. tecs:signature:: siEventflag

  イベントフラグの制御を行うためのシグニチャです (非タスクコンテキスト用)。

  .. tecs:sigfunction:: ER set([in] FLGPTN setPattern);

    イベントフラグに対して、setPatternで指定されるビットをセットします。サービスコール呼び出し前のビットパターンとsetPatternの値のビット毎の論理和に更新します。

    この関数は `set_flg` サービスコール [:toppers3-tag:`NGKI3534`] のラッパーです。

    :param setPattern: セットするビットパターン。
    :return: 正常終了 (`E_OK`) またはエラーコード。


実装の詳細
----------

イベントフラグの生成
^^^^^^^^^^^^

`tEventflag` によるイベントフラグの生成は、以下に示しているようなファクトリ記述により静的 API 記述を生成することで実現されています。

.. code-block:: tecs-cdl
  :caption: kernel.cdl (抜粋)

  factory {
      write( "tecsgen.cfg", "CRE_FLG(%s, { %s, %s});",　id, attribute, flagPattern);
  };

最初の ``MyEventflag`` を用いた例の場合、以下のような静的API記述が生成されます。

.. code-block:: c
  :caption: tecsgen.cfg

  CRE_FLG( FLGID_tEventflag_MyEventflag, { TA_NULL, 0 });

`tEventflag` が持つ属性は、 :tecs:attr:`~tEventflag::id` を除き実行時にはすべて未使用である為、``[omit]`` 指定を行うことでこれらの属性値へのメモリ割り当てが行われないようにしています。


サービスコール
^^^^^^^^^^^^^^
:tecs:entry:`~tEventflag::eEventflag` 及び :tecs:entry:`~tEventflag::eiEventflag` に対する呼出しは、以下に示すような受け口関数により TOPPERS/ASP3 カーネルのサービスコールへの呼出しに変換されます。

.. code-block:: c
  :caption: tEventflag_inline.h

  Inline ER
  eEventflag_set(CELLIDX idx)
  {
      CELLCB  *p_cellcb = GET_CELLCB(idx);
      return(set_flg(ATTR_id, FLGPTN setptn));
  }
