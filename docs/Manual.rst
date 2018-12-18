.. contents::

.. section-numbering::

.. raw:: pdf

    Pagebreak oneColumn



.. _usage:

Usage
=====

This specifies the relationship between default Sphinx directives
and how they will be interpreted by this Jupyter extension.

Usage in RST Files
------------------

To generate an ``In`` style executable block you can use:

.. code:: rst

    .. code-block:: {{ language }}

or,

.. code:: rst

    .. literalinclude::  {{ path_to_file }}

A ``literalinclude`` will make use of the default language in Sphinx 
to highlight the block, otherwise a language can be specified such as,

.. code:: rst

    .. literalinclude::  {{ path_to_file }}
        :language: julia

To generate a notebook that looks pre-computed you can specify output
using the ``:class: output`` option.

.. code:: rst

    .. code-block:: {{ language }}
        :class: output

To include code in the notebook that is not meant for execution you can use
the ``:class: no-execute``. This is useful when writing code
that is meant to throw errors, for example.

.. code:: rst

    .. code-block:: {{ language }}
        :class: no-execute

this will generate a highlighted markdown cell of the contents of the
code-block. An alias for this is ``:class: skip-test``. This is used
in the context of a test environment that is using the collection of 
notebooks to test a collection of code snippets.

.. todo:: 

    It might be nice to add screenshots to demonstrate the correlation between 
    the blocks above and the representation in the notebook.

Output blocks may be constructed and it will be paired directly with the 
previous ``In`` type code block. This can be used to construct notebooks that
look like they have already been pre-executed.

.. code:: rst

    .. code-block:: {{ language }}
        :class: output

.. todo::

    Discuss this feature. It may be better to generate and then execute the
    notebook to get notebooks that are pre-formatted with output figures etc.
    This would ensure output stays consistent with the code that generates it.

Math
----

Equations are transferred into the notebook environment and wrapped in 
``$`` for inline or `$$`` for display formulae. 

Equation numbering is respected on the individual notebook level and is 
implemented using html links in each notebook.