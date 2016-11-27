FOREACH_CELL マクロ
===============================

セルタイプコードにおいて、そのセルタイプに属するすべてのセルの変数を操作を行うために FOREACH_CELL マクロを使用できます。
主として、初期化の際に用います。

FOREACH_CELL マクロの使用
......................................

すべてのセルに対する操作を行うには、FOREACH_CELL マクロで始め END_FOR_EACHCELL で終わるループにより実現できます。
以下にコードの例を示します。

.. code-block:: c

  #include "tCelltype_tecsgen.h"

  ...

  func()
  {
    /* tCelltype のすべてのセルについて初期値を作業変数に移す */

    CELLCB  *p_cellcb;          /* 短縮形で属性、内部変数を参照するために p_cellcb とします */
    int      i;                 /* ループ変数を用意する必要があります．名前は適当で構いません */

    FOREACH_CELL(i,p_cellcb)	/* FOREACH_CELL でループの開始を宣言します */
      VAR_a0 = ATTR_a;		    /* 短縮形 VAR_a0, ATTR_a で変数、属性参照できます */
      VAR_b0 = ATTR_b;
    END_FOREACH_CELL
  }

FOREACH_CELL マクロの多重使用
........................................

FOREACH_CELL マクロを多重ループで用いることができます。
この場合、内側のループ内では外側のループのセルの属性、変数には直接アクセスすることはできません。
外側のループの属性、変数は別の自動変数に写し取ることで、内側のループで参照できます。

.. code-block:: c

  #include "tCelltype_tecsgen.h"

  ...

  func()
  {
    CELLCB  *p_cellcb;          /* 短縮形で属性参照するために p_cellcb としました */
    int      i;

    FOREACH_CELL(i,p_cellcb)
      CELLCB   *p;              /* p としたので短縮形で属性参照できません */
      int      j;		/* 内側のループ変数を j とします */
      FOREACH_CELL(j,p)
        /* 外側のループには短縮形が使えるが、内側のループはセルタイプのグローバル名を伴うマクロを使用 */
        if ( ATTR_a == tCelltype_ATTR_a( p ) ) {
	   ... 
	}
      END_FOREACH_CELL
    END_FOREACH_CELL
  }



