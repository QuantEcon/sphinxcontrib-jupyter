.. _directives:

Directives
==========

The following directives are provided by this extension:

.. contents::
    :depth: 1
    :local:

Directive: exercise
-------------------

Exercise directives can be added to your text such as:

.. code-block:: rst

    .. exercise::

        Contains the Exercise

If you would like to ``exclude`` them from your documents you 
can set:

.. code-block:: python

    exercise_include_exercises = False``

in your ``conf.py`` file.


Directive: exerciselist
-----------------------

Collect exercises from the document and compile an exercise list where the directive is placed in the RST

.. code-block:: rst

    .. exerciselist::


Beneath each exercise in the list there is another link "(back to text)" 
that points back to the location where you originally authored/placed the exercise. 

Provided Options
~~~~~~~~~~~~~~~~

.. code-block:: rst

    .. exerciselist::
        :scope: SCOPE
        :from: FILE
        :force:


.. list-table:: 
   :header-rows: 1

   * - Option
     - Description
     - Values
   * - ``:from:``
     - import exercise defined in a file
     - 
   * - ``:scope:``
     - provide scope of exercises
     - ``file``, ``section``, or ``all``
   * - ``:force:``
     - force exercises to render where they are defined
     - True/False
   * - ``:title:``
     - Specify title used for exercise block
     - 

``:scope:`` 
^^^^^^^^^^^

``file``        then only exercises defined in the same file as the `exerciselist` directive will be included
``section``     then all exercises defined in the same section will be included
``all``         then all exercises anywhere in the project will be included


``:force:``
~~~~~~~~~~~

By default, when the conf.py config setting `exercise_inline_exercises` is true, all 
exercises will render where they are defined and the exerciselist node will be removed 
from the doctree. 

.. warning::

    However, if the `:force`: option is given the exerciselist will always be rendered 
    and when `exercise_inline_exercises` is True, each problem will be rendered twice.

Additional Info
~~~~~~~~~~~~~~~

If an exercise is included in an exercise list, it is only removed from its original 
location if the exercise list is in the same file. 

For example, if I define an exercise in `A.rst` and in `B.rst` I both define an exercise
and an exerciselist with `:scope: section` then the following will happen:

- both exercises will render at the point of the exerciselist in `B.rst`
- The exercise in `B.rst` will not be rendered where it was defined, but instead a link to the exercise list and number will be given
- The exercise in `A.rst` will still be rendered in file A. This means its contents are rendered two times.