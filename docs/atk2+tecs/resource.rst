.. _atk2+tecs-resource:

カーネル ― `tResource`
=================


.. todo::
    to be filled in

使用方法
--------

リソースの生成
^^^^^^^^^^^^
アプリケーション開発者は `tResource` セルタイプのセルを生成することにより、リソースを生成することができます。次の例では ``MyResource`` という名前のリソースセルを生成し、 ``MyCell`` の ``cResource`` をメインルーチンとして結合しています。

.. code-block:: tecs-cdl
  :caption: app.cdl

  celltype tMyCellType {
      call sResource cResource;
  };

  cell tMyCellType MyCell {};

  cell tTask MyResource {
      property = "STANDARD";
      linkedResource = "OMISSIBLE";

      eResource = MyCell.cResource;
  };

.. code-block:: c
  :caption: tMyCellType.c


リファレンス
------------

セルタイプ
^^^^^^^^^^

.. tecs:celltype:: tResource
	リソースの生成を行うコンポーネントです。

  .. tecs:attr:: int8_t id = C_EXP("$ID$")
	リソースのIDの識別子を指定します。

  .. tecs:attr:: char_t *name = "$cell$"
  	リソースの名前を指定します。

  .. tecs:attr:: char_t *property
  	リソースの種類を指定します。

	.. c:macro:: STANDARD
		標準リソース
    .. c:macro:: INTERNAL
    	内部リソース
	.. c:macro:: LINKED
		リンクリソース


  .. tecs:attr:: char_t *linkedResource
  	リンクリソースにおけるリンク先リソースを指定します。



シグニチャ
^^^^^^^^^^

.. tecs:signature:: sResource
	リソースを操作するためのシグニチャ。

	.. tecs:sigfunction:: StatusType get(void)
		リソースを獲得する。

	.. tecs:sigfunction:: StatusType release(void)
		リソースを開放する。