.. _CDLref:

概要
----------------

TECS コンポーネント記述言語 (TECS CDL) の記述方法について、説明します。

 * :ref:`cdlref-undoc`

対応バージョン
----------------

TECS ジェネレータ V1.3.1.0 の実装に対応します。

共通事項
-------------

TECS CDL 全体にわたり共通する仕様を説明します。
TECS CDL の文法は、C 言語の文法と親和性のあるものとなっています。

 * CDL ファイル
     TECS CDL は CDL ファイルに格納します。
     CDL ファイルの拡張子は '.cdl' です。
     CDL ファイルは、通常文字コードとして UTF-8 を用います。しかし、7bit ASCII を含む文字コードであれば、他の文字コードも可能です。
     ただし sjis のようにマルチバイト文字の2バイト目以降に特殊な文字が来る可能性のある文字コードは、扱えるとは限りません。
 * :ref:`CDLref-lex`
 * :ref:`CDLref-type`
 * :ref:`CDLref-expression`
 * :ref:`CDLref-scope`
 * :ref:`CDLref-names`

【補足説明】TECS ジェネレータ V1.3.0.1 の実装では、sjis, euc, utf-8, 8bit-ASCII を扱うことができます。

TECS CDL の記述内容
-------------------

TECS CDL に記述する内容には、以下のものがあります。
前方参照に制約があるため、基本的には、以下の順序で記述します。前方参照とならない場合には、この順序に限定されません。

 * :ref:`CDLref-preface`
 * :ref:`CDLref-signature`
 * :ref:`CDLref-celltype`
 * :ref:`CDLref-composite`
 * :ref:`CDLref-cell`

シグニチャ、セルタイプ、複合セルタイプの名前衝突を防ぐ目的で、ネームスペース記述を用いることができます。
セル（間接的にセルタイプを含む）のレイアウト、および名前衝突を防ぐ目的で、リージョン記述を用いることができます。

 * :ref:`CDLref-namespace`
 * :ref:`CDLref-region`

