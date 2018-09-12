Only
====

This tests for support of the only directive with an html only block to follow this (unless option **jupyter_allow_html_only** is True)

.. only:: html

    I am inside an HTML only block

there should be no html block above this text

and one related to Jupyter

.. only:: jupyter

   this should show up

there should be: **this should show up** above this text