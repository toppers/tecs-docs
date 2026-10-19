.. _MrubyBridgePlugin:

MrubyBridgePlugin プラグインリファレンス
===================================================

名前
-------

  MrubyBridgePlugin ... mruby から TECS のセルを呼び出すブリッジプラグイン

概要
-------

TECS CDL のシグニチャ記述に基づき、mruby と TECS コンポーネントをブリッ
ジします。シグニチャごとに、mruby の C 言語実装クラス (ブリッジクラス)
であり、かつ TECS のセルタイプでもあるもの (ブリッジセルタイプ) を生成
します。

ブリッジセルは、ブリッジセルタイプのセルとして CDL に記述し、mruby から
操作したいセル (目的セル) の受け口に結合します。mruby のコードでは、ブ
リッジクラスのインスタンスを生成し、そのメソッドを呼び出すことで、目的
セルの受け口関数が呼び出されます。

.. code-block:: none

            +--------------------------+              +-------------------+
            |     (ブリッジセル)         |              |    (目的セル)      |
            |                          |              |                   |
   mruby    | nMruby::tsSignature      |  sSignature  |  tTargetCelltype  |
    - - - > |       BridgeCell         |--------------|>   TargetCell     |
            |                          |cTECS    eTest|                   |
            | mruby クラス：            |              |                   |
            |  TECS::TsSignature       |              |                   |
            +--------------------------+              +-------------------+

実行時情報機能 TECSInfo を使用し、セル名と受け口名の文字列で結合先を指定
する版は :ref:`MrubyInfoBridgePlugin` を参照してください。

プラグイン種別
----------------------------

MrubyBridgePlugin はマルチプラグインです。適応可能な対象は、シグニチャ、
セルタイプ、コンポジット、セルです。

.. list-table::
   :header-rows: 1
   :widths: 20 30 50

   * - 適用対象
     - 実体となるプラグイン
     - 役割
   * - シグニチャ
     - MrubyBridgeSignaturePlugin
     - シグニチャに対するブリッジセルタイプとブリッジクラスを生成する
   * - セル
     - MrubyBridgeCellPlugin
     - セルの受け口のシグニチャに対し MrubyBridgeSignaturePlugin を適用し、ブリッジセルも生成する
   * - セルタイプ
     - MrubyBridgeCelltypePlugin
     - セルタイプに属するセルの受け口に対しブリッジを生成する
   * - コンポジット
     - MrubyBridgeCompositePlugin
     - コンポジットセルタイプに対するブリッジを生成する

シグニチャプラグインの使い方が基本となります。セル、セルタイプ、コンポ
ジットへの適用は、シグニチャごとの generate とブリッジセルの記述を自動
化するものです。

構文
----------------------------

 .. code-block:: tecs-cdl

  generate( MrubyBridgePlugin, (シグニチャ名), "(オプション)" );
  generate( MrubyBridgePlugin, (セル名), "(オプション)" );

シグニチャは、generate の記述よりも前に定義されている必要があります。
オプションが複数ある場合は、','(コンマ)で区切ります。多くの関数を指定する
場合は、文字列を分割して連接できます。

 .. code-block:: tecs-cdl

  generate( MrubyBridgePlugin, sSignature,
      "ignoreUnsigned=true, "
      "include='func1,func2', "
      "include='func3,func4', "
  );

オプション
----------------------------

シグニチャに適用する場合
````````````````````````````

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - オプション
     - 説明
   * - ``include=func1,func2,...``
     - ブリッジの対象とする関数名を指定します。``exclude`` と同時に指定できません (MRB1011)。シグニチャにない関数名はエラーです (MRB1009)。
   * - ``exclude=func1,func2,...``
     - ブリッジの対象から除外する関数名を指定します。``include`` と同時に指定できません (MRB1011)。シグニチャにない関数名はエラーです (MRB1010)。
   * - ``ignoreUnsigned[=true]``
     - 無符号整数型へのポインタ型を、有符号整数型のポインタ型として扱います (値の範囲チェックを含む)。ポインタを扱うクラスのメモリ使用量を抑えられ、有符号・無符号の使い分けを緩くできます。既定値は ``false`` です。
   * - ``auto_exclude=true|false``
     - mruby から呼びだせない関数を自動的に除外するかどうかを指定します。既定値は ``true`` です。``false`` の場合は、該当する関数があるとエラーになります。

