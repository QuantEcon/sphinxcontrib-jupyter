Only
====

This tests for support of the only directive with an html only block to follow this

.. only:: html

    this text should **not** show up for Jupyter notebook

there should be no html block above this text unless option jupyter_allow_html_only is True

and one related to Jupyter

.. only:: jupyter

   this should show up

there should be: **this should show up** above this text