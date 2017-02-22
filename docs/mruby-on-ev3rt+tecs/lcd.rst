
LCD - `LCD`
==============

LCDに関するAPIです．
コンソールの幅は0~178，高さは0~128 （範囲外の数値も指定可能だが、コンソールには表示されない）．

特異メソッド一覧
----------------

* :ref:`LCD.font = (fnt) <mruby-on-ev3rt-lcd-font>`
* :ref:`LCD.draw (str, x, y) <mruby-on-ev3rt-lcd-draw>`
* :ref:`LCD.fill_rect (x, y, w, h, color) <mruby-on-ev3rt-lcd-fill-rect>`
* :ref:`LCD.draw_line (x0, y0, x1, y1) <mruby-on-ev3rt-lcd-draw-line>`
* :ref:`LCD.show_message_box (title, msg) <mruby-on-ev3rt-lcd-show-message-box>`
* :ref:`LCD.error_puts (msg) <mruby-on-ev3rt-lcd-error-puts>`
* :ref:`LCD.print (str) <mruby-on-ev3rt-lcd-print>`
* :ref:`LCD.puts (str) <mruby-on-ev3rt-lcd-puts>`

シンボル
------

* **color**

  LCDカラーを表すシンボル

  =======   =====
  シンボル
  ---------------
  :white    白
  :black    黒
  =======   =====

* **fnt**

  フォントサイズを表わすシンボル

  =======   ==========
  シンボル
  --------------------
  :small    小さいサイズのフォント
  :medium   普通サイズのフォント
  =======   ==========


特異メソッド
----------------

.. _mruby-on-ev3rt-lcd-font:

LCD.font = ( fnt ) -> nil
^^^^^^^^^^^^^^^^^^^^^^^^

デフォルトのフォントを設定する．

**引数**
  `fnt` フォントサイズのシンボル

**戻り値**
  nil

----

.. _mruby-on-ev3rt-lcd-draw:

LCD.draw ( str, x, y ) -> nil
^^^^^^^^^^^^^^

指定位置で文字列を描く．

**引数**
  `str` 文字列

  `x` 左上隅の水平方向の位置 （横方向にフォントサイズ＊x文字分ずらした位置，小数点以下切り捨て）

  `y` 左上隅の垂直方向の位置 （横方向にフォントサイズ＊y文字分ずらした位置，小数点以下切り捨て）

**戻り値**
  nil

----

.. _mruby-on-ev3rt-lcd-fill-rect:

LCD.fill_rect ( x, y, w, h, color ) -> nil
^^^^^^^^^^^^^^

矩形を描いて色を塗る．

**引数**
  `x` 左上隅の水平方向の位置 （小数点以下切り捨て）

  `y` 左上隅の垂直方向の位置 （小数点以下切り捨て）

  `w` 矩形の幅 （小数点以下切り捨て）

  `h` 矩形の高さ （小数点以下切り捨て）

  `color` カラーのシンボル

**戻り値**
  nil

----

.. _mruby-on-ev3rt-lcd-draw-line:

LCD.draw_line ( x0, y0, x1, y1 ) -> nil
^^^^^^^^^^^^^^

指定座標で線を引く．

**引数**
  `x0`  始点の水平方向の位置 （小数点以下切り捨て）

  `y0`  始点の垂直方向の位置 （小数点以下切り捨て）

  `x1`  終点の水平方向の位置 （小数点以下切り捨て）

  `y1`  終点の垂直方向の位置 （小数点以下切り捨て）

**戻り値**
  nil

----

.. _mruby-on-ev3rt-lcd-show-message-box:

LCD.show_message_box ( title, msg ) -> nil
^^^^^^^^^^^^^^

メッセージボックスにメッセージを表示する．
※メッセージボックスを表示中なmrubyのプログラムを一時停止し，中央（Enter）ボタンを押して再開する．

**引数**
  `title` メッセージボックスのタイトル
  `msg` メッセージ

**戻り値**
  nil

----

.. _mruby-on-ev3rt-lcd-error-puts:

LCD.error_puts ( msg ) -> nil
^^^^^^^^^^^^^^

メッセージボックスにエラーを出力する．

**引数**
  `msg` エラーメッセージ

**戻り値**
  nil

----

.. _mruby-on-ev3rt-lcd-print:

LCD.print ( str ) -> nil
^^^^^^^^^^^^^^

LCDコンソールに文字列を表示する（改行なし）．

**引数**
  `str` 文字列

**戻り値**
  nil

----

.. _mruby-on-ev3rt-lcd-puts:

LCD.puts ( str ) -> nil
^^^^^^^^^^^^^^

LCDコンソールに文字列を表示する（改行あり）．

**引数**
  `str` 文字列

**戻り値**
  nil

----


.. code-block:: ruby
  :caption: lcd_sample.rb
