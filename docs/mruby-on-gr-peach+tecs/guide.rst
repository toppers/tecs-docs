
アプリケーションの開発方法
===============================

ここでは， mruby アプリケーションの開発方法について説明します．
開発環境やビルド方法については，:ref:`gr-peach+tecs-howtobuild` を参照してください．

サンプルアプリケーション
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
asp3/workspace/mruby_app に mruby のサンプルプログラムが入っています.
基本的に，このディレクトリでプログラムを書いていきます．

デフォルトは，*led_sample.rb* となっています．


アプリケーションファイルの指定
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
mruby on GR-PEACH+TECS では，アプリケーションファイルの指定をCDLというファイルによってコンフィグレーションを行います．
TECS CDL については，:ref:`TECS-CDL` を参照してください．

asp3/workspace/build の VM1.cdl にてアプリケーションを指定しています．
アプリケーションを変更する場合は，``$(MRUBY_APP_DIR)/led_sample.rb`` の行を，任意のアプリケーション名に修正し,　**make** を実行してください．

例えば， ``$(MRUBY_APP_DIR)/rtos_sample.rb`` とすると，*rtos_sample.rb* が実行されます．


.. code-block:: tecs-cdl
  :caption: VM1.cdl

	import(<bridge.cdl>);

	cell nMruby::tMruby Mruby {
		mrubyFile =
			"$(MRUBY_LIB_DIR)/RTOS.rb "
			"$(MRUBY_LIB_DIR)/LED.rb "
			"$(MRUBY_APP_DIR)/led_sample.rb";	<---(アプリケーションの指定)

		cInit = VM_TECSInitializer.eInitialize;
		cSerialPort = SerialPort1.eSerialPort;
	};

	cell tTask MrubyTask1 {
		cTaskBody = Mruby.eMrubyBody;
		attribute = C_EXP("TA_ACT");
		priority  = 10;
		stackSize = 4096;
	};


