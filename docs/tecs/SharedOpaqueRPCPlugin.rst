.. _SharedOpaqueRPCPlugin:

SharedOpaqueRPCPlugin プラグインリファレンス
===================================================

名前
-------

  SharedOpaqueRPCPlugin ... 複数の結合で 1 本のチャンネルを共有する Opaque RPC プラグイン

概要
-------

OpaqueRPCPlugin と同じく、クライアント側とサーバー側のリージョンにまた
がる呼び出しを RPC で中継します。OpaqueRPCPlugin がシグニチャ(結合)ご
とにチャンネルとサーバータスクを生成するのに対し、SharedOpaqueRPCPlugin
は、``sharedChannelName`` に同じ名前を指定した複数の結合で、1 本の
チャンネルと 1 つのサーバータスクを共有します。

通信の本数とサーバータスクの数を抑えられます。クライアント側では、共有
するチャンネルに対するアクセスが、結合ごとに割り当てられたセマフォで
排他制御されます。

プラグイン種別
----------------------------

スループラグイン (ThroughPlugin の派生) です。リージョンの ``to_through``
指定子で、クライアント側とサーバー側のリージョンを結ぶ結合に対して使用
します。

構文
----------------------------

 .. code-block:: tecs-cdl

  [out_through(),
   to_through( rServer, SharedOpaqueRPCPlugin,
      "taskCelltype=tTask,PPAllocatorSize=1024,"
      "sharedChannelName= \"MyChannel\", "
      "substituteAllocator=\"Alloc.eAlloc=>CAlloc.eAlloc\", "
      "clientChannelCell= \"ClientChannel\", "
      "serverChannelCell= \"ServerChannel\" "
   ), linkunit]
  region rClient {
    ...
  };

オプション
----------------------------

オプションは OpaqueRPCPlugin と共通で、``sharedChannelName`` が加わります。
オプションが複数ある場合は、','(コンマ)で区切ります。

.. list-table::
   :header-rows: 1
   :widths: 28 22 50

   * - オプション
     - 既定値
     - 説明
   * - ``sharedChannelName=name``
     - (必須)
     - 共有するチャンネルの名前を指定します。同じ名前を指定したプラグインのセル群が、1 本のチャンネルを共有します。指定しないとエラーです。
   * - ``clientChannelCelltype=celltype``
     - ``tSocketClient``
     - クライアント側チャンネルのセルタイプを指定します。
   * - ``serverChannelCelltype=celltype``
     - ``tSocketServer``
     - サーバー側チャンネルのセルタイプを指定します。
   * - ``clientChannelCell=name``
     - ``(セル名)Client``
     - クライアント側チャンネルのセル名を指定します。CDL に記述したセルの名前に合わせます。
   * - ``serverChannelCell=name``
     - ``(セル名)Server``
     - サーバー側チャンネルのセル名を指定します。CDL に記述したセルの名前に合わせます。
   * - ``clientChannelInitializer=...``, ``serverChannelInitializer=...``
     - ソケット用の設定
     - チャンネルの初期化の記述です。OpaqueRPCPlugin と共通です。
   * - ``clientSemaphoreCelltype=celltype``, ``clientSemaphoreInitializer=...``
     - ``tSemaphore``, ``initialCount = 1; attribute = C_EXP( "TA_NULL" );``
     - OpaqueRPCPlugin と共通です。
   * - ``clientErrorHandler=...``, ``serverErrorHandler=...``
     - (指定なし)
     - エラーハンドラの受け口を指定します。OpaqueRPCPlugin と共通です。
   * - ``TDRCelltype=celltype``
     - ``tNBOTDR``
     - TDR のセルタイプを指定します。
   * - ``PPAllocatorSize=N``
     - (指定なし)
     - 引数の総和のサイズを指定します。``size_is`` 配列の引数があるシグニチャでは必須です。
   * - ``substituteAllocator=A.e=>B.e,...``
     - (指定なし)
     - アロケータの置き換えを指定します。
   * - ``noServerChannelOpenerCode=true|false``
     - ``false``
     - OpaqueRPCPlugin と共通です。
   * - ``taskCelltype=celltype``, ``taskPriority=N``, ``stackSize=N``
     - ``tTask``, 9, 4096
     - サーバー側タスクの指定です。共有チャンネルでは、最初に現れたプラグインの ``taskPriority`` がサーバー側タスクの優先度になります。

