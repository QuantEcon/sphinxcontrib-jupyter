Code blocks
-----------

This is a collection to test various code-blocks

This is a **.. code::** directive

.. code:: python

    this = 'is a code block'
    x = 1
    no = 'really!'
    p = argwhere(x == 2)

This is another **.. code::** directive

.. code:: python

    from pylab import linspace
    t = linspace(0, 1)
    x = t**2

This is a **::** directive

::

    from pylab import *
    x = logspace(0, 1)
    y = x**2
    figure()
    plot(x, y)
    show()

This is a **.. code-block:: julia** test with showing snippet for another language *Julia*
and it is included as a non-execute cell

.. code-block:: julia

    using QuantEcon

However this **currently** means **.. code-block:: python** is also included as a non-execute 
cell [See `issue <https://github.com/QuantEcon/sphinxcontrib-jupyter/issues/51>`__]

.. code-block:: python

    import pandas as pd

No Execute
----------

This is a **.. code::** directive with **:class: no-execute**

.. code:: python
   :class: no-execute

    import numpy as np


Other Examples from rst2ipynb
-----------------------------

Support for Python doctest code blocks::

    >>> 1+1
    2
    >>> for x in range(3):
    ...      print x
    ...
    0
    1
    2
    >>> x = 1
    >>> x = 2

but the input to this cell is not parsed into separate blocks unlike `rst2ipynb <https://github.com/nthiery/rst-to-ipynb>`__

Function with pycon code block style:

.. code:: pycon

   >>> def f(a, b, c):
   ...     """Multiline
   ...     docstring
   ...
   ...     """
   ...     # a comment
   ...
   ...     return a + b + c
   ...
   >>> f(1, 2, 3)
   6

Output Test Cases
-----------------

**Note:** This sphinx extension does not currently parse blocks internally

Long Pandas DataFrame's with more than three digits in the index column will
have a ``...`` in the output which shouldn't be considered a Python line
continuation prompt:

.. code:: pycon

   >>> import pandas as pd
   >>> pd.DataFrame({'b': pd.np.arange(1000)}, index=pd.np.linspace(0, 10, 1000))
               b
   0.00000     0
   0.01001     1
   0.02002     2
   0.03003     3
   0.04004     4
   0.05005     5
   0.06006     6
   0.07007     7
   0.08008     8
   0.09009     9
   0.10010    10
   0.11011    11
   0.12012    12
   0.13013    13
   0.14014    14
   0.15015    15
   0.16016    16
   0.17017    17
   0.18018    18
   0.19019    19
   0.20020    20
   0.21021    21
   0.22022    22
   0.23023    23
   0.24024    24
   0.25025    25
   0.26026    26
   0.27027    27
   0.28028    28
   0.29029    29
   ...       ...
   9.70971   970
   9.71972   971
   9.72973   972
   9.73974   973
   9.74975   974
   9.75976   975
   9.76977   976
   9.77978   977
   9.78979   978
   9.79980   979
   9.80981   980
   9.81982   981
   9.82983   982
   9.83984   983
   9.84985   984
   9.85986   985
   9.86987   986
   9.87988   987
   9.88989   988
   9.89990   989
   9.90991   990
   9.91992   991
   9.92993   992
   9.93994   993
   9.94995   994
   9.95996   995
   9.96997   996
   9.97998   997
   9.98999   998
   10.00000  999

   [1000 rows x 1 columns]

Nested Code Blocks
------------------

Due to the linear structure of Jupyter notebooks (a list of cells),
many nested structures can't be rendered exactly. Nevertheless we want
to make sure that, despite some degrading, the end result is
reasonably readable, and code blocks are rendered as code cells.

The tests are taken from `rst2ipynb`, where many of them fail.

#. Nested code block A

   ::

       1+1

#.  Nested code block B

    ::

       1+1

#. Nested code block C; ok to fail? (the inner indent does not match the itemized text indent)

    ::

       1+1

The following note contains a code block -- and these get rendered as code-blocks which
breaks the note structure. This is the currently accepted solution.

.. NOTE::

   A code block in a note::

       >>> 1+1

   Another one::

       >>> 1+1


.. TOPIC:: Note

   A code block in a topic::

       >>> 1+1

   Another one::

       >>> 1+1

.. TOPIC:: Doubly nested code blocks

    #.  Foo

        ::

            1+1

        ::

            >>> def plus_grand_element(liste):
            ...     """
            ...     Renvoie le plus grand élément de la liste
            ...     EXAMPLES::
            ...         >>> plus_grand_element([7,3,1,10,4,10,2,9])
            ...         10
            ...         >>> plus_grand_element([7])
            ...         7
            ...     """
            ...     resultat = liste[0]
            ...     for i in range(1, len(liste)-1):
            ...         # Invariant: resultat est le plus grand element de liste[:i]
            ...         assert resultat in liste[:i]
            ...         assert all(resultat >= x for x in liste[:i])
            ...         if liste[i] > resultat:
            ...             resultat = liste[i]
            ...     return resultat
            >>> plus_grand_element([7,3,1,10,4,10,2,9])
            10

        Foo.

        Bla::

            >>> 1+1

        ok to fail? (missing mandatory new line after `::`)::
            >>> 1+1

.. TOPIC:: A code block in a list in a topic

    #.  Foo

        ::

	    >>> def fusion(l1, l2):
	    ...     sort(l1+l2)
