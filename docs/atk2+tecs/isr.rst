
.. _atk2+tecs-isr:

割込み管理　－`tISR`
=================

割込みサービスルーチン（割込み処理関数）を登録して、割込み発生時に呼び出す機能です。

.. todo::
    to be filled in

使用方法
--------

割込みの生成
^^^^^^^^^^^^

アプリケーション開発者は `tISR` セルタイプのセルを生成することにより、タスクを生成することができます。次の例では ``MyISR`` という名前のタスクセルを生成し、 ``MyCell`` の ``eISRBody`` をメインルーチンとして結合しています。

.. code-block:: tecs-cdl
  :caption: app.cdl

  celltype tMyCellType {
      entry sHandlerBody eISRBody;
  };

  cell tMyCellType MyCell {};

  cell tISR MyISR {
      cBody = MyCell.eISRBody;
      category = 2;
      priority = 15;
      entryNumber = 48;
      interruptsource ="ENABLE";
  };

.. code-block:: c
  :caption: tMyCellType.c

  void eISRBody_main(CELLIDX idx)
  {
  }

割込みの管理
^^^^^^^^^^^^

 リファレンス
------------

セルタイプ
^^^^^^^^^^

.. tecs:celltype:: tISR

  割込みの生成を行うコンポーネントです。

  .. tecs:attr:: char_t *name = "$cell$"

    割込みの名前をしていしましす。
    指定しない場合、セルの名前が使用されます。

  .. tecs:attr:: uint32_t category

    割込みのカテゴリを指定します。

    .. c:macro:: 1

     カテゴリ1ISR(C11SR）
     OSのコードを経由せずに高速に呼び出される
     割込み制御関連以外のOSのシステムサービスを呼び出せない
     C11SRは，C21SRよりも割込み優先度が高い
  
    .. c:macro:: 2

     カテゴリ2ISR(C21SR）
     OSのコードを経由して呼び出される
     OSのサービスを呼び出せる

  .. tecs:attr:: uint32_t priority

    割込みの優先度を指定します。

  .. tecs:attr:: uint32_t entryNumber

    割込み番号を指定します。

  .. tecs:attr:: char_t *interruptsource

    割込み要因の初期状態を指定します。
    SC3、SC4のみで使用可能です。 
    categoryに1を指定した場合に、本パラメータにDISABLEを指定した場合、ジェネレータはエラーを検出します。
    SC3、SC4で本パラメータを省略した場合、ジェネレータはエラーを検出します。 

   .. c:macro:: ENABLE

      有効

    .. c:macro:: DISABLE

      無効 

  .. tecs:attr:: char_t *resource

    割込みが獲得するリソースを選択します（複数選択可能）。

シグニチャ
^^^^^^^^^^

.. tecs:signature:: sHandlerBody

  割込みハンドラを呼び出すためのシグニチャです。

  .. tecs:sigfunction:: void main(void)
      todo





