Jupyter Directive
=================

This is a set of tests related to the Jupyter directive

The following jupyter directive with cell-break option should
split this text and the text that follows into different IN
blocks in the notebook

.. jupyter::
   :cell-break:

This text should follow in a separate cell.

Output Cells
------------

The following code block should have an output block

.. code-block:: python3

    import numpy as np 

.. jupyter::
   :type: output

   This text is in an output block
   that contains two lines of text