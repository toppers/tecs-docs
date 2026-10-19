.. _OpaqueRPCPlugin:

OpaqueRPCPlugin プラグインリファレンス
===================================================

名前
-------

  OpaqueRPCPlugin ... Opaque RPC チャンネルを生成するスループラグイン

概要
-------

異なるリージョン (たとえば異なるノードやプロセッサ) にあるセル間の呼び
出しを、RPC (Remote Procedure Call) で中継するチャンネルを生成します。

TransparentRPCPlugin (CDL 上の名前は ``RPCPlugin``) が、一方向チャンネル
を使って引数をマーシャルして送るのに対し、OpaqueRPCPlugin は、クライア
ント側とサーバー側に別のチャンネルセル (既定ではソケット) を生成し、ク
ライアント側のマーシャラと、サーバー側のアンマーシャラおよびサーバータ
スクを自動で配置します。クライアントとサーバーを、別々にビルドされるプ
ログラムとして分けられます。

プラグイン種別
----------------------------

スループラグイン (ThroughPlugin の派生) です。リージョンの ``to_through``
指定子で、クライアント側とサーバー側のリージョンを結ぶ結合に対して使用
するのが基本です。

クライアント側のリージョン (開始リージョン) にクライアント側のセル群が、
サーバー側のリージョン (終了リージョン) にサーバー側のセル群が生成され
ます。

構文
----------------------------

 .. code-block:: tecs-cdl

  [to_through( (サーバー側リージョン), OpaqueRPCPlugin,
               "(オプション)" )]
  region (クライアント側リージョン) {
    ...
  };

リージョンの境界に対して指定する例を示します。

 .. code-block:: tecs-cdl

  [out_through(),
   to_through( rServer, OpaqueRPCPlugin,
      "PPAllocatorSize=1024,"                                 // PPAllocator サイズ (引数の総和)
      "substituteAllocator=%Alloc.eAlloc=>CAlloc.eAlloc%, "   // 代替アロケータ指定 (既定は未指定)
      "clientChannelCell= 'ClientChannel_$destination$', "    // クライアント側チャンネルセル名
      "serverChannelCell= !ServerChannel_$destination$!,  "   // サーバー側チャンネルセル名
      "clientErrorHandler = 'ClientRPCErrorHandler_$destination$.eHandler', "
      "serverErrorHandler = 'ServerRPCErrorHandler_$destination$.eHandler', "
   )]
  region rClient {
    ...
  };

オプション値の中で ``"`` を使えないため、``'...'``, ``!...!``, ``%...%``
で囲んで文字列を指定できます。また ``$count$``, ``$destination$`` などの
置換文字列が使えます (置換の詳細は TBC)。

オプション
----------------------------

オプションが複数ある場合は、','(コンマ)で区切ります。

.. list-table::
   :header-rows: 1
   :widths: 28 22 50

   * - オプション
     - 既定値
     - 説明
   * - ``clientChannelCelltype=celltype``
     - ``tSocketClient``
     - クライアント側チャンネルのセルタイプを指定します。セルタイプ以外を指定するとエラーです。
   * - ``serverChannelCelltype=celltype``
     - ``tSocketServer``
     - サーバー側チャンネルのセルタイプを指定します。セルタイプ以外を指定するとエラーです。
   * - ``clientChannelCell=name``
     - ``(セル名)Client``
     - クライアント側チャンネルのセル名を指定します。
   * - ``serverChannelCell=name``
     - ``(セル名)Server``
     - サーバー側チャンネルのセル名を指定します。サーバー側のアンマーシャラ、タスクのセル名の元にもなります。
   * - ``clientChannelInitializer=...``
     - ``portNo=8931+$count$; serverAddr="127.0.0.1";``
     - クライアント側チャンネルのセルの初期化の記述 (属性の設定) を指定します。
   * - ``serverChannelInitializer=...``
     - ``portNo=8931+$count$;``
     - サーバー側チャンネルのセルの初期化の記述を指定します。
   * - ``clientSemaphoreCelltype=celltype``
     - ``tSemaphore``
     - クライアント側のセマフォのセルタイプを指定します。セルタイプ以外を指定するとエラーです。
   * - ``clientSemaphoreInitializer=...``
     - ``initialCount = 1; attribute = C_EXP( "TA_NULL" );``
     - クライアント側のセマフォの初期化の記述を指定します。
   * - ``noClientSemaphore=true|false``
     - ``false``
     - ``true`` を指定すると、クライアント側のセマフォを生成しません。``true`` と ``false`` 以外はエラーです。
   * - ``clientErrorHandler=cell.entry``
     - (指定なし)
     - クライアント側のエラーハンドラの受け口 (``sRPCErrorHandler`` シグニチャ) を指定します。
   * - ``serverErrorHandler=cell.entry``
     - (指定なし)
     - サーバー側のエラーハンドラの受け口を指定します。
   * - ``TDRCelltype=celltype``
     - ``tNBOTDR``
     - TDR のセルタイプを指定します。セルタイプ以外を指定するとエラーです。
   * - ``PPAllocatorSize=N``
     - (指定なし)
     - 引数の総和のサイズを指定します。``size_is`` 配列の引数があるシグニチャでは必須です (指定しないとエラー)。
   * - ``substituteAllocator=A.e=>B.e,...``
     - (指定なし)
     - クライアント側で指定されたアロケータを、別のアロケータに置き換えます。``セル.受け口=>セル.受け口`` の形式で、コンマで区切って複数指定できます。形式が異なるとエラーです。
   * - ``noServerChannelOpenerCode=true|false``
     - ``false``
     - ``true`` を指定すると、サーバーチャンネルのオープナのコードを生成しません。
   * - ``taskCelltype=celltype``
     - ``tTask``
     - サーバー側タスクのセルタイプを指定します。セルタイプ以外を指定するとエラーです。
   * - ``taskPriority=N``
     - 9
     - サーバー側タスクの優先度を指定します。
   * - ``stackSize=N``
     - 4096
     - サーバー側タスクのスタックサイズを指定します。

