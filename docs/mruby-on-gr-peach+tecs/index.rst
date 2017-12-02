mruby on GR-PEACH+TECS
======================

mruby on GR-PEACH+TECS は，組込み向けスクリプト言語「 **mruby** 」をルネサス社製マイコンボード **GR-PEACH** 上で動作させることができる開発プラットフォームです．

本フレームワークは，TECS(TOPPERS Embedded Component System)を使用しているため，コンポーネントベース開発が可能です．

mrubyの各VMには，TOPPERS/ASP3カーネルのタスクを割り当てており，マルチVM機能をサポートしています．
また，mrubyメソッド p, puts, print は，シリアル出力されます．

.. 以下からダウンロード可能です．

.. `mruby-on-gr-peach+tecs`_

.. todo::
    to be filled in

.. _`mruby-on-gr-peach+tecs`: https://www.toppers.jp/tecs.html


目次:

.. toctree::
   :maxdepth: 1

   howtobuild
   guide

   rtos
   led