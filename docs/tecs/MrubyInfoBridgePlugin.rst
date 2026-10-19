.. _MrubyInfoBridgePlugin:

MrubyInfoBridgePlugin プラグインリファレンス
===================================================

名前
-------

  MrubyInfoBridgePlugin ... TECSInfo 版 mruby ブリッジプラグイン

概要
-------

実行時情報機能 TECSInfo を使用した版の mruby ブリッジです。mruby のコー
ドの中から TECSInfo を用いてセル名、受け口名から生の受け口ディスクリプタ
(RawEntryDescriptor) を取得して動的結合することで、目的となるセルを呼
びだすことができます。

従来の MrubyBridgePlugin は、ブリッジセルをあらかじめ CDL に記述して結
合しておく必要があります。MrubyInfoBridgePlugin では、結合先をセル名と
受け口名の文字列で実行時に指定できます。

プラグイン種別
----------------------------

MrubyInfoBridgePlugin はマルチプラグインです。適応可能な対象は、シグニ
チャまたはセルです。
通常は、nTECSInfo::tTECSInfoCompo または nTECSInfo::tTECSInfoAccessor
のセルに対し適用します。

.. list-table::
   :header-rows: 1
   :widths: 20 30 50

   * - 適用対象
     - 実体となるプラグイン
     - 役割
   * - セル
     - MrubyInfoBridgeCellPlugin
     - 全シグニチャに対し MrubyInfoBridgeSignaturePlugin を適用するコードを生成する
   * - シグニチャ
     - MrubyInfoBridgeSignaturePlugin
     - シグニチャごとにブリッジセルタイプと mruby のブリッジクラスを生成する
   * - セルタイプ、コンポジット
     - (対応しない)
     -

MrubyInfoBridgeCellPlugin は、すべてのシグニチャに対し
``generate( MrubyInfoBridgeSignaturePlugin, (シグニチャ), "auto_exclude=true" )``
を適用するコードを生成します。ただし、ネームスペース nMrubyInfo 下のシ
グニチャは対象外です。

シグニチャごとにオプションを指定したい場合は、
MrubyInfoBridgeSignaturePlugin を直接 generate します。

構文
----------------------------

 .. code-block:: tecs-cdl

  generate( MrubyInfoBridgePlugin, (セル名), "" );
  generate( MrubyInfoBridgePlugin, (シグニチャ名), "(オプション)" );

オプション
----------------------------

オプションは、シグニチャに対して適用する場合に指定できます。
MrubyBridgePlugin のシグニチャプラグインと共通です。
オプションが複数ある場合は、','(コンマ)で区切ります。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - オプション
     - 説明
   * - ``include=func1,func2,...``
     - ブリッジの対象とする関数名を指定します。指定した関数のみが mruby から呼びだせます。シグニチャにない関数名を指定するとエラーです (MRB1009)。
   * - ``exclude=func1,func2,...``
     - ブリッジの対象から除外する関数名を指定します。シグニチャにない関数名を指定するとエラーです (MRB1010)。
   * - ``auto_exclude=true|false``
     - mruby から呼びだせない関数を自動的に除外するかどうかを指定します。既定値は ``true`` です。``true`` の場合、除外した旨が情報メッセージ (MRI0001, MRI0002) として出力されます。``false`` の場合、該当する関数があるとエラーになります (MRB1001, MRB1003)。``true`` と ``false`` 以外の値は警告 (MRB9999) となり無視されます。
   * - ``ignoreUnsigned[=true]``
     - 値を省略するか ``true`` を指定すると、``ignoreUnsigned`` が有効になります。(効果の詳細は MrubyBridgePlugin と共通。TBC)

``include`` と ``exclude`` を同時に指定するとエラーです (MRB1011)。
関数がすべて除外された場合は警告となります (MRB1012)。

自動的に除外される関数
````````````````````````````

``auto_exclude=true`` の場合、次のいずれかに該当する関数は、ブリッジの対象から自動的に除外されます。

 * 戻り値の型が bool、整数、浮動小数点数、void のいずれでもない関数
 * ``send``, ``receive`` 方向の引数をもつ関数

対象外のシグニチャ
````````````````````````````

次のシグニチャは、MrubyInfoBridgeSignaturePlugin を適用してもブリッジが生成されません。

 * nTECSInfo ネームスペースのシグニチャ (nTECSInfo::sAccessor を除く)
 * nMruby::sInitializeBridge
 * nMruby::sInitializeTECSBridge

生成されるもの
----------------------------

