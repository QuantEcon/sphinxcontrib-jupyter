.. _usage:

.. note::

    REWRITE. DO NOT INCLUDE IN INDEX

RST Conversion and Usage
========================

The following specifies the relationship between default Sphinx directives
and how they will be interpreted by this Jupyter extension.

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
``$`` for inline or ``$$`` for display formulae. 

Equation numbering is respected on the individual notebook level and is 
implemented using html links in each notebook.


Exercise Solutions
------------------

The extension has support for ``:class: solution`` on code-blocks. This
allows for the compilation of two sets of notebooks, one containing solutions
and one without.


Test Blocks
-----------

Other class options for code-blocks include `test` to indicate the 
code block contains a test which can be used for adding test logic
for automatic testing of notebooks. This is by default set to `False`
in the configuration and all test blocks are dropped.



Jupyter Directive and Slides
----------------------------

The ``jupyter`` directive accepts three different arguments ``cell-break``, ``slide`` and ``slide-type``
How to use them is explained bellow


cell-break
~~~~~~~~~~

.. code:: rst
    
    .. jupyter::
        :cell-break:

it is used to break a `markdown_cell` in two, this is done for example, when a paragraph 
is too large to fit in one slide.

slide
~~~~~

If the user wants to create a notebook where the cells are converted into
slides the folowing code needs to be included at the top of the .rst file.

.. code:: rst

    .. jupyter::
        :slide: {{enable/disable}}

``:slide: enable`` activates the slideshow metadata into the jupyter notebook, 
setting as a default value that each **cell** is a **slide**. 
The directive detects automatically the different cells 
(going from a ``markdown_cell`` to a ``code_cell`` for example), 
but also new cells are created when a subtitle is detected. If the user wants to force
a new cell, the option ``cell-break`` can be added.



slide-type
~~~~~~~~~~

The default value for each cell would be ``slide``. If the user wants
to change the upcoming cell to something different (``subslide``, ``fragment``, ``notes``, ``skip``)
the following code must be included

.. code:: rst

    .. jupyter::
        :slide-type: subslide



Other Supported Directives
--------------------------

1. ``.. note::`` - the raw contents of this directive is included 
into the notebook as a block quote with a **Note** title.

2. ``.. only::`` - this will skip any only content that is not jupyter