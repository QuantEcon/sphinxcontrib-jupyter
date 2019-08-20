Exercises
=========

This notebook tests the new exercise directive defined in this package

.. exercise::

   This is a note that has some _italic_ and **bold** embedded

   - list
   - in
   - exercise

   .. code-block:: python
      :class: no-execute

      def foobar(x, y, z):
         print(x, y, z)


   And text after the code block

   below is something that should be a real code block

   .. code-block:: python3

      def foobar(x, y, z):
         print(x, y, z)

   And text to follow

text in between exercise

.. exercise::

   This is a normal exercise


.. exercise::
   :label: pyfun_functions_2

   I'm a function with a label and a solution

   Define a function named ``var`` that takes a list (call it ``x``) and
   computes the variance. This function should use the `mean` function that we
   defined earlier.

   Hint: :math:`\text{variance} = \frac{1}{N} \sum_i (x_i - \text{mean}(x))^2`

   .. code-block:: python

      # your code here


.. exercise::
   :label: label2

   This is another function with a label

   - and
   - *a*
   - **list**!



Collected Exercises
-------------------

**All exercises from file appear below**

.. exerciselist::


Repeated again because force doesn't matter
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. exerciselist::
   :force:
