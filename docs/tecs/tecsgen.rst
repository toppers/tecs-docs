.. _tecscmd-tecsgen:

tecsgen コマンドリファレンス
=================================

名前
---------

tecsgen  -- TECS ジェネレータ

使用方法
---------------

以下の、使用方法があります．

tecsgen を呼出す
````````````````````````

% tecsgen [OPTION] CDL-File

明示的に exerb 版を呼出す
````````````````````````````````

V1.3 以降 exerb 版は、サポートされなくなりました。

% tecsgen.exe [OPTION] CDL-File

実行モジュールの拡張子 .exe を付加して呼び出します．
Windows 上のみで使用可能です．Ruby インタプリタをインストールすることなく用いることができます。

明示的に Ruby スクリプトを呼出す
````````````````````````````````````````

% ruby [PATHtoTECSGEN]/tecsgen.rb CDL-File

[PATHtoTECSGEN] は TECS ジェネレータ (tecsgen) のインストールディレクトリへのパスです．
この呼出し形式は、TOPPERS プロジェクトで作成された各種パッケージで、見らることがあります。

説明
-------------

TECS ジェネレータ tecsgen は、TECS コンポーネント記述言語 (TECS CDL) に基づき記述された CDL-File を入力とし、インタフェースコードなどを生成します．

