TLSF+TECS
====================

TLSF+TECSは，「TLSF」をTECSでコンポーネント化した動的メモリアロケータです．

TLSFコンポーネントは，内部変数として独自のヒープ領域を保持しているため，タスク毎に独立してメモリ管理を行えます．

ただし，複数のタスクで同時に同じTLSFコンポーネントを使用する場合は，排他制御が必要です．


使用例:

mrubyのマルチVM機能 ( `mruby-on-ev3rt+tecs-package-beta2.0.1`_ ~)

.. _mruby-on-ev3rt+tecs-package-beta2.0.1: https://www.toppers.jp/tecs.html#mruby_ev3rt


リンク:

`TLSF (Two-Level Segregate Fit) -Memory Allocator for Real-Time-`_

.. _TLSF (Two-Level Segregate Fit) -Memory Allocator for Real-Time-: http://www.gii.upv.es/tlsf/


.. todo::
    to be filled in


目次:

.. toctree::
   :maxdepth: 1