シグニチャ (グローバル名 ``sigGlobalName``) に対し MrubyInfoBridgeSignaturePlugin を適用すると、次のものが生成されます。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 生成物
     - 説明
   * - ブリッジセルタイプ ``nMrubyInfo::tInfo`` + ``sigGlobalName``
     - シグニチャごとのブリッジセルタイプです。呼び口 cTECS を動的結合 (``dynamic``, ``optional``) で持ち、TECSInfo の呼び口 cTECSInfo などを持ちます。シングルトンです。
   * - 初期化セルタイプ ``nMrubyInfo::tInfo`` + ``sigGlobalName`` + ``_Initializer``
     - mruby VM へブリッジクラスを登録するセルタイプです。
   * - ブリッジセル ``MrubyInfoBridge_`` + ``sigGlobalName``
     - ブリッジセルタイプのセルです。cTECSInfo を ``TECSInfo.eTECSInfo`` に結合します。
   * - mruby のブリッジクラス ``TECS::Info`` + ``sigGlobalName``
     - mruby のコードからアクセスするクラスです。``TECS::Info`` + ``sigGlobalName`` ``.new( "(セル名).(受け口名)" )`` でインスタンスが生成されます。
   * - ``gen/(セル名)Initializer.cdl``
     - VM ごとに生成される初期化セル ``(VM名)_TECSInitializer`` (セルタイプ nMruby::tTECSInitializer) の宣言です。VM 名の既定値は ``VM`` で、ブリッジセルの属性 ``VMname`` で変更できます。

生成時に、対応関係が次の形式で標準出力に表示されます。

.. code-block:: none

  MrubyInfoBridgePlugin: [signature] ::nSample::sSig => [class] TECS::Info...

また、``Makefile`` に mruby 用の設定が追加されます。

 * リンクフラグ ``-lmruby -L$(MRUBYPATH)/lib -lm``
 * インクルードパス ``$(MRUBYPATH)/include``
 * 変数 ``MRUBYPATH`` (既定値 ``..``。利用環境に合わせて変更します)

使用方法
----------------------------

MrubyInfoBridgePlugin を使用するには、コンポーネント記述 TECS CDL と
mruby コード (.rb) に、それぞれ定型の記述を追加します。
その上で セル名、受け口名を指定して TECS のセルに結合し、セルの受け口
関数呼びだすことができます。

1) TECS CDL(.cdl) の記述
````````````````````````````````

コンポーネント記述 TECS CDL には、TECSInfo の複合セルタイプ
nTECSInfo::tTECSInfoCompo のセルを追加した上で、これに対し2つのプラグ
イン MrubyBridgePlugin, MrubyInfoBridgePlugin を適用するコードを追記し
ます。

 .. code-block:: tecs-cdl

  // -------- TECSInfoAccessor --------- // <<<< ここから
  import( <TECSInfoAccessor.cdl> );
  cell nTECSInfo::tTECSInfoCompo TECSInfo {
  };

  // -------- Mruby Bridge --------- //
  import( <mruby.cdl> );
  generate( MrubyBridgePlugin, TECSInfo, "exclude_port=eTECSInfo");
  generate( MrubyInfoBridgePlugin, TECSInfo, "");
  // ---------                              <<<< ここまで

  // -------- Mruby VM の定義  ----------- //
      //  既存ものを使用する場合変更不要 (従来ブリッジと合わせて初期化が行われる)
  cell nMruby::tTECSInitializer VM_TECSInitializer;
  cell nMruby::tMrubyProc VM {
      cInit = VM_TECSInitializer.eInitialize;  // TECS ブリッジクラスの登録
  };

2) mruby コード (.rb) の記述
````````````````````````````````

2-1) 追加コード
``````````````````

以下を mruby のコードに追加します。

.. code-block:: ruby

  ## -------- MrubyInfoBridgePlugin: Bridge Joiner --------- ##
  module TECS
    module Bridge
      @@accessor = TECS::TnTECSInfo_sAccessor.new( 'TECSInfoeAccessorBridge' )
      @@cp = TECS::CharPointer.new( 256 );
      def self.join( cell_ent_name )     # このメソッドでは、ネームスペース下のシグニチャに対応しない
        cell_ent_chararray = TECS::CharPointer.new( cell_ent_name.length + 1);
        cell_ent_chararray.from_s cell_ent_name
        if( @@accessor.getSignatureNameOfCellEntry( cell_ent_chararray, @@cp, @@cp.length) != 0 )
          raise "'#{cell_ent_name}' not found"
        end
        signature_name = @@cp.to_s
        self.join2( cell_ent_name, signature_name )
      end
      def self.join2( cell_ent_name, signature_global_name )
                # このメソッドでは、ネームスペース下のシグニチャに対応できる
                # signature_global_name は '_' つなぎ、'::' ではない
        bridgeClass = Object.const_get( 'TECS::Info' + signature_global_name.to_s )
                # this can cause Ruby exception for non-existing signature name
        bridgeClass.new( cell_ent_name )
      end
    end
  end

2-2) ブリッジの生成と結合
````````````````````````````````````

mruby のコード (.rb) でブリッジを生成し TECS のセルの受け口に結合す
るコードは、以下のように記述します。受け口配列でない場合と、受け口配
列の場合の例を示します。

1. 非配列の受け口へのブリッジの生成

   mruby コード記述例

.. code-block:: ruby

     bridge = TECS::Bridge.join( "Sample.eEnt" )

