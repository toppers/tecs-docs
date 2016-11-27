初期化コード
========================

TECS のコードが実行される前に、以下のマクロを呼び出して初期化を行います。

.. code-block:: c

  INITILIZE_TECS()


INITILIZE_TECS は、必要に応じて以下を行います。

 * 内部変数の初期化
 * CB から INIB へのポインタ設定

初期化を行う前に TECS のコードが実行された場合の振る舞いは、未定義です。

【補足説明】TECS ジェネレータ V1.2.* まで INITIALZE_TECSGEN であったが、V1.3.0.0 以降、INITIALIZE_TECS に変更となった。ただし INITIALIZE_TECSGEN を INITIALIZE_TEcS に置換するマクロが定義されるため、従来のコードも期待した通りにコンパイル、リンクスうることができる。

【補足説明】TECS ジェネレータ V1.2.* まで、INITIALIZE_TECS() は TECS ジェネレータにオプション -R が指定された時だけ生成されていたが、V1.3.0.1 以降、常に生成される。ただし -R が指定されていない場合、INITIALIZE_TECS()の内容は空であり INITIALIZE_TECS() が呼び出されない従来のコードも動作する。ただし、将来においても成り立つとは限らない。