以下のオプションを指定できます．

    -D, --define=def
        import_C でヘッダファイルを取込む際の C のプリプロセッサに与え
        るマクロ (define) を定義します．ここで指定されたものは tecsgen
        の出力 Makefile.templ のコンパイルコマンドの引数に引き継がれま
        す．
        -D は複数指定することができます．
   
    -G, --generate-region=path
        コード生成するリージョンを限定します．指定されたリージョンのみ
        コード生成されます．-G を繰り返すことで、複数のリージョンを指定
        することができます．コード生成するリージョンからコード生成しな
        いリージョンへの結合は、エラーとなります．
   
    -I, --import-path=path
        import で取込む CDL ファイルのパス、および import_C でヘッダファ
        イルを取込む際に C のプリプロセッサに与える　include パスを指
        定します．
        tecsgen の引数で指定された CDL ファイルを取込む際にも、このオ
        プションで指定されたパスをサーチします．
        ここで指定されたものは tecsgen の出力 Makefile.templ のコンパ
        イルコマンドの引数に引き継がれます．
        -I は複数指定することができます．
   
    -L, --library-path=path
        ruby のライブラリパスを指定します．環境変数 RUBYLIB でも指定で
        きます．generator/tecslib へのパスが指定される必要があります．
   
    -R, --RAM-initializer
        RAM の初期値を設定するための初期化コードが生成されます．本オプ
        ションが指定された場合 RAM 領域は未初期化変数として出力される
        ため、初期化コードを実行する必要があります．初期化コード
        INITIALZE_TECS() (global_tecsgen.h にマクロ定義) を呼び出す
        ことにより初期化されます．[[BR]]
        RAM only オプション -r が指定された場合、本オプションは無視さ
        れます．[[BR]]
        tecsgen V1.2.* までの初期化コードは INITIALZE_TECSGEN() でし
        た。tecsgen V1.3 以降でも INITIALZE_TECS() の別名として
        INITIALZE_TECSGEN() が定義されます。
        tecsgen V1.3 以降では -R の指定に関わらず INITIALZE_TECS()マク
        ロが定義されます。-R の指定に関わらず、TECS コンポーネントを呼
        び出す前に INITIALZE_TECS() を呼び出すようにしてください。
   
    -U, --unoptimize
        最適化を無効にします．
   
    -c, --cpp=cpp_cmd
        C プリプロセッサコマンドを指定します．デフォルトでは
        'gcc -E -D TECSGEN' です．環境変数 TECS_CPP により指定することが
        できます．[[BR]]
        tecsgen V1.2.* までのデフォルトは 'gcc -E -D TECS' でした．
   
    -d, --dryrun
        処理を実行しますがインタフェースコードは生成されません．TECS 
        コンポーネント記述の文法誤りをチェックすることができます．
   
    -f, --force-overwrite
        出力を強制上書きします．デフォルトでは、内容に変化のあった出力
        ファイルのみ更新します．
   
    -g, --gen=dir
        インタフェースコードなどを生成するディレクトリを指定します．デ
        フォルトでは、カレントディレクトリの下の 'gen' ディレクトリに
        出力されます．
   
    -i, --idx_is_id
        すべての celltype で指定子 idx_is_id が指定されたものとして扱
        います．
   
    -k, --kcode=code
        文字コードを指定します．code は euc, sjis, none, utf8 のいずれ
        かを指定可能です．デフォルトは euc です．
        (exerb 版では sjis がデフォルトになります)
   
    -r, --ram
        RAM のみで動作するコードを生成します．デフォルトでは attribute 
        など ROM (const)領域に配置するコードが生成されます．
   
    -s, --show-tree
        パースツリーを表示します．
        tecsgen のデバッグに使用します．
   
    -t, --generator-debug
        tecsgen のデバッグする場合に使用します．パーサーが取込んだトー
        クンを逐次表示します．コード生成段階で内部エラーが発生した場合
        には、スタックトレースを表示します．
        factory はコード生成時にエラーが発生することがあります．その場
        合、どのfactory でエラーが発生したかを知るための情報が表示され
        ます．
   
    -u, --unique-id
        idx_is_id により付与される ID （整数）は、デフォルトでは各セル
        タイプごとに 1 から始まる番号が割付けられます．本オプションが
        与えられた場合、すべてのセルで異なる ID が割付けられます．
   
    -v, --verbose
        いくらかの情報を出力します．
        ・プロトタイプ宣言されているが、存在しないセル
        ・ロードするプラグイン
        ・through により実行される ruby スクリプト
        ・C プリプロセッサコマンド
        ・セルタイプごとの実施された最適化
   
    -y, --yydebug
        tecsgen のパーサー部をデバッグするために使用します．bnf.tab.rb 
        のかわりに bnf-deb.tab.rb が使用されます．
   
    --no-banner
        バナーを表示しません．
   
    --version
        tecsgen の version を表示します．
   
    --generate-all-template
        すべてのセルタイプのテンプレートを生成します．
        デフォルトでは tecsgen は、セルが一つも生成されないセルタイプ、
        再利用されているセルタイプ（import時、山括弧文字列 <file.cdl> 
        指定されている）のテンプレートを生成しません．
   
    --generate-no-template
        テンプレートを生成しません（セルタイプ、 Makefile とも）．
        オプション --generate-all-template と同時指定された場合、このオプションが
        優先されます．
   
    --no-default-import-path
        デフォルトでは、環境変数 $TECSPATH で示されるディレクトリ、およ
        びそのディレクトリ直下のディレクトリが import および import_C
        で取り込む場合のサーチパスに含まれますが、本オプションを指定し
        た場合、それらのディレクトリはサーチパスに含まれません．
   
    --c-suffix=c
        生成する C 言語のソースファイルのサフィックスを指定されたものに、
        変更します．C++ 用のソースファイルとして扱いたい場合、cc や
        cpp を指定します．
    
    --h-suffix=h
        生成する C 言語のヘッダファイルのサフィックスを指定されたものに、
        変更します．このオプションを指定した場合、factory で生成される
        ヘッダファイル名が不一致になる可能性がある点に注意してください．

以下のものが出力されます．

 * ヘッダファイル (global_tecsgen.h, CELLTYPE_tecsgen.h, CELLTYPE_factory.h, SIGNATURE_tecsgen.h)
 * セルタイプtecsgenコード  (CELLTYPE_tecsgen.c)
 * セルタイプコードテンプレート (CELLTYPE_templ.c, CELLTYPE_inline_temple.h)
 * Makefile  (Makefile.templ, Makefile.tecsgen, Makefile.depend)
 * 中間ファイル
   * プラグインにより生成されるコンポーネント記述
   * 取込まれる C のヘッダファイル

