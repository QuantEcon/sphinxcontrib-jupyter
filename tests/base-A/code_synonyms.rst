Code Synonyms
=============

This is useful for when you want to highlight two languages such as ``python`` and ``ipython``
syntax but want each to be executable within the same document.

This can be done in the ``conf.py`` file through the ``jupyter_lang_synonyms = ["ipython"]`` option

.. code-block:: python3

   import numpy as np 
   a = np.random.rand(10000)

and now an ipython block

.. code-block:: ipython

    %%file us_cities.txt
    new york: 8244910
    los angeles: 3819702
    chicago: 2707120 
    houston: 2145146
    philadelphia: 1536471
    phoenix: 1469471
    san antonio: 1359758
    san diego: 1326179
    dallas: 1223229

this will generate a file ``us_cities.txt`` in the local directory using an ipython 
cellmagic