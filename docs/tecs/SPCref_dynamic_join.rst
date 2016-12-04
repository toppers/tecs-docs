.. _tecsspc-dynamic:

動的結合
===================

概要
------------

動的結合は、実行時に呼び口を受け口に結合させる機能です。
結合する側、結合される側、いずれのセルも生成は静的に行われていて、結合を動的に変更するものです。

用語
------------

動的呼び口
^^^^^^^^^^^^^^

  動的(dynamic)指定子が指定されて、動的結合可能な呼び口。
  ディスクリプタ設定関数によりディスクリプタ型の値を設定することで、動的結合が行われます。

ディスクリプタ参照呼び口
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  ディスクリプタ参照(ref_desc)指定子が指定されて、結合先の受け口のディスクリプタを取得することのできる呼び口。
  ディスクリプタ取得関数により、結合先の受け口のディスクリプタ型の値を取得します。

ディスクリプタ型
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

受け口ディスクリプタの型。
  受け口に対応づいたシグニチャにより型が決定されます。
  以下の構文で受け口型を記述します。

.. code-block:: tecs-cdl

       'Descriptor' '(' ネームスペースシグニチャ名 ')'

【記述例】

.. code-block:: tecs-cdl

       Descriptor( sSignature )

TECS CDL においては、関数の引数の型としてのみ用いることができます。
属性や、内部変数、定数の型として用いることはできません。
セルタイプコードにおいては、typedef 型として用いることができます。

自身を含むシグニチャを Descriptor の引数に与えることはできません。

コンポーネント記述
-------------------------

動的結合の TECS CDL の記述例を示します。

.. code-block:: c
                
 /*----  (動的結合の対処となる)一般的なシグニチャの例 ------*/
 signature sSignature {
    initialize();
    do_something();
    finalize();
 };
 /*----  ディスクリプタ型を出力するシグニチャの例 ------*/
 signature sGetDescriptor {
    ER getDescriptor( [out] Descriptor(sSignature) *pDesc );
 };
 /*----  ディスクリプタ型を入力するシグニチャの例 ------*/
 signature sSetDescriptor {
    ER setDescriptor( [in] Descriptor(sSignature) desc );
 };

 /*----  動的呼び口を持つセルタイプの例 ------*/
 celltype tCelltype {
   [dynamic]
     call  sSignature cCallDynamic;
   [ref_desc]
     call  sSignature cCallRefDesc;
   call  sGetDescriptor  cGetDescriptor;  // 呼び口を動的に得る
   entry sSetDescriptor  eSetDescriptor;  // 呼び口を動的に設定する
 };
 /*----  動的呼び口を持つ複合セルタイプの例 ------*/
 composite tComposite {
   [dynamic]
     call  sSignature cCallDynamic;
   [ref_desc]
     call  sSignature cCallRefDesc;
   call  sGetDescriptor  cGetDescriptor;
   entry sSetDescriptor  eSetDescriptor;

   cell tCelltype Inner{
     cCallDynamic = composite.cCallDynamic;
     cCallRefDesc = composite.cCallRefDesc;
     cGetDescriptor = composite.cGetDescriptor;
   };
   composite.eSetDescriptor => Inner.eSetDescriptor;
 };

適合性
----------------

動的結合では、以下の条件を満たす必要があります。
これらの条件は、セルにディスクリプタの参照と動的呼び口への設定の両方が備わっていることを満たすものです。
以下を満たさなくても、コード生成は可能であるが、これらを満たさない場合、使い方に問題があると考えられます。

提供、利用、または転送のいずれかにおいて、一つ以上の条件を満たす必要があります。

なお、以下の提供、利用、転送の関係において、呼び口、またはディスクリプタ型のシグニチャは一致しなくてはなりません。

提供
^^^^^^^^^^^^^^^^^^^^^^^

 * 呼び口の ref_desc かつ 受け口の out 引数に ディスクリプタ型がある
 * 呼び口の ref_desc かつ 呼び口の in 引数に ディスクリプタ型がある

利用
^^^^^^^^^^^^^^^^^^^^^^^

 * 呼び口の dynamic かつ 受け口の in 引数に ディスクリプタ型がある
 * 呼び口の dynamic かつ 呼び口の out 引数に ディスクリプタ型がある

提供と利用
^^^^^^^^^^^^^^^^^^^^^^^

 * 呼び口の dynamic かつ 呼び口の ref_desc がある (自己完結)

転送
^^^^^^^^^^^^^^^^^^^^^^^

 * (受け口の out 引数 or 呼び口の in 引数に ディスクリプタ型がある)  かつ (受け口の in 引数 or 呼び口の out 引数に ディスクリプタ型がある)

 以下は、「提供」、「利用」の逆（自己完結を除く）．チェック済みを記憶しないために必要となる規則．
 * (受け口の out 引数 or 呼び口の in 引数に ディスクリプタ型がある) かつ 呼び口の ref_desc がある
 * (受け口の in 引数 or 呼び口の out 引数に ディスクリプタ型がある) かつ 呼び口の dynamic がある

その他の適合性
^^^^^^^^^^^^^^^^^^^^^^^