終了ステータス
----------------------

 *  0 … 正常終了
 *  1 … エラー

エラーには、CDL ファイルの文法誤りの他、入力ファイルの読み込みや出力ファイルの作成の失敗があります．
警告 (warning) の発生は、エラーとはみなされません．

言語および文字コードの決定
------------------------------

言語および文字コードの指定は、tecsgen への入力と出力で対応が異なります．

入力については、文字コードの指定が sjis の場合を除いて、tecsgen は、CDL ファイルの文字コードを ASCII-8BIT とみなして読み込みます．
ファイルが sjis の場合に限っては、第二バイトに '\' が含まれることがあり、そのような文字が " (ダブルクオート) の直前にあるとエスケープされてしまい、期待したとおりに動作しないため、sjis の場合には入力ファイルの文字コードを認識して処理を行います．

出力については、コンソールに出力されるエラーメッセージ、gen ディレクトリに生成されるファイルの両方で、言語、文字コードの指定が影響します．

tecsgen は、文字コードの指定を以下の順に調べていき、最後に設定されていたものの言語および文字コードの指定が有効となります．

 * codepage (exerb 版かつ TERM 環境変数未設定または TERM=cygwin の場合のみ)
 * 環境変数 LANG
 * 環境変数 TECSGEN_LANG, TECSGEN_FILE_LANG
 * オプション -k

TECSGEN_LANG はエラーメッセージ、ファイル文字コードの両方に影響します．
ただし、LANG と TECSGEN_LANG が相違する場合、エラーメッセージが正しく表示されない可能性が高いので、よくわからない場合は設定しないようにしてください．

TECSGEN_FILE_LANG はファイル文字コードのみ影響します．

-k で euc, sjis が指定された場合、TECSGEN_FILE_LANG=ja_JP.eucJP または ja_JP.sjis が仮定されます．
utf8, none が指定された場合は、それ以前に決定された言語が選択されます．

現在の実装では、環境変数 LANG, TECSGEN_LANG, TECSGEN_FILE_LANG の有効な値は、以下の通りです．

 * 言語: C, en_US, ja_JP
 * 文字コード： utf8(utf-8), iso8859-1, sjis, eucJP

大文字、小文字は区別されません．
これ以外が指定された場合、C.ISO8859-1 (内部的には en_US.ASCII-8BIT) が仮定されます．

環境変数
-------------

tecsgen は、以下の環境変数を参照します．

TECSPATH
```````````````

【補足説明】TECS ジェネレータ V1.2.1.4 以降、TECSPATH は、必ずしも設定する必要はありません。tecsgen/tecs へのパスは TECS ジェネレータの所在するパスから割り出されます(exerb 版を除く)。テストコードをビルドする際には、C コンパイラのヘッダパスを指定するために必要です。

tecsgen/tecs の所在するディレクトリへのパスを指定します．
TECSPATH で示されるディレクトリ、およびそのサブディレクトリは、import および import_C のサーチパス (-I) の末尾に加えられます．

Makefile.templ を出力する際に、TECSPATH の設定値が、$(TECSPATH) に置き換えられます．

tecsgen を B-shell 上で使用する場合、tecsgen/set_env.sh を、set_env.sh の所在するディレクトリで、以下のようにシェルに読み込ませると環境変数 TECSPATH がセットされます．

  % source set_env.sh

Windows のコマンドプロンプト上では、tecsgen/set_env.bat を、set_env.bat の所在するディレクトリで、以下のように実行することで、環境変数 TECSPATH がセットされます．

  !>> set_env.bat

TECS_CPP
```````````````

C プリプロセッサを指定します。オプション -c (--cpp) の説明を参照してください．

言語および文字コードに影響する環境変数
`````````````````````````````````````````````

文字コードを決定する際に、以下の環境変数を参照します．

  LANG, TECS_LANG, TECS_FILE_LANG, TERM

「言語および文字コードの決定」の項を参照してください．
