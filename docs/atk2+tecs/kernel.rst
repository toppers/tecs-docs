
.. _atk2+tecs-kernel:

カーネル ― `tKernel`
=================


.. todo::
    to be filled in

使用方法
--------

カーネルの生成
^^^^^^^^^^^^

アプリケーション開発者は `tKernel` セルタイプのセルを生成することにより、カーネルを生成することができます。次の例では ``MyKernel`` という名前のタスクセルを生成し、 ``MyCell`` の ``sHookBody`` を結合しています。

.. code-block:: tecs-cdl
  :caption: app.cdl

  celltype tMyCellType {
      entry sHookBody   eStartupHookBody;
  };

  cell tMyCellType MyCell {};

  cell tKernel MyKernel {
      cStartupHookBody[0] = Sample.eStartupHookBody;
      cPreTaskHookBody = Sample.ePreTaskHookBody;
      cPostTaskHookBody = Sample.ePostTaskHookBody;
      cErrorHookBody = Sample.eErrorHookBody;
      cShutdownHookBody[0] = Sample.eShutdownHookBody;
      status = "EXTENDED";
      useGetServiceId = TRUE;
      useParameterAccess = TRUE;
      StackMonitoring = TRUE;
      stackSize = 512;
      ScalabilityClass ="SC1";
  };

.. code-block:: c
  :caption: tMyCellType.c

  void eStartupHookBody_main()
  {
    #ifdef TOPPERS_ENABLE_SYS_TIMER
      target_timer_initialize();
    #endif /* TOPPERS_ENABLE_SYS_TIMER */
    syslog_initialize();
    syslog_msk_log(LOG_UPTO(LOG_INFO));
    InitSerial();
    print_banner();
    blsm_autosar_init();  
  }

リファレンス
------------

セルタイプ
^^^^^^^^^^

.. tecs:celltype:: tKernel

カーネルの生成を行うコンポーネントです。

  .. tecs:attr:: char_t *name = C_EXP("$cell$")

  カーネルの名前を指定します。
  指定しない場合、セルの名前が使用されます。

  .. tecs:attr:: char_t *status = "EXTENDED"

  エラーコード種別を指定します。
  指定しない場合、EXTENDEDが使用されます。

    .. c:macro:: "EXTENDED"

    標準エラーと拡張エラーを検出

    .. c:macro:: "STANDARD"

    標準エラーのみ検出

  .. tecs:attr:: bool_t StackMonitoring

  スタックモニタリング使用の有無を指定します。

    .. c:macro:: True

      スタックモニタリングを使用します。

    .. c:macro:: False

      スタックモニタリングを使用しません。

  .. tecs:attr:: uint32_t stackSize

  C2ISR用スタックとフック用スタックを1つのスタックで確保する場合のスタックサイズを指定します。

  .. tecs:attr:: char_t *ScalabilityClass = "SC1"

  OSのスケーラビリティクラスを指定します。
  現在はSC1しかサポートしていません。

  .. tecs:attr:: bool_t useGetServiceId

  OSErrorGetServiceId()の使用有無を指定します。

    .. c:macro:: True

    OSErrorGetServiceId()を使用します。

    .. c:macro:: False

    OSErrorGetServiceId()を使用しません。

  .. tecs:attr:: bool_t useParameterAccess

  エラーが発生したシステムサービスの引数取得の使用有無を指定します。

    .. c:macro:: True

    エラーが発生したシステムサービスの引数取得有効。

    .. c:macro:: False

    エラーが発生したシステムサービスの引数取得無効。 

シグニチャ
^^^^^^^^^^

