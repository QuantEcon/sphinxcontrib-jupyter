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

~~However this **currently** means **.. code-block:: python** is also included as a non-execute 
cell [See `issue <https://github.com/QuantEcon/sphinxcontrib-jupyter/issues/51>`__]~~

This has been fixed by using jupyter_lang_synonyms = ["python"] in **conf.py** file. So **python**
will now be included alongside *python3*, *ipython*, and *pycon*.

.. code-block:: python

    import pandas as pd



A test suite for inline items

Here is some inline python ``import numpy as np`` that should be displayed

and some text that is not code ``here``

Inline maths with inline role: :math:`x^3+\frac{1+\sqrt{2}}{\pi}`

Inline maths using dollar signs (not supported yet): $x^3+\frac{1+\sqrt{2}}{\pi}$ as the 
backslashes are removed.

