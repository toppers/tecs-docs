セルタイプコード
===================

セルタイプコードは、コンポーネントの振る舞いを記述するもので、受け口関数の実装です。

使用言語
...........

セルタイプコードは　C 言語で記述します。

【補足説明】C++ として記述することもできる。ただし、外部名を C 言語に合わせる。

記述単位
...........

セルタイプコードは、セルタイプごとにファイルを分けて記述します。
一つのセルタイプのセルタイプコードを、複数のファイルに分けて記述することはできます。

インラインの受け口関数と非インラインの受け口関数とでは、ファイルを分けて記述します。

【補足説明】複数のセルタイプのセルタイプコードを一つにまとめることはできない。

ファイル名
..............

非インライン受け口関数を格納するファイルの名前は、セルタイプのグローバル名に C 言語の拡張子 .c を付加したものです。C++ で記述する場合には、適切な拡張子を付加します。

セルタイプコードを複数のファイルに分けて記述する場合、他のファイル名を付与します（名前付け規則は定めない）。

【ファイル名の例】

    tCelltype.c

インラインのセルタイプコードのファイル名
................................................

インラインの受け口関数を格納するファイルのファイル名は、セルタイプのグローバル名に ’_inline.h' を付加したヘッダファイルとします。
インラインの受け口関数を実装するセルタイプコードを複数のファイルに分けて記述する場合、セルタイプのグローバル名に ’_inline.h' を付加した名前のヘッダファイルからインクルードします。

以下に、セルタイプのネームスペース識別子が nNS::tCelltype である場合のファイル名の例を示します。

【ファイル名の例】

   nNS_tCelltype_inline.h


ファイルの記述内容
................................................

セルタイプコードを格納するファイルには、以下を記述します。

 * セルタイプヘッダファイルのインクルード
 * 受け口関数
 * 受け口関数から呼び出される関数

セルタイプヘッダのインクルード
......................................

セルタイプヘッダは、セルタイプコードからインクルードすべき、TECS ジェネレータの生成したヘッダファイルです。

非インライン受け口関数を実装するセルタイプコードを記述するファイルでは、セルタイプヘッダをインクルードします。
以下にセルタイプ tCelltype の場合の例を示します。

【セルタイプコード記述例】

.. code-block:: c

   #include "tCelltype_tecsgen.h"


セルタイプコードを記述しようとするセルタイプ以外のセルタイプヘッダをインクルードすることはできません。

【補足説明】複数のセルタイプのセルタイプコードを一つのファイルに含めることは想定されていない。C 言語のマクロを駆使して関数の結合先をコンパイル時に決定する TECS の実装では、やむを得ない制限である。

参照できるもの
......................

セルタイプコードの中では、以下のものを参照できます。

これらは、いずれもセルタイプコードを記述しようとするセルタイプの持つものに限られます。

 * 呼び口関数
 * 属性
 * 内部変数

この他に、ライブラリとして提供されるものを参照することができますが、コンポーネントとして提供されるものの代わりにライブラリ参照するのは、望ましくない実装となります。

これ以外のものを参照する場合、逸脱になります。

受け口関数の実装
......................

受け口に対応付けられたシグニチャで定義されたすべての関数を受け口関数として実装します。

受け口関数の名前は、以下のように受け口名と関数名を連結したものとなります。


  (受け口関数名) = (受け口名) + '_' + (シグニチャで定義された関数名)


【補足説明】受け口関数名は、マクロにより、受け口関数のグローバル名に置換される。

セルタイプが非シングルトンの場合、シグニチャで定義された関数ヘッダに比べ、第一引数が挿入されます。
挿入される第一引数の型は、CELLIDX 型です。

以下に受け口関数の形式（関数ヘッダ）の例を示します。

受け口関数 (非シングルトンの場合)
``````````````````````````````````````

【TECS CDL 記述例】

.. code-block:: tecs-cdl

  signature sSignature{
    ER func1( [in]int32_t inval, [out]int32_t *outval );
    ER func2( [in,size_is(size)]const int8_t *buf, [in]int32_t size );
  };
  celltype tCelltype {
    entry sSignature eEntry;
  };

tCelltype のセルタイプコードに記述する必要のある受け口関数

【セルタイプコード記述例】

.. code-block:: c

  ER eEntry_func1( CELLIDX idx, int32_t inval, int32_t *outval )
  ER eEntry_func2( CELLIDX idx, const int8_t *buf, int32_t size )


なお CELLIDX 型が何であるかは、ここでは規定しません。
ポインタ値であったり整数値であったりします。

