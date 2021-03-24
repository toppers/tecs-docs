
TECS / ASP3+TECS ドキュメント
===========================

Getting Started
---------------

本ドキュメントのコンパイルにはSphinx等のPython製ツールを使用しています。Sphinx等のPythonパッケージをインストールする方法は複数あります。

### Pipenv

[Pipenv](https://github.com/kennethreitz/pipenv)はPythonプロジェクトの依存関係の管理を容易化するシステムです。Pipenvをインストール後、このディレクトリで以下のコマンドを実行して下さい。

    pipenv install
    pipenv shell

これにより、専用の環境 (`virtualenv`) が作成され、その中でサブシェルが起動します。依存パッケージは自動的にインストールされます。

### Virtualenv

TODO

### global環境へのインストール

`requirements.txt` に、必要なソフトウェアと対応バージョンの一覧が含まれています。以下のコマンドを使用することで、これらを一括でインストールすることができます。

    pip install -r requirements.txt

この方法でインストールする場合、環境によってインストール済みのパッケージやバージョンの集合が微妙に異なったものになり、これが原因でトラブルが発生する可能性がある為、注意が必要です。これが理由で、global環境へのインストールは推奨されません。

Building
--------

### HTML

以下のコマンドでHTML版ドキュメントをビルドできます。

    make html

もしくは、ソースを変更する度に自動でビルドし、ブラウザで表示したい場合 (ライブプレビュー) は以下のコマンドを使用します。

    make livehtml

### PDF

以下のコマンドでPDF版ドキュメントをビルドできます。

    make latexpdfja

PDF出力にはpLaTeXが必要となります。予め `platex` にパスが通っていることを確認してください。

note: 現時点では一部環境で組版に失敗しますが、発生条件や解決方法は不明です。

Read the Docsで日本語テキストを含むドキュメントをPDF出力することは[できず](https://github.com/rtfd/readthedocs.org/issues/1959#issuecomment-175960871)、コミュニティーエフォートとマークされています。このため、PDF版についてはRead the Docsの外側で別途配布するという方針となりました。


書き方
------

### reStructuredText の書き方

SphinxはreStructuredText (以下 reST) を利用したドキュメンテーションシステムです。この為、ドキュメントはreSTで記述しますが、SphinxではreSTの書き方について独自のガイドラインを定めています。この為基本的な書き方についてはreSTの仕様ではなく、Sphinxドキュメンテーションの[reStructuredText Primer](http://www.sphinx-doc.org/en/stable/rest.html)を参照することを推奨します。

Sphinxには多くの有用な機能が含まれています。以下は本ドキュメントで特に有用と思われる機能のドキュメントの一覧です。

- **ドメイン** - APIを記述するのに有用
    - [Sphinx Domains/The C Domain](http://www.sphinx-doc.org/en/stable/domains.html#the-c-domain)

### 和文にインラインマークアップを適用する際のアドバイス

通常、reST のインラインマークアップ (e.g., ``**strong emphasis**``) は両側にスペースを空ける必要があり、日本語等の[分かち書き](https://ja.wikipedia.org/wiki/わかち書き)を行わない言語では問題となります。

この場合、スペースをバックスラッシュでエスケープすることによりこの制約を回避することができます。例えば、

    使用方法の一つとして\ :ref:`タスクを通知先とする場合 <asp3tecs-timeeventnotifier-task>`\ を例として…

このreSTテキストは次のように表示されます。

> 使用方法の一つとしてタスクを通知先とする場合を例として…

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
