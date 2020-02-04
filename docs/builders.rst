.. _builders:

Builders
=========

.. contents:: Options
    :depth: 1
    :local:

execute
-------

This builder extracts code-blocks from the `RST` files and manages the 
execution of each block. It saves the results in a `json` type codetree
object for use by other builders that construct notebooks.

jupyter
-------

This builder build IPYNB notebooks.

if `jupyter_execute_notebooks=True` is set in the `conf.py` file then 
the `execute` builder is automatically called to run all code.


jupyterhtml 
-----------

This builder manages the construction of project websites

if `jupyter_execute_notebooks=True` is set in the `conf.py` file then 
the `execute` builder is automatically called to run all code.

jupyterpdf
----------

This builder handles construction of `pdf` versions of the RST documents.

if `jupyter_execute_notebooks=True` is set in the `conf.py` file then 
the `execute` builder is automatically called to run all code.
