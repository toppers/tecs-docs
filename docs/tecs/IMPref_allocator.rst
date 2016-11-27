セルタイプコードでのアロケータ
==============================

シグニチャの関数の引数の基本指定子として send または receive を指定すると、引数としてアロケータによりアロケートされたメモリ領域のアドレスが渡されます。
渡されたメモリ領域は、受け取った側で解放します。

send 指定された引数の場合、呼び元でアロケートし、呼び先でデアロケートします。
receive 指定された引数の場合、呼び先でアロケートし、呼び元でデアロケートします。
アロケート、デアロケート操作は、アロケータ呼び口を通して行います。

アロケータ呼び口
.................

TECS では、メモリアロケータをセルとして実装しますが、アロケータセルの受け口に結合する呼び口が必要となります。
この呼び口のことをアロケータ呼び口と呼びます。
アロケータ呼び口は TECS CDL に明示的に記述しません。TECS ジェネレータにより生成されます。

アロケータ呼び口には、以下の名前が与えられます。

  (アロケータ呼び口名)  = (呼び口名または受け口名) + '_' + (関数名) + '_' + (引数名)

アロケータ使用の具体例
.......................

以下に、アロケータを使用する例を示します。

TECS CDL のコード例には、呼び先のセルタイプおよびセル、呼び元のセルタイプおよびセルが実装されているとします。
ジェネレータによって呼び先および呼び元の双方に、アロケータ呼び口およびその結合が自動的に挿入されます。

【TECS CDL 記述例】

.. code-block:: tecs-cdl

  signature sSendRecv {
    /* この関数名に send, receive を使ってしまうとアロケータ指定できない */
    ER snd( [send(sAlloc),size_is(sz)]int8 *buf, [in]int32  sz );
    ER rcv( [receive(sAllocTMO),size_is(*sz)]int8 **buf, [out]int32  *sz );
  };

  celltype tTestComponent {
    entry  sSendRecv eS;
  };

  // 受け口側で、send/receive 指定された引数ごとにアロケータを指定
  [allocator(eS.snd.buf=alloc.eA,eS.rcv.buf=alloc.eA)]
  cell tTestComponent comp{
  };

  celltype tTestClient {
  call   sSendRecv cS;
  };

  // 呼び口側では、アロケータを指定しない
  cell tTestClient cl {
    cS = comp.eS;
  };

【アロケータ呼び口が挿入されたコード（TECS ジェネレータにより内部生成された状態）】

以下のコードは、内部状態を説明するためのものであって、以下のような TECS CDL コードを記述するものではありません。

.. code-block:: tecs-cdl

  celltype tTestComponent {
    entry  sSendRecv eS;

    /* 自動生成されたアロケータ呼び口 */
    call   sAlloc    cS_snd_buf;    <<< 自動生成された呼び口
    call   sAlloc    cS_rcv_buf;    <<< 自動生成された呼び口
  };

  [allocator(eS.snd.buf=alloc.eA,eS.rcv.buf=alloc.eA)]
  cell tTestComponent comp{

    /* 自動生成されたアロケータ呼び口の結合 */
    eS_snd_buf = alloc.eA;          <<< 自動生成された結合
    eS_rcv_buf = alloc.eA;          <<< 自動生成された結合
  };

  celltype tTestClient {
    call   sSendRecv cS;

    /* 自動生成されたアロケータ呼び口 */
    call   sAlloc    cS_snd_buf;    <<< 自動生成された呼び口
    call   sAlloc    cS_rcv_buf;    <<< 自動生成された呼び口
  };

  cell tTestClient cl {
    cS = comp.eS;

    /* 自動生成されたアロケータ呼び口の結合 */
    cS_snd_buf = alloc.eA;          <<< 自動生成された結合
    cS_rcv_buf = alloc.eA;          <<< 自動生成された結合
  };

セルタイプ tTestClient の呼び口 cS の関数の send, receive 指定された引数に対して、以下のようなアロケータ呼び口関数が、生成されます。
アロケート関数、デアロケート関数の両方が使用できますが、send 指定された引数の場合、通常、呼び元で使用する必要があるのは、アロケート関数です。
rceive 指定された引数の場合は、デアロケート関数です。

