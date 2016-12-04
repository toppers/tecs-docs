.. _IMPref-macros:

マクロ
=================

以下に、TECS ジェネレータが生成し、セルタイプコードで使用可能なマクロの一覧を記します。
セルタイプコードを記述する場合、短縮形を用います。

+------------------------+-------------------+---------------------------+
|  マクロ                |  短縮形           | 通常形                    |
+========================+===================+===========================+
| IDXの正当性チェック    | VALID_IDX         | tCelltype_VALID_IDX       |
+------------------------+-------------------+---------------------------+
| セルCBを得るマクロ     | GET_CELLCB        | tCelltype_GET_CELLCB      |
+------------------------+-------------------+---------------------------+
| 属性アクセスマクロ     | ATTR_attribute    | tCelltype_ATTR_attribute  |
+------------------------+-------------------+---------------------------+
| 内部変数アクセスマクロ | VAR_variable      | tCelltype_VAR_variable    |
+------------------------+-------------------+---------------------------+
| 呼び口関数マクロ       | cCall_func        |                           |
+------------------------+-------------------+---------------------------+
| 受け口関数マクロ       | eEntry_func       | tCelltype_eEntry_func     |
+------------------------+-------------------+---------------------------+
| 呼び口関数マクロ       | cCall_func        |                           |
+------------------------+-------------------+---------------------------+
| 呼び口配列サイズマクロ | NCP_cCall         | N_CP_cCall                |
+------------------------+-------------------+---------------------------+
| FOREACH_CELLマクロ     | FOREACH_CELL      |                           |
+------------------------+-------------------+---------------------------+

この表では、一例を示しています。
以下のような置き換えが必要です。

 * attirbute は属性名に置き換える
 * variable は内部変数名に置き換える
 * func は関数名に置き換える
 * cCall は呼び口名に置き換える
 * eEntry は受け口名に置き換える
 * tCelltype はセルタイプ名に置き換える

短縮形マクロ
------------------------

短縮形マクロは、通常形に優先して使用されることが意図されています。
また、テンプレートコードは、短縮形の使用を意図して生成されています。
属性・変数参照マクロでは CELLCB へのポインタが p_cellcb という名前で定義されることが仮定されています。

セルCBを得るマクロ(短縮形)
------------------------------------

セル CB を得るマクロは、GET_CELLCB です。

【マクロ定義例】

.. code-block:: c

 #define GET_CELLCB(idx)  tAttribute_GET_CELLCB(idx)

IDXの正当性チェックマクロ（短縮形）
------------------------------------

IDXの正当性チェックマクロは VALID_IDX です。

【マクロ定義例】

.. code-block:: c

 #define VALID_IDX(IDX)  tAttribute_VALID_IDX(IDX)

属性アクセスマクロ(短縮形)
------------------------------------

属性アクセスマクロは、接頭辞 'ATTR\_' に属性名を結合した名前です。

【マクロ定義例】

.. code-block:: c

 #define ATTR_size           	((p_cellcb)->_inib->size)
 #define ATTR_size_array     	((p_cellcb)->_inib->size_array)
 #define ATTR_ptr            	((p_cellcb)->_inib->ptr)

内部変数アクセスマクロ(短縮形)
------------------------------------

内部変数アクセスマクロは、接頭辞 'VAR\_' に属性名を結合した名前です。

【マクロ定義例】

.. code-block:: c

 #define VAR_sz_array        	((p_cellcb)->sz_array)

呼び口配列の大きさを得るマクロ（短縮形）
------------------------------------------

呼び口配列の大きさを得るマクロは、接頭辞 'NCP\_' に呼び口名を結合した名前です。
呼び口が配列の場合のみ、このマクロが生成されます。

【マクロ定義例】

.. code-block:: c

  #define NCP_carray    (2)


【訂正】(2016/11/12) 本マニュアルの最初の公開時(以前のTECS 仕様書においても)、呼び口配列の大きさを得るマクロについて、(NCP_cCall ではなく) N_CP_cCall としていましたが、これは引数を取る場合と、取らない場合がありました。シングルトン、または配列添数が定数の場合に引数を取りませんでした。なお、TECS ジェネレータの生成するテンプレートのコメントは、以前から NCP_cCall の形式となっていました。

オプショナル呼び口テストマクロ（短縮形）
------------------------------------------

呼び口配列の場合、このマクロで結合をチェックする前に、呼び口配列の大きさが1以上であることを確認してください。

【マクロ定義例】

.. code-block:: c

  #define is_cCall_joined      ((p_cellcb)->_inib->cCall!=0)

通常形マクロ
------------------------------------------

通常形のマクロは、他のセルの属性、変数を参照するために使用することが意図されています。

IDXの正当性チェックマクロ
------------------------------------------

【マクロ定義例】

.. code-block:: c

 #define tAttribute_VALID_IDX(IDX) (1)

セルCBを得るマクロ
------------------------------------------

【マクロ定義例】

.. code-block:: c

 #define tAttribute_GET_CELLCB(idx) (idx)


属性アクセスマクロ
------------------------------------------

【マクロ定義例】

.. code-block:: c

 #define tAttribute_ATTR_size( p_that )	((p_that)->_inib->size)
 #define tAttribute_ATTR_size_array( p_that )	((p_that)->_inib->size_array)
 #define tAttribute_ATTR_ptr( p_that )	((p_that)->_inib->ptr)

 #define tAttribute_GET_size(p_that)	((p_that)->_inib->size)
 #define tAttribute_GET_size_array(p_that)	((p_that)->_inib->size_array)
 #define tAttribute_GET_ptr(p_that)	((p_that)->_inib->ptr)


変数アクセスマクロ
------------------------------------------

【マクロ定義例】

.. code-block:: c

 #define tAttribute_VAR_sz_array	((p_cellcb)->sz_array)

 #define tAttribute_GET_sz_array(p_that)	((p_that)->sz_array)
 #define tAttribute_SET_sz_array(p_that,val)	((p_that)->sz_array=(val))


オプショナル呼び口テストマクロ
------------------------------------------

呼び口配列の場合、このマクロで結合をチェックする前に、呼び口配列の大きさが1以上であることを確認すること。

【マクロ定義例】

.. code-block:: c

  #define tCelltype_is_cCall_joined(p_that)      ((p_that)->_inib->cCall!=0)



