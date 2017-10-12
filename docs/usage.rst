Usage
=====

This details the relationship between default Sphinx directives
and how they will be interpreted by this Jupyter extension.

Usage in RST Files
------------------

To generate an ``In`` style executable block you can use

.. code:: rst

    .. code-block:: python

.. code:: rst

    .. literalinclude::  

To generate a notebook that looks precomputed you can specify output
using the ``:class: output`` option.

.. code:: rst

    .. code-block:: python
        :class: output

To include code in the notebook that is not meant for execution can be
included using ``:class: no-execute``. This is useful when writing code
that is meant to throw errors, for example.

.. code:: rst

    .. code-block:: python
        :class: no-execute

this will generate a highlighted markdown cell of the contents of the
code-block. An alias for this is ``:class: skip-test``. This is used
in the context of a test environment that is using the collection of 
notebooks to test a collection of code snippets.