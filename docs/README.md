
TECS / ASP3+TECS ドキュメントの書き方
=================================

スタイルの微調整
-------------

### 表の背景色が交互に変わらないようにする

    .. rst-class:: no-alt-color

    +---------+---------+
    | column1 | column2 |
    +=========+=========+
    ...

`no-alt-color` は `_static/style.css` で定義されています。

TECS固有のマークアップ
-------------------

`code-block` の言語として `tecs-cdl` を使用できます。これを使用すると、TECS コンポーネント記述言語を対象としたシンタックスハイライトが適用されるようになります。
この機能は `tecslexer` Sphinx 拡張により提供されています。

    .. code-block:: tecs-cdl
      (insert TECS CDL code here)

リファレンスマニュアルのような形式で TECS のオブジェクトの説明を行う際は、以下のマークアップを使用して下さい。
これらは `tecs` Sphinx 拡張により提供されています。

    .. tecs:celltype:: nNamespace1::nNamespace2::tCellTypeName

      blah blah

      .. tecs:attr:: Type attributeName
      .. tecs:var:: Type variableName
      .. tecs:entry:: sSignature eEntryPortName
      .. tecs:call:: sSignature cCallPortName

        blah blah

    .. tecs:signature:: sSignatureName

      blah blah

      .. tecs:sigfunction:: ReturnType functionName(int functionParams)

        blah blah

これらのマークアップは、対応するインラインマークアップを用いることで、リンクを張ることができます。

    :tecs:attr:`tCellTypeName::attributeName` : tCellTypeName::attributeName と表示されます。
    :tecs:attr:`~tCellTypeName::attributeName` : attributeName と表示されます。
    :tecs:attr:`hoge <tCellTypeName::attributeName>` : hoge と表示されます。 TODO: 要検証