.. code-block:: c

  // allocator port for call port: cS func: send param: buf
    ER             cS_snd_buf_alloc( int32_t size, void** p );
    ER             cS_snd_buf_dealloc( const void* p );
  // allocator port for call port: cS func: receive param: buf
    ER             cS_rcv_buf_alloc( int32_t size, void** p );
    ER             cS_rcv_buf_dealloc( const void* p );
  // allocator port for call port: cA func: send param: buf
    ER             cA_snd_buf_alloc( subscript, int32_t size, void** p );
    ER             cA_snd_buf_dealloc( subscript, const void* p );
  // allocator port for call port: cA func: receive param: buf
    ER             cA_rcv_buf_alloc( subscript, int32_t size, void** p );
    ER             cA_rcv_buf_dealloc( subscript, const void* p );


セルタイプ tTestComponent の受け口 eS の関数の send, receive 指定された引数に対しても、同様なアロケータ呼び口関数が、生成されます。

【未決定事項】アロケータを一々使い分けるのは、誤りのもとである。まとめる手段が必要。

アロケータの例
==============

アロケータセルの例を以下に示します。

【TECS CDL 記述例】

.. code-block:: tecs-cdl

  signature sAlloc {
     ER alloc( [in]size_t len, [out]void *p );
     ER dealloc( [in]void *p );
  };

  celltype tAlloc {
    entry sAlloc eA;
  };

  cell alloc {
  };


リレーアロケータ
==========================

リレーアロケータの TECS CDL 記述例を示します。

【TECS CDL 記述例】

.. code-block:: tecs-cdl

  signature sSendRecv {
    /* この関数名に send, receive を使ってしまうとアロケータ指定できない */
    ER snd( [send(sAlloc),size_is(sz)]int8_t *buf, [in]int32_t  sz );
    ER rcv( [receive(sAlloc),size_is(*sz)]int8_t **buf, [out]int32_t  *sz );
  };

  celltype tThroughComponent {
    [allocator(                  /* 受け口から呼び口へリレー */
        snd.buf <= cSR.snd.buf,  /* cSR:前方参照可能 */
        rcv.buf <= cSR.rcv.buf
    )]
    entry  sSendRecv eS;
    call   sSendRecv cSR;
  };

   /* セルの定義で、受け口の send/receive 指定された引数のアロケータ指定不要 */
   cell tThroughComponent comp{
     cSR = TargetCell.eS;   /* TargetCell でアロケータ指定が必要 */
   };

リレーアロケータの場合も、上述のアロケータの例と同様に、アロケータ呼び口と結合が生成されます。
tThroughComponent のセルタイプコードでは、以下のアロケータ呼び口関数が生成されます。
ただし、受け取ったものをそのまま渡すため、これらの呼び口関数は、実際には使用する必要はありません。
もし、受け取ったものをそのまま渡すのではなく、再アロケート(reallc) するような場合には、これらの呼び口を用いることになります。
（この例では realloc は含まれません）

.. code-block:: c

  // allocator port for call port: eA func: snd param: buf
    ER             eA_snd_buf_alloc( subscript, int32_t size, void** p );
    ER             eA_snd_buf_dealloc( subscript, const void* p );
  // allocator port for call port: eA func: rcv param: buf
    ER             eA_rcv_buf_alloc( subscript, int32_t size, void** p );
    ER             eA_rcv_buf_dealloc( subscript, const void* p );
  // allocator port for call port: eS func: snd param: buf
    ER             eS_snd_buf_alloc( int32_t size, void** p );
    ER             eS_snd_buf_dealloc( const void* p );
  // allocator port for call port: eS func: rcv param: buf
    ER             eS_rcv_buf_alloc( int32_t size, void** p );
    ER             eS_rcv_buf_dealloc( const void* p );
  // allocator port for call port: cSR func: snd param: buf
    ER             cSR_snd_buf_alloc( int32_t size, void** p );
    ER             cSR_snd_buf_dealloc( const void* p );
  // allocator port for call port: cSR func: rcv param: buf
    ER             cSR_rcv_buf_alloc( int32_t size, void** p );
    ER             cSR_rcv_buf_dealloc( const void* p );