.. tecs:signature:: sKernelTask
  Task用のカーネル本体を呼び出すシグニチャ

  .. tecs:sigfunction:: StatusType schedule(void)
  明示的な再スケジューリングを行う。

  .. tecs:sigfunction:: void enableAllInterrupts(void)
  disableAllInterruptsによって設定された割込み禁止状態を割込み許可状態に戻す。

  .. tecs:sigfunction:: void disableAllInterrupts(void)
  ターゲットの割込みをすべて禁止し、クリティカルセクションに入る。

  .. tecs:sigfunction:: void resumeAllInterrupts(void)
  suspendAllInterruptsによって設定された割込み禁止状態を割込み許可状態に戻す。

  .. tecs:sigfunction:: void suspendAllInterrupts(void)
  ターゲットの割込み状態を保存した後、ターゲットの割込みをすべて禁止しクリティカルセクションに入る。

  .. tecs:sigfunction:: void resumeOsInterrupts(void)
  suspendOSInterrupts によって設定された割込み禁止状態を割込み許可状態に戻す。

  .. tecs:sigfunction:: void suspendOsInterrupts(void)
  ターゲットの割込み状態を保存した後、C2ISRをすべて禁止しクリティカルセクションに入る。 

  .. tecs:sigfunction:: AppModeType getActiveApplicationMode(void)
  OS起動時に指定されたアプリケーションモードを取得する。

  .. tecs:sigfunction:: void shutdownOs([in] StatusType ercd)
  すべてのOSサービスを終了する。





.. tecs:signature:: sKernelISR1

  ISR1用のカーネル本体を呼び出すシグニチャ

  .. tecs:sigfunction:: void enableAllInterrupts(void)
  disableAllInterruptsによって設定された割込み禁止状態を割込み許可状態に戻す．。

  .. tecs:sigfunction:: void disableAllInterrupts(void)
  ターゲットの割込みをすべて禁止し、クリティカルセクションに入る。

  .. tecs:sigfunction:: void resumeAllInterrupts(void)
  suspendAllInterruptsによって設定された割込み禁止状態を割込み許可状態に戻す。

  .. tecs:sigfunction:: void suspendAllInterrupts(void)
  ターゲットの割込み状態を保存した後、ターゲットの割込みをすべて禁止しクリティカルセクションに入る。

  .. tecs:sigfunction:: void resumeOsInterrupts(void)
  suspendOSInterrupts によって設定された割込み禁止状態を割込み許可状態に戻す。

  .. tecs:sigfunction:: void suspendOsinterrupts(void)
  ターゲットの割込み状態を保存した後、C2ISRをすべて禁止しクリティカルセクションに入る。 






.. tecs:signature:: sKernelISR2

  ISR2用のカーネル本体を呼び出すシグニチャ

  .. tecs:sigfunction:: void enableAllInterrupts(void)
  disableAllInterruptsによって設定された割込み禁止状態を割込み許可状態に戻す．。

  .. tecs:sigfunction:: void disableAllInterrupts(void)
  ターゲットの割込みをすべて禁止し、クリティカルセクションに入る。

  .. tecs:sigfunction:: void resumeAllInterrupts(void)
  suspendAllInterruptsによって設定された割込み禁止状態を割込み許可状態に戻す。

  .. tecs:sigfunction:: void suspendAllInterrupts(void)
  ターゲットの割込み状態を保存した後、ターゲットの割込みをすべて禁止しクリティカルセクションに入る。

  .. tecs:sigfunction:: void resumeOsInterrupts(void)
  suspendOSInterrupts によって設定された割込み禁止状態を割込み許可状態に戻す。

  .. tecs:sigfunction:: void suspendOsinterrupts(void)
  ターゲットの割込み状態を保存した後、C2ISRをすべて禁止しクリティカルセクションに入る。 

  .. tecs:sigfunction:: AppModeType getActiveApplicationMode(void) 
  OS起動時に指定されたアプリケーションモードを取得する。

  .. tecs:sigfunction:: void shutdownOs([in] StatusType ercd)
  すべてのOSサービスを終了する。





