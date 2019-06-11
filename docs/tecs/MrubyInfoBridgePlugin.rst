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
(RawEtnryDescriptor †) を取得して動的結合することで、目的となるセルを呼
びだすことができます。

プラグイン種別
----------------------------

MrubyInfoBridgePlugin はマルチプラグインです。適応可能な対象は、シグニ
チャまたはセルです。
通常は、nTECSInfo::tTECSInfoCompo または nTECSInfo::tTECSInfoAccessor
のセルに対し適用します。

使用方法
----------------------------

MrubyInfoBridgePlugin を使用するには、コンポーネント記述 TECS CDL と
mruby コード (.rb) に、それぞれ定型の記述を追加します。
その上で セル名、受け口名を指定して TECS のセルに結合し、呼びだすこと
ができます。

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

.. code-block:: tecs-cdl

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

mruby コード記述例

.. code-block:: tecs-cdl
                
     bridge = TECS::Bridge.join2( "Sample.eEnt", nBride_sSample )

現在の実装では TECSInfo でネームスペースパスを得ることができないため、
ネームスペースパスを指定する必要があります。

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

・MrubyBridgePlugin との併用
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