セルに適用する場合
````````````````````````````

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - オプション
     - 説明
   * - ``exclude_port=port1,port2,...``
     - ブリッジの対象から除外する受け口名を指定します。セルタイプにない受け口名はエラーです。
   * - ``exclude_port_func=port.func,...``
     - ブリッジの対象から除外する関数を ``受け口名.関数名`` の形式で指定します。
   * - ``ignoreUnsigned[=true]``
     - シグニチャの場合と同じです。
   * - ``auto_exclude=true|false``
     - シグニチャの場合と同じです。

セルに適用すると、そのセルタイプの受け口のうち、シグニチャのコンテキス
トが ``task`` または ``any`` のものについて、シグニチャプラグインの適用
とブリッジセル ``(セル名)(受け口名)Bridge`` の生成が行われます。

セルタイプ、コンポジットに適用した場合のオプションは、ソースからは確定できていません (TBC)。

生成されるもの
----------------------------

シグニチャ (グローバル名 ``sigGlobalName``) に対して生成されるものは、次のとおりです。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 生成物
     - 説明
   * - ブリッジセルタイプ ``nMruby::t`` + ``sigGlobalName``
     - 呼び口 ``cTECS`` を持ちます。属性 ``VMname`` (mruby VM のセル名、既定値 ``"VM"``) を持ちます。
   * - 初期化セルタイプ ``nMruby::t`` + ``sigGlobalName`` + ``_Initializer``
     - mruby VM へブリッジクラスを登録します。
   * - mruby のブリッジクラス ``TECS::T`` + ``sigGlobalName``
     - ブリッジセル名を引数として ``new`` すると、インスタンスが生成されます。
   * - ポインタ・構造体クラス
     - ``TECS::Int8Pointer`` など、引数の型として使われたものだけが生成されます。

例: シグニチャ ``sSignature`` に対し、ブリッジセルタイプ ``nMruby::tsSignature`` とブリッジクラス ``TECS::TsSignature`` が生成されます。

ブリッジセルタイプに対応する CDL は、概念的には次のとおりです。

 .. code-block:: tecs-cdl

   namespace nMruby {
     celltype tsSignature {
       call sSignature cTECS;
     };
   };

生成時に、シグニチャとブリッジクラスの対応が標準出力に表示されます。
また、tecsgen を実行すると、VM の初期化セルへの結合を促す次のメッセージが出力されます。

.. code-block:: none

  MrubyBridgePlugin: join your VMs cInitialize to VM_TECSInitializer.eInitialize

使用方法
----------------------------

1) ブリッジセルの設置
````````````````````````````

ブリッジセルは、ブリッジセルタイプのセルとして CDL に記述し、呼び口
``cTECS`` を、mruby から呼びだしたいセルの受け口に結合します。

 .. code-block:: tecs-cdl

   cell nMruby::tsSignature BridgeCell {
     cTECS = Cell.eEnt;
   };

VM が複数ある場合など、VM のセル名を既定値 ``VM`` から変える場合は、属性
``VMname`` を指定します。``VMname`` は、``VM_TECSInitializer`` のように、
ブリッジを登録するセルの名前に使われます。

 .. code-block:: tecs-cdl

   cell nMruby::tsSignature BridgeCell {
     cTECS = Cell.eEnt;
     VMname = "VM2";
   };

2) mruby コードでの呼び出し
````````````````````````````

ブリッジクラスは、モジュール ``TECS`` の下に作成されます。ブリッジクラ
スの名前は、シグニチャのグローバル名に ``T`` を前置したものです。ブリッ
ジセル名を引数として ``new`` することで、ブリッジのインスタンスが生成さ
れます。ブリッジのインスタンスは、ブリッジセルへのポインタ情報を保持す
るだけで、同一のブリッジのインスタンスは何度でも生成できます。

 .. code-block:: ruby

   bridge = TECS::TsSignature.new( "BridgeCell" )
   bridge.func( 1, 2 )

簡単な使用例は、tecsgen の ``SimpleSample.cdl`` および ``SimpleSample.rb``
にあります。

扱える型
----------------------------

