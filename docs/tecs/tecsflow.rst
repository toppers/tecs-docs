.. _tecscmd-tecsflow:

tecsflow コマンドリファレンス
=================================

名前
------

tecsflow  -- TECS 呼出しフロー解析器

使用方法
-------------

% tecsflow [-g gen_dir]

説明
-------

TECS フロー解析ツール tecsflow は、アクティブなセルタイプに属するセル
の呼び口関数を起点とする、関数単位の呼出しフローを解析します。

より具体的には、タスクやハンドラの呼び口関数について、呼び口関数の結合
先の受け口関数、(1)その受け口関数から呼び出される呼び口関数とその結合
先の受け口関数について再帰的に呼出しフローを出力します。また(2)その受
け口関数から呼び出される非呼び口関数 (TECS 外の関数)についても再帰的に
呼出しフローを出力します。

これによりあるタスクやハンドラから呼び出される一連の関数を知ることがで
きます。

tecsflow の入力は TECS ジェネレータの生成物 tecsgen.rbdmp および C 言
語フロー解析ツール tcflow の生成物 tcflow.rbdmp です。それぞれの生成物
tecsgen.rbdmp, tcflow.rbdmp は Ruby のダンプです。Ruby のダンプファイ
ルとすることで中間生成物の定義を省略しています。

TECS ジェネレータの生成物 tecsgen.rbdmp は TECS ジェネレータの実行によ
り自動的に生成されます (V1.7.0 以降)。C 言語フロー解析ツール tcflow の
生成物 tcflow.rbdmp は tcflow の実行により生成されます。

以下のオプションを指定できます．::

    -g, --gen=dir
        インタフェースコードなどを生成するディレクトリを指定します．デ
        フォルトでは、カレントディレクトリの下の 'gen' ディレクトリに
        出力されます．
   

Makefile 記述例
----------------------------

Makefile に以下を追加します。たいていの場合、以下の記述が適切です。

.. code-block:: Makefile

  TECS_TARGET = tecs
  # TECS_TARGET = tecsgen            # 古い TECS ジェネレータのターゲット
  # TECS_TARGET = tecsgen.timestamp  # カーネルパッケージなどに見られる
  # GEN_DIR     = gen                # もし GEN_DIR が定義されていなければ
  tecsflow : $(GEN_DIR)/tecsgen.rbdmp tcflow
  	tecsflow -g $(GEN_DIR)

  tecsflow_u : $(GEN_DIR)/tecsgen.rbdmp tcflow
  	tecsflow -g $(GEN_DIR) -U

  $(GEN_DIR)/tecsgen.rbdmp : $(TECS_TARGET)

  tcflow : $(TECS_TARGET)
  	make tcflow_exec

  tcflow_exec : $(GEN_DIR)/tcflow.rbdmp
  $(GEN_DIR)/tcflow.rbdmp : $(CELLTYPE_SRCS) $(PLUGIN_CELLTYPE_SRCS)
  	tcflow -g $(GEN_DIR) -c '$(CC) -E -DTECSFLOW $(CFLAGS) -I ./' $^
    # add -DTECSGEN if many errors occur, especially when using gcc (*)

以上の記述で CELLTYPE_SRCS, PLUGIN_CELLTYPE_SRCS は Makefile.tecsgen
にて定義されますので、調整の必要はありません。TECS_TARGET は、Makefile
により異なる可能性があります。

以下のコマンドにより C言語フロー解析ツール tcflow, TECS フロー解析ツー
ル tecsflow が 実行されます。もし TECS ジェネレータ tecsgen が未実行の
場合は、これも実行されます。::

  % make tecsflow

(*) tcflow は、gcc の拡張機能への対応がよくありません。
    あるいは、C 言語標準への対応が十分ではないために tcflow は文法エラー
    として扱う可能性があります。
    tcflow は、文法エラーが発生している場合でも tcflow.rbdmp を生成します。
    生成された tcflow.rbdmp は tecsflow に取り込むことができます。
    ただし、エラーが発生しているファイルのいくらか (最長で末尾まで)
    スキップされてしまうため、C言語のソースファイルに記述されていても
    関数が出力されない (未定義となる) 可能性があります。

出力例
--------------

出力は3つのパートからなります。
 (1) アクティブセルを起点とするフロー
 (2) 未使用の受け口関数を起点とするフロー
 (3) 未使用の非受け口関数を起点とするフロー


(1) 「アクティブセルを起点とするフロー」の出力例
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::
   
  [active cell] ::AVR_CyclicAVR (../../tecs_lib/mindstorms_nxt/target_lib_inst.cdl 46)
      ciBody.main => AVR_AVRBody.eiCyclicBody.main (gen/tmp_tAVRBody.c 482)
            nxt_avr_updateBody: printed

[active cell] で始まる行はアクティブセルです。
次の行は、以下の形式です。::
   (呼び口).(呼び口関数) => (呼び先セル).(受け口).(受け口関数)

受け口関数が、呼び口関数を呼び出している場合、字下げしながら再帰的に出力されます。
次の行は、既に出力済みの C 言語の関数を表示しています。

(2) 「未使用の受け口関数を起点とするフロー」の出力例
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

  --- unreferenced entry functions ---
  [unreferenced entry function] ::ASPKernel.eKernel.sleep (../../tecs_kernel/tKernel_inline.h 56)
      slp_tsk: [Function Out of TECS, not defined]

--- unreferenced entry functions --- で始まる行から未使用の受け口関数
を起点とするフローのパートが始まることを示します。

[unreferenced entry function] で始まる行は受け口関数を表します。
次の行は TECS 外の関数が呼び出されていることの出力です。

(3) 「未使用の非受け口関数を起点とするフロー」の出力例
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::
   
  --- unreferenced C functions ---
  [Function Out of TECS, unreferenced] at91sam7s_putc (../../target/mindstorms_nxt_gcc/at91sam7s.h 667)
    Calling Function:
      sil_rew_mem (../../target/mindstorms_nxt_gcc/at91sam7s.h 667)
      sil_wrw_mem : printed

--- unreferenced C functions --- で始まる行から未使用の非受け口関数を
起点とするフローのパートが始まることを表します。
次の行からは、その関数が呼び出している関数を再帰的に出力します。
