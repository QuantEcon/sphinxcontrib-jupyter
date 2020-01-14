Table
=====

These tables are from the `RST specification <http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html#grid-tables>`__: 

Grid Tables
-----------

A simple rst table with header

+------+------+
| C1   | C2   |
+======+======+
| a    | b    |
+------+------+
| c    | d    |
+------+------+

**Note:** Tables without a header are currently not supported as markdown does
not support tables without headers.


Simple Tables
-------------

=====  =====  =======
  A      B    A and B
=====  =====  =======
False  False  False
True   False  False
False  True   False
True   True   True
=====  =====  =======

Directive Table Types
---------------------

These table types are provided by `sphinx docs <http://www.sphinx-doc.org/en/master/rest.html#directives>`__


List Table directive
~~~~~~~~~~~~~~~~~~~~

.. list-table:: Frozen Delights!
   :widths: 15 10 30
   :header-rows: 1

   * - Treat
     - Quantity
     - Description
   * - Albatross
     - 2.99
     - On a stick!
   * - Crunchy Frog
     - 1.49
     - If we took the bones out, it wouldn't be crunchy, now would it?
   * - Gannet Ripple
     - 1.99
     - On a stick!


CSV Table Directive
~~~~~~~~~~~~~~~~~~~

.. csv-table:: Frozen Delights!
   :header: "Treat", "Quantity", "Description"
   :widths: 15, 10, 30

   "Albatross", 2.99, "On a stick!"
   "Crunchy Frog", 1.49, "If we took the bones out, it wouldn't be crunchy, now would it?"
   "Gannet Ripple", 1.99, "On a stick!"

Complex Tables
--------------

**MultiColumn and MultiRow** tables are currently **not** supported by this extension