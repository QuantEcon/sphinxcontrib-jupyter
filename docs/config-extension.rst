.. _config_extension:

Extension Configuration and Options
===================================

.. note::

    The extension has recently been re-written to include separate translators
    for notebooks that have different end purposes. There is now IPYNB, HTML, 
    and PDF translators which allows the number of configuration options to be
    substantially reduced.

    Execution is now also handled by a specialised execution builder with results
    shared across IPYNB, HTML and PDF translators.

Options are available for each builder and translator:

.. toctree::
   :maxdepth: 1

   config-general
   config-ipynb-translator
   config-html-translator 
   config-pdf-translator
   config-execution
   config-directive-exercise

This extension also offers additional directives that can be used while writing your documents

.. toctree::
   :maxdepth: 1

   directives

It can also be useful to have multiple configurations when working on a large project, such as generating notebooks for
working on locally while compiling the project for HTML in a deployment setting. 

Further details on how to manage large projects can be found `here <config_project>`__.

An example *conf.py* is available `here <config_example>`__

