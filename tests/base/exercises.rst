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


Collected Exercises
-------------------

Below should not report anything...

.. exerciselist::


This, however should repeat exercises from above

.. exerciselist::
   :force:
