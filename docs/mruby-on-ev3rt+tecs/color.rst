
カラー - `Color`
==============

カラーセンサに関するAPIです．

.. todo::
    RGBの値を取得できるAPIの追加

インスタンスメソッド一覧
----------------

* :ref:`initialize( port ) <mruby-on-ev3rt-color-initialize>`
* :ref:`color <mruby-on-ev3rt-color-color>`
* :ref:`refrect <mruby-on-ev3rt-color-reflect>`
* :ref:`ambient <mruby-on-ev3rt-color-ambient>`

シンボル
------

* **color**

  カラーセンサで識別できるカラーのシンボル

  =======   =====
  シンボル
  ---------------
  :black    黒
  :blue     青
  :green    緑
  :yellow   黄
  :red      赤
  :white    白
  :brown    茶
  :none     識別できなかった
  =======   =====

* **port**

  センサポートを表わすシンボル

  =======   ==========
  シンボル
  --------------------
  :port_1   ポート 1
  :port_2   ポート 2
  :port_3   ポート 3
  :port_4   ポート 4
  =======   ==========

----

.. _mruby-on-ev3rt-color-initialize:

initialize ( port ) -> nil
^^^^^^^^^^^^^^^^^^^^^^^^^^

カラーセンサポートを設定する．

**引数**
  `port`  センサポートのシンボル
**戻り値**
  nil

----

.. _mruby-on-ev3rt-color-color:

color -> Symbol
^^^^^^^^^^^^^^

カラーセンサでカラーを識別する．

**引数**
  なし
**戻り値**
  識別したカラーのシンボルを返す．

----

.. _mruby-on-ev3rt-color-reflect:

reflect -> nil
^^^^^^^^^^^^^^^^^^^^^^

カラーセンサで反射光の強さを測定する．

**引数**
  なし
**戻り値**
  反射光の強さ（0〜100）

----

.. _mruby-on-ev3rt-color-ambient:

ambient -> Fixnum
^^^^^^^^^^^^^^^

カラーセンサで環境光の強さを測定する．

**引数**
  なし
**戻り値**
  環境光の強さ（0〜100）

----


.. code-block:: ruby
  :caption: color_sample.rb