MrubyBridgePlugin を適用するシグニチャでは、次の型を扱えます。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - TECS の型
     - mruby 側
   * - ``bool_t``
     - ``true`` / ``false``。mruby で偽と見なされるもの (``false``, ``nil``) は C の false、それ以外は true として扱います。整数値 0 は偽とは見なされません。
   * - ``char_t``, ``uchar_t``
     - FIXNUM (0..255)
   * - ``schar_t``
     - FIXNUM (-128..127)
   * - ``intN_t``, ``uintN_t`` (N=8,16,32,64), ``int``, ``short``, ``long``, ``char``
     - FIXNUM
   * - ``double64_t``, ``float32_t``
     - FLOAT
   * - ``bool_t*``, ``intN_t*``, ``char_t*``, ``float32_t*``, ``double64_t*`` など
     - ``TECS::BoolPointer``, ``TECS::Int32Pointer``, ``TECS::CharPointer``, ``TECS::Float32Pointer``, ``TECS::Double64Pointer`` など (ポインタの指す先の値を扱う)
   * - ``struct TAG``, ``struct TAG*``
     - ``TECS::StructTAG`` (``TAG`` は構造体のタグ名)

型についての制限は、次のとおりです。

 * ``void *`` は扱えません。アドレス値を渡したい場合は ``intptr_t``, ``uintptr_t`` を使用します。
 * ポインタ型は、``size_is``, ``string`` 指定の有無にかかわらず扱えます。ただし、構造体型へのポインタに ``size_is`` を指定したものは扱えません (MRB1004)。
 * ``string`` の長さ指定がない場合は、``in`` 引数にのみ使用できます。
 * 構造体のメンバは、スカラー型でなければなりません (MRB1006)。タグのない構造体、``typedef`` した名前による構造体は扱えません。
 * ``typedef`` された型は、元の型として扱われます。
 * 戻り値の型は ``void``, ``bool_t``, ``char_t``, ``intN_t``, ``float32_t``, ``double64_t``, ``int``, ``short``, ``long``, ``char`` (およびこれらの ``typedef``) に限られます。
 * 引数の方向は ``in``, ``inout``, ``out`` が指定できます。``send``, ``receive`` は指定できません。

整数値が引数の型の範囲を超える場合は、例外が発生します。無符号型は負の値を取れません (``mrb_int`` と同じかそれ以上のサイズの場合を除く)。ビルド時にマクロ ``TECS_NO_VAL_CHECK`` を定義すると、値の範囲チェックを行いません。

``initialize`` という名前の関数は、mruby の既定メソッドと重複するため ``initialize_cell`` に置き換えられます。``initialize`` と ``initialize_cell`` の両方がシグニチャにある場合はエラーです。

自動的に除外される関数
````````````````````````````

``auto_exclude=true`` の場合、使用できない型の戻り値や引数 (``send``, ``receive`` 方向の引数) をもつ関数は、ブリッジの対象から自動的に除外されます。

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
   * - MRB1002, MRW2001
     - 警告
     - ``initialize`` は内部で定義されている。mruby 側では ``initialize_cell`` に変更する
   * - MRB1003
     - エラー
     - ``send``, ``receive`` 方向の引数が使用できない (``auto_exclude=false`` の場合)
   * - MRB1004
     - エラー
     - 構造体へのポインタに ``size_is``, ``count_is``, ``string`` は指定できない
   * - MRB1005
     - エラー
     - 引数の型が使用できない
   * - MRB1006
     - エラー
     - 構造体のメンバの型が使用できない
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
     - エラー
     - ``exclude`` により、残った関数がない
   * - MRB9999
     - エラー/警告
     - 長さ指定のない ``string`` を ``out``, ``inout`` に使用した。``exclude_port`` / ``exclude_port_func`` / ``auto_exclude`` の指定が不正

備考、制限事項
-------------------

Makefile について
````````````````````````````

``gen/Makefile.templ`` に変更を加える必要があります。``tSysLog`` を使用する場合は、リロケータブルオブジェクトを追加します。

.. code-block:: none

  OTHER_OBJS = $(_TECS_OBJ_DIR)vasyslog.o

VM が異なる場合のブリッジ名
````````````````````````````

VM が異なる場合に、他の VM に割り付けたブリッジ名が見えてしまいます。ア
クセス制限は十分ではありません。セルタイプ単位でのアクセス制限はできて
いますが、同じセルタイプで複数のブリッジセルがある場合のブリッジ名のア
クセス制限はできていません。

関連
----------------------------

 * :ref:`MrubyInfoBridgePlugin`
 * :doc:`mrubyBridge`
 * :doc:`mrubyTECSPointer`
 * :doc:`mrubyTECSStruct`
 * :doc:`Plugin`
