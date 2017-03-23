
TECS / ASP3+TECS ドキュメント
===========================

Getting Started
---------------

本ドキュメントのコンパイルにはSphinx等のPython製ツールを使用しています。Sphinx等のPythonパッケージをインストールする方法は複数あります。

### Pipenv

[Pipenv](https://github.com/kennethreitz/pipenv)はPythonプロジェクトの依存関係の管理を容易化する実験的なシステムです。Pipenvをインストール後、このディレクトリで以下のコマンドを実行して下さい。

    pipenv install
    pipenv shell

これにより、専用の環境 (`virtualenv`) が作成され、その中でサブシェルが起動します。依存パッケージは自動的にインストールされます。

### Virtualenv

TODO

### global環境へのインストール

`requirements.txt` に、必要なソフトウェアと対応バージョンの一覧が含まれています。以下のコマンドを使用することで、これらを一括でインストールすることができます。

    pip install -r requirements.txt

この方法でインストールする場合、環境によってインストール済みのパッケージやバージョンの集合が微妙に異なったものになり、これが原因でトラブルが発生する可能性がある為、注意が必要です。これが理由で、global環境へのインストールは推奨されません。


書き方
------

### スタイルの微調整

#### 表の背景色が交互に変わらないようにする

    .. rst-class:: no-alt-color

    +---------+---------+
    | column1 | column2 |
    +=========+=========+
    ...

`no-alt-color` は `_static/style.css` で定義されています。

### TECS固有のマークアップ

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
