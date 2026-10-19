.. _TracePlugin:

TracePlugin プラグインリファレンス
===================================================

名前
-------

  TracePlugin ... 受け口関数の呼び出しをトレースするスループラグイン

概要
-------

セルの呼び口と受け口の間に、トレース用のセルを挿入します。受け口関数が
呼び出されるたびに、関数の入口 (``Enter``) と出口 (``Leave``) で、``syslog``
を用いて、呼び出し元のセル名と引数の値を出力します。

トレース用のセルは、結合先の受け口と同じシグニチャを持ちます。呼び出し
は、そのまま元の受け口へ中継されます。

プラグイン種別
----------------------------

TracePlugin はスループラグイン (ThroughPlugin の派生) です。結合の記述に
``through`` 指定子で指定するか、リージョンの ``in_through``,
``out_through``, ``to_through`` 指定子で指定します。

構文
----------------------------

結合に対して指定する場合は、呼び口の結合の直前に ``through`` 指定子を記述します。

 .. code-block:: tecs-cdl

  cell tSample Sample {
    [through(TracePlugin,"")]
      cSimple = Simple.eSimple;
  };

リージョンの境界で指定する場合は、リージョンの ``in_through``,
``out_through`` に指定します。このとき、リージョンを通過する結合すべてが
トレースの対象になります。

 .. code-block:: tecs-cdl

  [in_through(TracePlugin,""), out_through()]
  region rSPon {
    ...
  };

オプション
----------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - オプション
     - 既定値
     - 説明
   * - ``maxArrayDisplay=N``
     - 16
     - ``size_is``, ``count_is`` 指定の配列の要素を表示する最大の個数を指定します。
   * - ``cellEntry=cell.entry,...``
     - (指定なし)
     - トレースの対象とする受け口を ``セル名.受け口名`` の形式で指定します。コンマ区切りで複数指定できます。指定した場合、指定外の受け口にはトレース用のセルを挿入せず、元の受け口にそのまま結合します。形式が異なるとエラーになります。
   * - ``probeName=name``
     - (なし)
     - トレース出力の先頭に付ける名前を指定します。「name: 」(コロンと空白) の形式で各行に付加されます。
   * - ``displayTime=true|false``
     - ``false``
     - 時刻の表示を指定します。``true`` と ``false`` 以外はエラーです。(注: 1.9.1 の実装では、この指定を保持する変数名が参照側と一致しておらず、指定は出力に影響しません。時刻は常に出力されます。)
   * - ``kernelCelltype=celltype``
     - ``tKernel``
     - カーネルのセルタイプを指定します。トレース用セルタイプの ``eKernel`` の require 先です。セルタイプ以外を指定するとエラーです。
   * - ``syslogCelltype=celltype``
     - ``tSysLog``
     - システムログのセルタイプを指定します。トレース用セルタイプの ``eSysLog`` の require 先です。セルタイプ以外を指定するとエラーです。

生成されるもの
----------------------------

シグニチャのグローバル名を ``sigGlobalName`` とすると、次のものが生成されます。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 生成物
     - 説明
   * - セルタイプ ``tTracePlugin_`` + ``sigGlobalName``
     - 受け口 ``eThroughEntry`` と呼び口 ``cCall`` を持ちます。属性 ``probeName_str`` と ``from_str`` (呼び出し元のセル名) を持ちます。``eSysLog`` と ``eKernel`` を require します。``gen/(セルタイプ名).cdl`` に出力されます。
   * - セル
     - 呼び口 ``cCall`` が、元の結合先の受け口に結合されます。呼び出し元のセルがあれば、``from_str`` にそのセル名が設定されます。
   * - 受け口関数の本体
     - 変更の必要のないコードが自動生成されます。

``send``, ``receive`` 方向の引数をもつ関数のために、トレース用セルタイプには、元の結合先へのアロケータ結合が設定されます。

出力形式
----------------------------

関数の入口と出口で ``syslog( LOG_INFO, ... )`` を用いて、次の形式で出力されます。

.. code-block:: none

  Enter: (probeName: )Time=(マイクロ秒): (セル名).(受け口名).(関数名) calledFrom: (呼び出し元セル名)
    [IN]  (型) (引数名) = (値);
  Leave: (probeName: )Time=(マイクロ秒): (セル名).(受け口名)[(添数)].(関数名)
    [OUT] (型) (引数名) = (値);

引数は、方向に応じて入口 (``in``, ``inout``, ``send``) または出口 (``out``,
``inout``, ``receive``) で表示されます。

 * 整数型は ``int_t`` より大きい場合 ``long`` として表示されます。
 * 浮動小数点型は ``double`` に変換して表示されます。
 * 構造体型は、メンバごとに表示されます。
 * ポインタ型は、``size_is``, ``count_is`` の値を表示した上で、要素を ``maxArrayDisplay`` 個まで表示します。
 * ``enum`` 型、関数型、配列型の表示は未対応です (ソースの ``mikan`` コメントによる)。

使用方法
----------------------------

トレース用セルタイプは、システムログの受け口 ``eSysLog`` とカーネルの受
け口 ``eKernel`` を require します。既定ではセルタイプ ``tSysLog`` と
``tKernel`` が使われるため、これらのセルタイプを持つ CDL をあらかじめ
``import`` しておきます。他のセルタイプを使用する場合は、
``kernelCelltype``, ``syslogCelltype`` で指定します。

 .. code-block:: tecs-cdl

  cell tSample Sample {
    [through(RPCPlugin,"PPAllocatorSize=1024"),through(TracePlugin,"")]
      cSimple = Simple.eSimple;
  };

``through`` 指定子は、コンマで区切って複数指定できます。上の例では、
RPCPlugin と TracePlugin が続けて挿入されます。

リージョンの ``in_through``, ``out_through`` に TracePlugin を指定して、
リージョン外から内への呼び出しをトレースする場合、システムログのセルを
リージョンの外から参照する必要があるため、``out_through()`` が併せて必要です。

 .. code-block:: tecs-cdl

  [in_through(TracePlugin,""), out_through()]
  region rSPon {
    ...
  };

備考、制限事項
-------------------

 * ``enum`` 型、関数型、配列型の引数は表示されません。
 * ``displayTime`` オプションは、1.9.1 の実装では出力に影響しません。

関連
----------------------------

 * :doc:`Plugin`