受け口関数 (シングルトンの場合)
```````````````````````````````````````````
【TECS CDL 記述例】

.. code-block:: tecs-cdl

  [singleton]
  celltype tCelltype {
    entry sSignature eEntry;
  };


【セルタイプコード記述例】

.. code-block:: c

  ER eEntry_func1( int32_t inval, int32_t *outval )
  ER eEntry_func2( const int8_t *buf, int32_t size )


シングルトンの場合、セルを識別するための引数 idx が挿入されません。

受け口関数の形式（受け口配列の場合）
````````````````````````````````````````````

受け口配列の場合、第二引数に配列添数を挿入します。

次に受け口配列の例を示す。以下のような TECS CDL の記述があったとします。

【TECS CDL 記述例】

.. code-block:: tecs-cdl

  signature sSignature{
    ER func1( [in]int32_t inval, [out]int32_t *outval );
    ER func2( [in,size_is(size)]const int8_t *buf, [in]int32_t size );
  };
  celltype tCelltype {
    entry sSignature eEntry[2];
  };


tCelltype のセルタイプコードに記述する必要のある受け口関数の関数ヘッダは、以下のようになります。

【セルタイプコード記述例】

.. code-block:: c

  ER eEntry_func1( CELLIDX idx, int_t subscript, int32_t inval, int32_t *outval )
  ER eEntry_func2( CELLIDX idx, int_t subscript, const int8_t *buf, int32_t size )

CB ポインタ
........................

CB ポインタは、非シングルトンのセルタイプの場合に、セルを選択するために必要となります。
シングルトンのセルタイプでは、CB ポインタを得ることはできません。

以下に、セルタイプが非シングルトンの場合の、受け口関数の中で CB ポインタを得る方法を説明します。
CB ポインタが何物であるかは、ここでは規定しません。

CB ポインタを得るコードの例を以下に示します。

【セルタイプコード記述例】

.. code-block:: tecs-cdl

  CELLCB   *p_cellcb;    /* p_cellcb の名前を変えてはならない */
  if (VALID_IDX(idx)) {
    p_cellcb = GET_CELLCB(idx);
  }
  else {
    return(E_ID);
  }

以下に必須の要件を記します。

 * 非シングルトンセルタイプの場合、CB ポインタを得る
 * CB ポインタの変数名は p_cellcb とする
 * CB ポインタの型は CELLCB 型とする
 * 第一引き数 CELLIDX idx を検査する関数（マクロ）として VALID_IDX を使用する
 * 第一引き数 CELLIDX idx を CB ポインタに変換する関数（マクロ）として GET_CELLCB を使用する
 
先ほどの CB ポインタを得るコードの例にあって、この要件にないのは、VALID_IDX で idx が不正と判断された場合に E_ID を返すことです。
TOPPERS/ASP 系の OS では E_ID を返すのが妥当ですが、戻り値の型が ER や ER_INT でない場合、あるいは TOPPERS/ASP 系以外の　OS で動作させることを目的に記述している場合には、E_ID を返す必要はありません。

【補足説明】実際の実装において idx_is_id が指定されいてない場合、 VALID_IDX が false を返すことはない。

【補足説明】呼び口関数、属性、内部変数のいずれも参照しない場合、p_cellcb は非参照となる。

呼び口関数
.................

セルタイプコードにおいて、呼び口のシグニチャで定義された関数を呼び出し可能です。
呼び口関数は、シグニチャで定義された関数と以下の点で異なります。

 (呼び口関数名) = (呼びけ口名) + '_' + (シグニチャで定義された関数名)


以下に例を示す。以下のような TECS CDL の記述があったとします。

【TECS CDL 記述例】

.. code-block:: tecs-cdl

  signature sSignature{
    ER func1( [in]int32_t inval, [out]int32_t *outval );
    ER func2( [in,size_is(size)]const int8_t *buf, [in]int32_t size );
  };
  celltype tCelltype {
    call sSignature cCall;
  };


tCelltype のセルタイプコードでの呼び口関数の形式は以下のようになります。

【セルタイプコードでの形式の例】

.. code-block:: c

  ER cCall_func1( int32_t inval, int32_t *outval )
  ER cCall_func2( const int8_t *buf, int32_t size )

【補足説明】受け口関数の場合は、第一引き数 idx が挿入されたが、呼び口関数では挿入されない。

呼び口関数（呼び口配列の場合）
......................................

次に呼び口配列の例を示します。以下のような TECS CDL の記述があるとします。

【TECS CDL 記述例】

.. code-block:: tecs-cdl

  signature sSignature{
    ER func1( [in]int32_t inval, [out]int32_t *outval );
    ER func2( [in,size_is(size)]const int8_t *buf, [in]int32_t size );
  };
  celltype tCelltype {
    call sSignature cCall[];
  };


tCelltype のセルタイプコードでの呼び口関数は以下のようになります。

【セルタイプコード記述例】

.. code-block:: c

  ER cCall_func1( int_t subscript, int32_t inval, int32_t *outval )
  ER cCall_func2( int_t subscript, const int8_t *buf, int32_t size )


非配列の場合に比べ、第一引き数に配列添数が加えられます。
配列添数の最小値は 0 です。
配列サイズは、マクロ NCP_cCall (cCall は呼び口名に置き換える) により知ることができます。

【訂正】(2016/11/12) N_CP_cCall は、通常形ですが、引数に p_that を取る場合と、取らない場合がありました。NCP_cCall (短縮形) は、常に引数 p_that を取りません。

属性
..........

セルタイプコードにおいて、属性を参照可能です。
属性参照名は、以下のように属性名に 'ATTR\_' を前置きしたものです。

 (属性参照名) = 'ATTR\_' + (属性名)

以下に例を示します。以下のような TECS CDL の記述があったとします。

【TECS CDL 記述例】

.. code-block:: tecs-cdl

  celltype tCelltype {
    attr {
      int32_t  attribute;
    }
  };

tCelltype のセルタイプコードでの属性参照は以下のようになります。

【セルタイプコード記述例】

.. code-block:: c

  ATTR_attribute


ATTR_attribute は左辺値として扱うことができます。

内部変数
............

セルタイプコードにおいて、内部変数を参照可能です。

内部変数参照名は、以下のように内部変数名に 'VAR\_' を前置きしたものです。

 (内部変数参照名) = 'VAR\_' + (内部変数名)

以下に例を示します。以下のような TECS CDL の記述があったとします。

【TECS CDL 記述例】

.. code-block:: tecs-cdl

  celltype tCelltype {
    var {
      int32_t  variable;
    }
  };


tCelltype のセルタイプコードでの内部変数参照は以下のようになります。

【セルタイプコード記述例】

.. code-block:: c

  VAR_variable

VAR_variable は左辺値として扱うことができます。

非シングルトンセルタイプの場合のセルタイプコードの例
.................................................................

これまでの、セルタイプコードの規則に従ったコードの例を示します。
ここでは、非シングルトンセルタイプの場合を示します。

【TECS CDL 記述例】

.. code-block:: tecs-cdl

  signature sSignature{
    ER func1( [in]int32_t inval, [out]int32_t *outval );
    ER_INT func2( [in,size_is(size)]const uint8_t *buf, [in]int32_t size );
  };
  celltype tCelltype {
    entry sSignature eEntry;
    attr {
      int32_t  attribute;
    };
    var {
      int32_t  variable;
    };
  };

tCelltype のセルタイプコードは以下のようになります。

【セルタイプコード記述例】

.. code-block:: c

  ER eEntry_func1( CELLIDX idx, int32_t inval, int32_t *outval )
  {
    /* CB ポインタを得るコード */
    CELLCB   *p_cellcb;          /* p_cellcb の名前を変えてはならない */
    if (VALID_IDX(idx)) {
      p_cellcb = GET_CELLCB(idx);
    }
    else {
      return(E_ID);
    }

    *out_val = inval - ATTR_attribute;  /* 属性 attribute を参照

    return E_OK;
  };
  ER_INT eEntry_func2( CELLIDX idx, const uint8_t *buf, int32_t size )
  {
    /* CB ポインタを得るコード */
    CELLCB   *p_cellcb;          /* p_cellcb の名前を変えてはならない */
    int32_t  i, sum = 0;
    if (VALID_IDX(idx)) {
      p_cellcb = GET_CELLCB(idx);
    }
    else {
      return(E_ID);
    }

    for( i = 0; i < size; i++ )
	 sum += buf[i];

    return sum;
  };

【補足説明】ATTR_attribute は CB ポインタ p_cellcb を含むマクロであることを想定するが、限定するものではない。実例として、ATTR_attribute ではさらに以下のものを含む。属性は ROM に置かれるが、これを INIB と呼ぶ。CB から INIB へのポインタ参照も ATTR_attribute マクロに含まれる。これは、最適化状態において変わりうる。

【補足説明】VAR_variable は CB ポインタ p_cellcb を含むマクロであることを想定するが、規定するものではない。

シングルトンセルタイプの場合のセルタイプコード
.............................................................

これまでの、セルタイプコードの規定に従ったコードの実例を示します。
ここでは、シングルトンセルタイプの場合を示します。

【TECS CDL 記述例】

.. code-block:: tecs-cdl

  signature sSignature{
    ER func1( [in]int32_t inval, [out]int32_t *outval );
    ER_INT func2( [in,size_is(size)]const uint8_t *buf, [in]int32_t size );
  };
  [singleton]
  celltype tCelltype {
    entry sSignature eEntry;
    attr {
      int32_t  attribute;
    };
    var {
      int32_t  variable;
    };
  };

tCelltype のセルタイプコードは以下のようになります。

【セルタイプコード記述例】

.. code-block:: c

  ER eEntry_func1( int32_t inval, int32_t *outval )
  {
    *out_val = inval - ATTR_attribute;  /* 属性 attribute を参照 */

    return E_OK;
  };
  ER_INT eEntry_func2( const uint8_t *buf, int32_t size )
  {
    int32_t i, sum = 0;

    for( i = 0; i < size; i++ )
	 sum += buf[i];

    return sum;
  };

【補足説明】シングルトンセルタイプのコードでは、idx 引き数がない、CB ポインタを得るコードがない点で、非シングルトンセルタイプのコードと異なる。

【補足説明】ATTR_attribute は INIB 構造体名を含むマクロであることを想定するが、規定するものではない。

【補足説明】VAR_variable は CB 構造体名を含むマクロであることを想定するが、規定するものではない。