.. tecs:signature:: sKernelErrorHook

  カーネル本体を呼び出すシグニチャ（ErrorHook用）

  .. tecs:sigfunction:: void resumeAllInterrupts(void)
  suspendAllInterruptsによって設定された割込み禁止状態を割込み許可状態に戻す。

  .. tecs:sigfunction:: void suspendAllInterrupts(void)
  ターゲットの割込み状態を保存した後、ターゲットの割込みをすべて禁止しクリティカルセクションに入る。

  .. tecs:sigfunction:: AppModeType getActiveApplicationMode(void) 
  OS起動時に指定されたアプリケーションモードを取得する。

  .. tecs:sigfunction:: void shutdownOs([in] StatusType ercd)
  すべてのOSサービスを終了する。




.. tecs:signature::　sKernelTaskHook

  カーネル本体を呼び出すシグニチャ（TaskHook用）

  .. tecs:sigfunction:: void resumeAllInterrupts(void)
  suspendAllInterruptsによって設定された割込み禁止状態を割込み許可状態に戻す。

  .. tecs:sigfunction:: void suspendAllInterrupts(void)
  ターゲットの割込み状態を保存した後、ターゲットの割込みをすべて禁止しクリティカルセクションに入る。

  .. tecs:sigfunction:: AppModeType getActiveApplicationMode(void)
  OS起動時に指定されたアプリケーションモードを取得する。






.. tecs:signature:: sKernelPreTaskHook
  カーネル本体を呼び出すシグニチャ（PreTaskHook用）

  .. tecs:sigfunction:: AppModeType getActiveApplicationMode(void)  
  OS起動時に指定されたアプリケーションモードを取得する。






.. tecs:signature:: sKernelPostTaskHook

  カーネル本体を呼び出すシグニチャ（PostTaskHook用）

  .. tecs:sigfunction:: AppModeType getActiveApplicationMode(void)  
  OS起動時に指定されたアプリケーションモードを取得する。






.. tecs:signature:: sKernelStartupHook

  カーネル本体を呼び出すシグニチャ（StartupHook用）

  .. tecs:sigfunction:: AppModeType getActiveApplicationMode(void)  
  OS起動時に指定されたアプリケーションモードを取得する。

  .. tecs:sigfunction:: void shutdownOs([in] StatusType ercd)
  すべてのOSサービスを終了する。







.. tecs:signature:: sKernelShutdownHook

  カーネル本体を呼び出すシグニチャ（ShutdownHook用）

  .. tecs:sigfunction:: AppModeType getActiveApplicationMode(void)  
  OS起動時に指定されたアプリケーションモードを取得する。






.. tecs:signature:: sKernelAlarmCallback

  カーネル本体を呼び出すシグニチャ（AlarmCallback用）

  .. tecs:sigfunction:: void resumeAllInterrupts(void)
  suspendAllInterruptsによって設定された割込み禁止状態を割込み許可状態に戻す。

  .. tecs:sigfunction:: void suspendAllInterrupts(void)  
  ターゲットの割込み状態を保存した後、ターゲットの割込みをすべて禁止しクリティカルセクションに入る。




.. tecs:signature:: snKernel

  カーネル起動シグニチャ

  .. tecs:sigfunction:: void startOs([in] AppModeType mode)
　　指定されたアプリケーションモードでOSを起動する。









.. tecs:signature:: sEventISR2

  .. tecs:sigfunction:: StatusType set([in] TaskType tskid, [in] EventMaskType mask)
  TaskID で指定されたタスクに Mask で指定されたイベントを設定する。
    :return: 正常終了 (`E_OK`) またはエラーコード。

  .. tecs:sigfunction:: StatusType get([in] TaskType tskid, [out] EventMaskRefType p_mask)
    TaskID で指定されたタスクが保持しているイベントマスク値を取得する。
    :return: 正常終了 (`E_OK`) またはエラーコード。





.. tecs:signature:: sEventHook
  .. tecs:sigfunction:: StatusType get([in] TaskType tskid, [out] EventMaskRefType p_mask)
    TaskID で指定されたタスクが保持しているイベントマスク値を取得する。
    :return: 正常終了 (`E_OK`) またはエラーコード。

