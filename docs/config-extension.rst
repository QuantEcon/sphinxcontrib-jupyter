.. _config_extension:

Extension Configuration and Options
===================================

Beyond generating ``Jupyter`` notebooks this extension can also be configured to:

#. execute notebooks
#. convert notebooks to html
#. convert notebooks to pdf (https://github.com/QuantEcon/sphinxcontrib-jupyter/pull/211)

This section provides documentation on the full suite of options available in the extension. A summary of each
option is provided in the table below.

The options are split into the different parts of the compilation pipeline that is available in this extension:

.. contents:: Extension Configuration:
   :maxdepth: 1

   config-extension-notebooks
   config-extension-execution
   config-extension-html
   config-extension-coverage

It can be useful to have multiple configurations when working on a large project, such as generating notebooks for
working on locally and editing and compiling the project for HTML in a deployment setting. 
Further details on how to manage large projects can be found `here <config-project>`__.

An example *conf.py* is available `here <config_example>`__

