.. _CDLref-preface:

前置部
==========

型定義など、前方参照できないため、参照される前に記述する必要があります。

前置部には、以下のものを記述することができます。

 * :ref:`CDLref-import_C`
 * :ref:`CDLref-import`
 * :ref:`CDLref-typedef`
 * :ref:`CDLref-struct`
 * :ref:`CDLref-enum`
 * :ref:`CDLref-const`

.. _CDLref-import_C:
   
C 言語ヘッダのインポート(import_C)
-----------------------------------------------

C 言語で記述したヘッダファイルをインポートするには import_C を用います。

【記述例】

.. code-block:: tecs-cdl

      import_C( "my_header.h" );


実際に取り込まれるのは、型定義 (typedef) だけです。

マクロ定義 (#define) を含め、その他の記述は、取り込まれません。

【注意】　マクロ定義の参照には C_EXP を用いる。セルタイプの属性の項を参照。

【注意】　C++ 言語のヘッダファイルを取り込むことは、できない。

.. _CDLref-import:

CDL ファイルのインポート(import)
----------------------------------------------

CDl ファイルをインポートするには import を用います。

CDL ファイルを再利用する部分と、アプリケーション固有の部分に分けて記述する場合や、
CDL ファイルを分割して記述したい場合に用います。

再利用する部分の CDL ファイルをインポートするには、以下のように記述します。

【記述例】

.. code-block:: tecs-cdl

      import( <reusable.cdl> );


【補足】この場合、resuable.cdl 内に記述されたセルタイプは、すでに作成済とみなされ、TECS ジェネレータはテンプレートファイルを生成しない。

CDL ファイルを分割して記述したい場合は、以下のように記述します。

【記述例】

.. code-block:: tecs-cdl

      import( "appl.cdl" );


【補足】この場合 appl.cdl 内に記述されたセルタイプは、開発中とみなされ、TECS ジェネレータはテンプレートコードを生成する。

.. _CDLref-typedef:

型定義(typedef)
-----------------------------------------------

型定義は、C 言語と同様です。

【記述例】

.. code-block:: tecs-cdl
        
      typedef  double64_t LengthM;
      typedef  double64_t WeightKg;
      typedef  int64_t    size64_t;

.. _CDLref-struct:

構造体(struct)
-----------------------------------------------

構造体のタグとメンバーの記述は、C 言語と同様です。

【記述例】

.. code-block:: tecs-cdl

      struct tag {
        int8_t  count;
      };


【補足】構造体変数を定義することはできません。

.. _CDLref-enum:

列挙 (enum)
-----------------------------------------------

【注意】実装されていません。

.. _CDLref-const:

定数(const)
-----------------------------------------------

定数は、C 言語の定数と同様に記述します。

【記述例】

.. code-block:: tecs-cdl

     const double64_t PI = 3.14159265;

定数は、CDL ファイル内の式を記述するところで参照できます。

【補足】TECS ジェネレータは、定数を global_tecsgen.h のマクロとして出力する。