生成されるもの
----------------------------

シグニチャのグローバル名を ``sigGlobalName`` とします。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 生成物
     - 説明
   * - コンポジットセルタイプ ``tOpaqueRPCPlugin_(TDR)_(クライアントチャンネル)_sigGlobalName``
     - クライアント側のマーシャラと TDR を含みます。``gen/`` 下に CDL ファイルとして生成されます。
   * - コンポジットセルタイプ ``tOpaqueRPCPlugin_(TDR)_(サーバーチャンネル)_sigGlobalName``
     - サーバー側のアンマーシャラと TDR を含みます。``PPAllocatorSize`` が指定されている場合、PPAllocator のセルを含みます。
   * - クライアント側のセル
     - クライアント側チャンネルのセル、(セマフォのセル)、マーシャラのセル。セマフォは ``noClientSemaphore=true`` で生成されません。
   * - サーバー側のセル
     - サーバー側チャンネルのセル、アンマーシャラのセル、タスクメインのセル、タスクのセル。タスクは起動時に自動で起動されます (``TA_ACT``)。

サーバー側のタスクメインのセルは、サーバーチャンネルのセルタイプが
``sServerChannelOpener`` シグニチャの受け口 ``eOpener`` を持つ場合、
オープナ付きのもの (``tRPCDedicatedTaskMainWithOpener``) になります。持
たない場合、警告 ``O9999`` が出力されます。``noServerChannelOpenerCode=true``
を指定すると、この処理を行いません。

結合先のセルにアロケータ指定がある場合は、クライアント側のマーシャラの
受け口 ``eThroughEntry`` にアロケータ指定が引き継がれます。
``substituteAllocator`` により、アロケータの置き換えができます。

使用方法
----------------------------

クライアント側とサーバー側のリージョンを分け、リージョンの境界を通る結
合に対して ``to_through`` を指定します。クライアント側のリージョンとサー
バー側のリージョンは、別々のリンクユニット (``linkunit``) にできます。

サーバー側のチャンネルの初期化 (ポート番号など) とクライアント側のチャ
ンネルの初期化 (ポート番号、サーバーアドレスなど) は、既定ではソケット
向けの設定になっています。ソケット以外のチャンネルを使う場合は、
``clientChannelCelltype``, ``serverChannelCelltype`` と、それぞれの
``Initializer`` を指定します。

エラー・警告メッセージ
----------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - メッセージ
     - 内容
   * - RPCPlugin: clientChannelCelltype / serverChannelCelltype / taskCelltype / clientSemaphoreCelltype / TDRCelltype
     - 指定したセルタイプが、セルタイプでない、または定義されていない
   * - RPCPlugin: noClientSemaphore / noServerChannelOpenerCode
     - ``true`` と ``false`` 以外を指定した
   * - PPAllocatorSize must be speicified for size_is array
     - ``size_is`` 配列の引数があるのに ``PPAllocatorSize`` がない
   * - syntax error in substituteAllocator option
     - ``substituteAllocator`` の形式が不正
   * - O9999
     - サーバーチャンネルのセルタイプに ``entry sServerChannelOpener eOpener`` がなく、オープナのコードを生成しなかった (警告)

備考、制限事項
-------------------

通信の両端について、次を仮定しています。

 * 呼び元と呼び先で、エンディアンが同じである
 * 呼び元と呼び先で、``char``, ``short``, ``int_t``, ``long_t``, ``intptr_t`` のサイズが同じである
 * 呼び元と呼び先で、有符号型と無符号型のサイズが同じである

関連
----------------------------

 * TransparentRPCPlugin プラグインリファレンス
 * SharedOpaqueRPCPlugin プラグインリファレンス
 * :doc:`Plugin`
