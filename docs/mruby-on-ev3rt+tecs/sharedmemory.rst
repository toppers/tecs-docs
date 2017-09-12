共有変数 - `SharedMemory`
==============

各VM間で共有変数を扱うAPIです．


インスタンスメソッド一覧
----------------

* :ref:`putVal　(index, val) <mruby-on-ev3rt-sharedmemory-putVal>`
* :ref:`getVal　(index) <mruby-on-ev3rt-sharedmemory-getVal>`

インスタンスメソッド
----------------

.. _mruby-on-ev3rt-sharedmemory-putVal:

putVal ( index, val ) -> nil
^^^^^^^^^^^^^^^^^^^^^^^^^^

共有変数に値を入力する

**引数**
  ``index``  共有変数のインデックス

  `val`   　値

**戻り値**
  nil

**a[index] = val でも可**

----

.. _mruby-on-ev3rt-sharedmemory-getVal:

getVal ( index ) -> Fixnum
^^^^^^^^^^^^^^^^^^^^^^^^^^

共有変数の値を出力する

**引数**
  ``index``  共有変数のインデックス

**戻り値**
  共有変数の値

**b = a[index] でも可**

----

.. code-block:: ruby
  :caption: sharedmemory_sample.rb
