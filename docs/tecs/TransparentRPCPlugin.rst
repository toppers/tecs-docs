.. _TransparentRPCPlugin:

TransparentRPCPlugin プラグインリファレンス
===================================================

名前
-------

  TransparentRPCPlugin ... Transparent RPC チャンネルを生成するスループラグイン

  CDL で指定するプラグイン名は ``RPCPlugin`` です。このリファレンスでは、
  Transparent RPC を行う ``RPCPlugin`` を TransparentRPCPlugin と呼びます。

概要
-------

異なるリージョン (たとえば異なるノードやプロセッサ) にあるセル間の呼び
出しを、RPC (Remote Procedure Call) で中継するチャンネルを生成します。
呼び元のセルは、呼び先のセルが同じ場所にあるかのように、通常の呼び口で
呼び出せます (Transparent RPC)。

シグニチャの関数の引数と戻り値は、マーシャラによって一方向チャンネルで
送られ、呼び先でアンマーシャルされて、受け口関数が呼び出されます。マー
シャラは、シグニチャごとに自動生成されます。

マーシャルの形式が固定されているため、通信の両端で型の表現が一致してい
る必要があります (「制限事項」を参照)。クライアントとサーバーを別のプ
ログラムに分けて通信する場合は、OpaqueRPCPlugin を参照してください。

プラグイン種別
----------------------------

スループラグイン (ThroughPlugin の派生) です。シグニチャのコンテキスト
が ``task`` の受け口に対してのみ使用できます (それ以外はエラー)。

結合に対して ``through`` 指定子で指定するか、リージョンの ``to_through``,
``out_through``, ``in_through`` で指定します。

構文
----------------------------

 .. code-block:: tecs-cdl

  [through(RPCPlugin,"(オプション)")]
    (呼び口) = (セル).(受け口);

実際の記述例を示します。

 .. code-block:: tecs-cdl

  cell tSample Sample {
    [through(RPCPlugin,"PPAllocatorSize=1024")]
      cSimple = Simple.eSimple;
  };

オプション
----------------------------

オプションが複数ある場合は、','(コンマ)で区切ります。

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - オプション
     - 既定値
     - 説明
   * - ``taskPriority=N``
     - 8
     - RPC チャンネルのタスクの優先度を指定します。
   * - ``channelCelltype=celltype``
     - ``tDataqueueOWChannel``
     - 一方向チャンネルのセルタイプを指定します。セルタイプ (コンポジットセルタイプを含む) 以外を指定するとエラーです。
   * - ``TDRCelltype=celltype``
     - ``tTDR``
     - TDR のセルタイプを指定します。セルタイプ以外を指定するとエラーです。
   * - ``channelCell=name``
     - ``(セル名)_Channel``
     - 一方向チャンネルのセル名を指定します。識別子として使える名前でなければなりません。
   * - ``PPAllocatorSize=N``
     - (指定なし)
     - 引数の総和のサイズを指定します。``oneway`` 関数の ``in`` 引数に配列があるシグニチャでは必須です (指定しないとエラー RPC9999)。
   * - ``noClientSemaphore=true|false``
     - ``false``
     - ``true`` を指定すると、クライアント側のセマフォを生成しません。``true`` と ``false`` 以外はエラーです。
   * - ``semaphoreCelltype=celltype``
     - ``tSemaphore``
     - セマフォのセルタイプを指定します。セルタイプ以外を指定するとエラーです。

生成されるもの
----------------------------

