Code blocks
-----------

.. code:: python

    this = 'is a code block'
    x = 1
    no = 'really!'
    p = argwhere(x == 2)

.. code:: python

    from pylab import linspace
    t = linspace(0, 1)
    x = t**2

::

    from pylab import *
    x = logspace(0, 1)
    y = x**2
    figure()
    plot(x, y)
    show()

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
