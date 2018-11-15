Usage
=====

This document explains the Jupyter directive, how to use it, 
and how to create a notebook where the cells are converted into slides.

Usage of jupyter directive 
------------------

The ``jupyter`` accepts three different arguments ``cell-break``, ``slide`` and ``slide-type``
How to use them is explained bellow


cell-break
++++++++++

.. jupyter::
    :cell-break:

it is used to break a `markdown_cell` in two, this is done for example, when a paragraph 
is too large to fit in one slide.

slide
+++++

If the user wants to create a notebook where the cells are converted into
slides the folowing code needs to be included at the top of the .rst file.

.. jupyter::
    :slide: {{enable/disable}}

`:slide: enable` activates the slideshow metadata into the jupyter notebook, 
setting as a default value that each *cell* is a *slide*. 
The directive detects automatically the different cells 
(going from a `markdown_cell` to a `code_cell` for example), 
but also new cells are created when a subtitle is detected. If the user wants to force
a new cell, the option `cell-break` can be added.



slide-type
++++++++++

As explained before, the default value for each cell would be `slide`. If the user wants
to change the upcoming cell to something different (subslide, fragment, notes, skip)
the following code must be included


.. jupyter::
    :slide-type: subslide