シグニチャのグローバル名を ``sigGlobalName`` とします。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 生成物
     - 説明
   * - マーシャラ / アンマーシャラのセルタイプ ``tMarshaler_`` + ``sigGlobalName``, ``tUnmarshaler_`` + ``sigGlobalName``
     - シグニチャごとに ``gen/`` 下に CDL ファイルとして生成されます。生成は ``TransparentRPCSignaturePlugin`` の generate を介して行われます。
   * - RPC チャンネルのセルタイプ ``tRPCPlugin_`` + (TDR) + ``_`` + (チャンネル) + ``_`` + ``sigGlobalName``
     - ``gen/`` 下に CDL ファイルとして生成されます。
   * - 一方向チャンネルのセル
     - ``channelCelltype`` のセルです。名前は ``channelCell`` で指定します。
   * - RPC チャンネルのセル
     - 呼び口を元の結合先の受け口に結合し、``cTDR`` と ``cEventflag`` をチャンネルセルの ``eTDR``, ``eEventflag`` に結合します。属性 ``taskPriority`` が設定されます。

結合先のセルにアロケータ指定がある場合は、RPC チャンネルのセルの受け口
``eThroughEntry`` にアロケータ指定が引き継がれます。

使用方法
----------------------------

1) 結合に対する指定
````````````````````````````

RPC を経由させたい結合に、``through`` 指定子を記述します。

 .. code-block:: tecs-cdl

  cell tSample Sample {
    [through(RPCPlugin,"PPAllocatorSize=1024")]
      cSimple = Simple.eSimple;
  };

  cell tSimple Simple {
    [through(RPCPlugin,"PPAllocatorSize=1024")]
      cCall = Sample.eEnt;
  };

2) リージョンの境界に対する指定
````````````````````````````````

リージョンを分け、リージョンを通過する結合すべてに RPC を適用する場合は、
リージョンの ``out_through``, ``in_through``, ``to_through`` に指定します。
すべての結合に対して、シグニチャごとにチャンネルが生成されます。

3) 他のスループラグインとの併用
````````````````````````````````

``through`` 指定子はコンマで区切って複数指定できます。たとえば RPC の
前後にトレースを入れる場合は、TracePlugin を併用します。

 .. code-block:: tecs-cdl

  [through(RPCPlugin,"PPAllocatorSize=1024"),through(TracePlugin,"")]
    cSimple = Simple.eSimple;

エラー・警告メッセージ
----------------------------

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 番号 / メッセージ
     - 内容
   * - RPC9999 (context)
     - シグニチャのコンテキストが ``task`` でない
   * - RPC9999 (PPAllocatorSize)
     - ``oneway`` 関数の ``in`` 配列に対し ``PPAllocatorSize`` が指定されていない
   * - RPC9999 (noClientSemaphore)
     - ``noClientSemaphore`` に ``true`` と ``false`` 以外を指定した
   * - RPC9999 (semaphoreCelltype)
     - ``semaphoreCelltype`` がセルタイプでない、または定義されていない
   * - RPCPlugin: channeclCelltype
     - ``channelCelltype`` がセルタイプでない、または見つからない
   * - RPCPlugin: TDRCelltype
     - ``TDRCelltype`` がセルタイプでない、または見つからない
   * - RPCPlugin: channeclCellName
     - ``channelCell`` が識別子として使えない

備考、制限事項
-------------------

通信の両端について、次を仮定しています。

 * 呼び元と呼び先で、エンディアンが同じである
 * 呼び元と呼び先で、``char``, ``short``, ``int_t``, ``long_t``, ``intptr_t`` のサイズが同じである
 * 呼び元と呼び先で、有符号型と無符号型のサイズが同じである

また、ソースの注記によると、スループラグインではネームスペースが考慮さ
れていません。tecsgen の起動時に、カーネルのセルタイプを持つ CDL とチャ
ンネル用の ``sChannel.cdl`` を指定する必要があります (TBC: 現行の版で必要な
ファイル名は、利用するターゲットの環境に依存します)。

1.9.1 では、マーシャラの生成に ``TransparentRPCSignaturePlugin`` を generate します。このプラグインに
対応するファイルは tecsgen のプラグインディレクトリに見当たらず、実体の所在は確認できていません (TBC)。

関連
----------------------------

 * OpaqueRPCPlugin プラグインリファレンス
 * SharedOpaqueRPCPlugin プラグインリファレンス
 * TracePlugin プラグインリファレンス
 * :doc:`Plugin`