以下の各条件について、すべて満たす必要があります。

 * シグニチャが、空であってはならない
 * ref_desc, dynamic を指定された呼び口に対応付いたシグニチャは、引数にディスクリプタ型を含んではいけない
 * ref_desc と dynamic の両方を一つの呼び口に指定することはできない
 * ref_desc, dynamic と omit は両立しない
 * ref_desc, dynamic を呼び口配列に指定することができる
 * Descriptor は、関数の in, out, inout 引数にのみ用いることができる
     セルタイプコードにおいては、この制限はない
 * Descriptor を含むシグニチャを Descriptor の引数に指定することはできない
   * ヘッダファイルの相互参照が起きないことを保障できる
   * 動的な受け口を、動的に渡すような、ことを許さない
 * Descriptor の引数が、自身を含むシグニチャの場合
    Descriptor の引数が、自身を含むシグニチャとすることはできない。
    このシグニチャは、dynamic や ref_desc の指定された呼び口に対応付けられると考えられるが、ディスクリプタ型の引数を持つシグニチャ sGetDesc を指定することができないため、別途エラーとなる。

.. code-block:: tecs-cdl

  signature sGetDesc {
     void  func( [out]Descriptor( sGetDesc ) *desc );  // Descriptor の引数が、自身を含むシグニチャ
  };


他の指定子との併用
-------------------------------

ダイナミック指定子を他の指定子と併用する場合について、説明します。

オプショナル(optional)指定子との併用
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

オプショナル指定子は、動的(dynamic)指定子、ディスクリプタ参照(ref_desc)指定子のいずれとも同時に指定できます。

オプショナル指定かつ動的指定された呼び口を未結合にすることができます。未結合(unjoin)にするセルタイプコードの記述方法は、セルタイプコードの節を参照してください。

ディスクリプタ参照(ref_desc) 指定された呼び口が、オプショナル指定されている場合、未結合状態を返す可能性があります。
未結合状態のディスクリプタを動的呼び口に設定してはなりません。アサーと(assert) により、例外検出します。
未結合状態のディスクリプタを動的呼び口に設定するのではなく、未結合化(unjoin) します。「オプショナル指定されたディスクリプタ参照呼び口の注意点」の項を参照してください。

省略 (omit) 指定子との併用
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

併用することはできません。
動的(dynamic)指定子や、ディスクリプタ参照(ref_desc)指定子を、省略(omit)指定子と同時に指定することはできません。

セルタイプコード
--------------------------

動的結合のセルタイプコードの書き方について説明します。

ディスクリプタ型 
^^^^^^^^^^^^^^^^^^^^^^^^^^

セルタイプコードにおいて、ディスクリプタ型は、引数以外にも用いることができます。
ディスクリプタ型は、TECS CDL と同様の記述であるが、ネームスペースシグニチャ名ではなく、シグニチャのグローバル名を引数とします。

TECS CDL の記述

.. code-block:: tecs-cdl

    Descriptor( nNameSpace::sSignature )

セルタイプコード

.. code-block:: c

    Descriptor( nNameSpace_sSignature )


コード例

.. code-block:: tecs-cdl
   
    Descriptor( sDynamicSignature ) desc;  // ディスクリプタ型の変数の定義


ディスクリプタの参照(取得)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ディスクリプタ参照(ref_desc)指定された呼び口(cRefDescCall)に結合された受け口のディリプタを参照する (取得する) コードの例を示します。

.. code-block:: c

    desc = cRefDescCall_refer_to_descriptor();


呼び口(cRefDescCall)が呼び口配列の場合、コードの例は、以下の通りです。

.. code-block:: c
   
    desc = cRefDescCall_refer_to_descriptor( i );

=== オプショナル指定されたディスクリプタ参照呼び口の注意点 ===

オプショナル指定されたディスクリプタ参照呼び口からは、未結合状態(内部的にはNULL) が得られる可能性があります。
これをテストするには is_descriptor_unjoined マクロを用います。

.. code-block:: c
   
    is_descritpror_unjoined( descriptor )

引数 descriptor にはディスクリプタ型の変数を与えてください。

なお、ディスクリプタ参照(ref_desc)指定された呼び口(cOptinalRefDescCall)が結合されていることをテストするには、以下のマクロを用います。
これは、動的に限らず、オプショナルな呼び口において、結合されていることをテストするマクロと同じです。

.. code-block:: c

   is_cOptinalRefDescCall_joined()   // int 値を返す。結合済みなら 1, そうでなければ 0 を返す

参考：引数のヌルアブル(nullable)指定子は、ディスリプタ型へのポインタがヌルとなりうるかどうかを示すもので、ディスクリプタ型が未結合状態 (内部的にはNULL) であることを示すものではない。

動的結合の実行
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

動的(dynamic)指定された呼び口(cDyanmicCall)に、受け口のディスクリプタを設定する、すなわち動的結合するコードの例は、以下の通りです。

.. code-block:: c

    cDynamiCall_set_descriptor( desc );

オプショナル指定された動的呼び口の未結合化
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

オプショナル(optional)指定された呼び口(cDyanmicOptionalCall)の場合は、未結合にすることができるが、この場合はアンジョイン関数を使用します。
結合を解除する目的で desc に NULL を渡すのは、誤りです。

.. code-block:: c
   
    cOptionalDyamicCall_unjoin();


動的呼び口配列の場合の動的結合の実行、未結合化
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

オプショナルな呼び口(cDyanmicOptionalCall)が呼び口配列の場合は、以下のように記述します。

呼び口配列の場合の、動的結合の実行

.. code-block:: c

    cDynamiCall_set_descriptor( i, desc );

呼び口配列の場合の、未結合化

.. code-block:: c

    cOptionalDyamicCall_unjoin( i );

