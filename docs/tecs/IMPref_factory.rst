ファクトリ
==================

ファクトリでは、任意のファイルに出力できますが、以下の2つのファイルは、予め想定するファイルです。

コンフィギュレーションファイル
................................................

ファクトリの第一の使用目的は、コンフィギュレーションファイルに TOPPERS/ASP 系カーネルの静的 API を生成することです。
TECS ジェネレータにより生成されるコンフィギュレーションファイルの名前は、以下を推奨します。

  tecsgen.cfg 

以下は、コンフィギュレーションファイルに静的 API を生成する TECS CDL の記述例です。
セルが生成されるごとに、コンフィギュレーションファイルに静的 API が出力されます。

.. code-block:: tecs-cdl

  celltype tTask {
    attr {
            ID                   id = C_EXP( "TASKID_$id$" );
            VP_INT               exinf;
      [omit]ATR                  tskatr;
      [omit]PRI                  itskpri;
      [omit]SIZE                 stksize = 4096;
    };

    factory {
      write( "tecsgen.cfg",
             "CRE_TSK(%s,{%s,&$id$_CB,tTask_start_task,%s,%s,NULL});",
             id, tskatr, itskpri, stksize );
    };
  };


【補足説明】ファクトリで記述できることは限られている。判断や繰り返しが必要な場合、セルタイププラグインにより実現する。

ファクトリヘッダ
..........................

ファクトリヘッダは、セルタイプコードに取込むためのヘッダファイルであり、セルタイプヘッダにおいてインクルードされます。
ファクトリヘッダには、セルの属性、変数において C_EXP で与えられた初期値に含まれるマクロの定義を記述することができます。
ファクトリヘッダの名前は、以下のとおりです。
CELLTYPENAME の部分は、セルタイプ名に置き換えます。

   CELLTYPENAME_factory.h

以下の例は、セルタイプファクトリで TOPPERS/ASP のコンフィグレータの生成する kernel_cfg.h をインクルードするものです。
これによりコンフィグレータの出力するマクロを、セルの属性、変数の C_EXP 初期化子の中で参照することができます。

.. code-block:: tecs-cdl

   celltype tCelltype {
     FACTORY {
       write( "$ct$_factory.h", "#include \"kernel_cfg.h\"" );
     };
   };