各オプションの詳細は、OpaqueRPCPlugin プラグインリファレンスを参照してください。

生成されるもの
----------------------------

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 生成物
     - 説明
   * - コンポジットセルタイプ ``tSharedOpaqueRPCPluginChannel_tTDR_Client``
     - クライアント側の共有チャンネルです。TDR、セマフォ、共有チャンネル管理 (``tRPCSharedChannelMan``) を含みます。``gen/`` 下に CDL ファイルとして生成されます。
   * - コンポジットセルタイプ ``tSharedOpaqueRPCPluginChannel_tTDR_Server``
     - サーバー側の共有チャンネルです。TDR、タスクメイン (オープナ付き)、タスクを含みます。タスクは起動時に自動で起動されます (``TA_ACT``)。
   * - 共有チャンネルのセル ``(sharedChannelName)``, ``(sharedChannelName)_Server``
     - クライアント側、サーバー側のリージョンに、それぞれ 1 つ生成されます。サーバー側のセルの ``cUnmarshalAndCallFunction`` は、共有する結合ごとのアンマーシャラの受け口が配列として結合されます。
   * - マーシャラのセル
     - クライアント側に、結合ごとに生成されます。共有チャンネルのセルの ``eTDR`` と、結合ごとに割り当てられた ``eSemaphore[N]`` に結合されます。
   * - アンマーシャラのセル ``(セル名)_Server``
     - サーバー側に、結合ごとに生成され、元の結合先の受け口に結合されます。``PPAllocatorSize`` が指定されている場合は ``PPAllocator_(共有チャンネル名)`` のセルも生成されます。

``clientChannelCell``, ``serverChannelCell`` で指定するチャンネルのセル
(たとえば ``tSocketClient``, ``tSocketServer`` のセル) は、プラグインでは
生成されません。CDL に記述しておく必要があります。

使用方法
----------------------------

1. クライアント側のリージョン、サーバー側のリージョンを定義します。
2. それぞれのリージョンに、``clientChannelCell``, ``serverChannelCell``
   で指定する名前のチャンネルのセルを記述します。
3. 共有したい結合のそれぞれに、同じ ``sharedChannelName`` を指定して
   ``to_through`` を指定します。

共有するプラグインは、開始リージョンと終了リージョンが一致している必要
があります。一致しない場合は、エラーになります。

エラー・警告メッセージ
----------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - メッセージ
     - 内容
   * - 'sharedChannelName' option: mandatory
     - ``sharedChannelName`` が指定されていない
   * - SharedRPCPlugin: start region mismatch
     - 同じチャンネルを共有するプラグインで、開始リージョンが一致しない
   * - SharedRPCPlugin: end region mismatch
     - 同じチャンネルを共有するプラグインで、終了リージョンが一致しない
   * - その他
     - OpaqueRPCPlugin と共通です

備考、制限事項
-------------------

通信の両端について、OpaqueRPCPlugin と同じ仮定をおいています。

 * 呼び元と呼び先で、エンディアンが同じである
 * 呼び元と呼び先で、``char``, ``short``, ``int_t``, ``long_t``, ``intptr_t`` のサイズが同じである
 * 呼び元と呼び先で、有符号型と無符号型のサイズが同じである

関連
----------------------------

 * OpaqueRPCPlugin プラグインリファレンス
 * TransparentRPCPlugin プラグインリファレンス
 * :doc:`Plugin`