join の引数は、(セル名) + '.' + (受け口名) の文字列である。

2. 受け口配列へのブリッジの生成

   mruby コード記述例

.. code-block:: ruby

     bridge2 = TECS::Bridge.join( "Sample.eEntArray[1]" )

join の引数は (セル名) + '.' + (受け口名) + '[' + (配列添数) + ']'の文
字列である。

上記により TECS::Bridge.join は、受け口のシグニチャ名を調べてシグニチャ
に対応するブリッジクラスのインスタンスが生成され結合されます。

2-3) ネームスペース下にシグニチャがある場合
````````````````````````````````````````````

受け口のシグニチャの定義が子ネームスペースの下にある場合、2-2) の方法
では結合できません。この場合、シグニチャのグローバル名も指定してjoin2
メソッドを使用して結合します。
グローバル名は、ネームスペース名とシグニチャ名を '_' でつないだもので
す ('::' ではありません)。

mruby コード記述例

.. code-block:: ruby

     bridge = TECS::Bridge.join2( "Sample.eEnt", "nBridge_sSample" )

現在の実装では TECSInfo でネームスペースパスを得ることができないため、
ネームスペースパスを指定する必要があります。

mruby から見たクラスと関数
----------------------------

ブリッジクラスのインスタンスに対し、シグニチャの関数と同名のメソッド
を呼びだすことで、結合先のセルの受け口関数が呼びだされます。

 * シグニチャに ``initialize`` という名前の関数がある場合、内部で
   ``initialize`` を定義しているため、mruby 側では ``initialize_cell``
   に名前を変更する必要があります (警告 MRW2001, MRB1002)。

エラー・警告メッセージ
----------------------------

.. list-table::
   :header-rows: 1
   :widths: 15 15 70

   * - 番号
     - 種別
     - 内容
   * - MRB1001
     - エラー
     - 戻り値の型が使用できない (``auto_exclude=false`` の場合)
   * - MRB1003
     - エラー
     - ``send``, ``receive`` 方向の引数が使用できない (``auto_exclude=false`` の場合)
   * - MRB1009
     - エラー
     - ``include`` に指定した関数がシグニチャにない
   * - MRB1010
     - エラー
     - ``exclude`` に指定した関数がシグニチャにない
   * - MRB1011
     - エラー
     - ``include`` と ``exclude`` を同時に指定した
   * - MRB1012
     - 警告
     - ``exclude`` により、残った関数がない
   * - MRB1002, MRW2001
     - 警告
     - ``initialize`` は内部で定義されている。mruby 側では ``initialize_cell`` に変更する
   * - MRB9999
     - 警告
     - ``auto_exclude`` の値が不正 (``true`` か ``false`` を指定する)
   * - MRBW001
     - 情報
     - 同じシグニチャに対するプラグインの重複。2つめ以降は無視される
   * - MRI0001, MRI0002
     - 情報
     - 使用できない戻り値の型または引数方向のため、関数を自動除外した

備考、制限事項
-------------------

マルチ VM に未対応
````````````````````````````````````````

マルチ VM に対応しません。
このため、マルチ VM に対応したい場合、現時点では従来の
MrubyBridgePlugin を用いてください。

マルチ VM 下で使用するには、次の問題があります。

 * 同時に同じシグニチャの受け口を呼びだした時、他方の結合先のセルを呼び出す可能性がある

同時に同じシグニチャの受け口を呼びだした時、他方の結合先のセルを呼び出
す可能性があるのは、mruby においては異なるブリッジのインスタンスが生成
されますが、それに対応する TECS のコンポーネントは、同じシグニチャに対
しては、1つのセルしか存在しておらず、かつ動的結合により結合先を切り替
えているためです。

この問題は、強い動的結合を導入することで解決する予定です。従来の動的結
合 (これを弱い動的結合と呼ぶことにします)は、セルの呼び口を書き換える
ためにリエントラント性を確保することができません。強い動的結合では、自
動変数として呼び口を持つことでリエントラント性を確保します。強い動的結
合によりリエントラント性が確保されることで、同じシグニチャに対しては1
つしかブリッジセルがなくても、同時に異なる結合先に結合させることができ
るようになります。

MrubyBridgePlugin との併用
````````````````````````````````````````

VM_Initializer セルには MrubyBridgePlugin, MrubyInfoBridgePlugin の両
方の初期化セルがマージされて出力されます。

MrubyBridgePlugin の呼出しは必須ではない
````````````````````````````````````````````````````````````

 以下の行は必須ではありません。

.. code-block:: tecs-cdl

  generate( MrubyBridgePlugin, TECSInfo, "exclude_port=eTECSInfo");

この行は join メソッドを使用する場合には必要ですが、join2 メソッドの
みを使用する場合には不要です。少しオーバーヘッドを低減できます。
@@accessor を初期化する行も不要になりますので合わせて削除します。

関連
----------------------------

 * :doc:`mrubyBridge`
 * :doc:`Plugin`
