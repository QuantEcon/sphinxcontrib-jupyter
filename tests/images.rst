Images
======

Collection of tests for **.. image::** and **.. figure::** directives

Image
-----

`Docutils Reference <http://docutils.sourceforge.net/docs/ref/rst/directives.html#images>`__

Most basic image directive

.. image:: _static/hood.jpg

A scaled down version with 25 % width

.. image:: _static/hood.jpg
   :width: 25 %

A height of 50px

.. image:: _static/hood.jpg
   :height: 50px

Including *alt*

.. image:: _static/hood.jpg
   :alt: A Mountain View

An image with a *right* alignment

.. image:: _static/hood.jpg
   :scale: 75 %
   :align: right

An image with a *left* alignment

.. image:: _static/hood.jpg
   :scale: 50 %
   :align: left

Figure
------

`Docutils Reference <http://docutils.sourceforge.net/docs/ref/rst/directives.html#figure>`__

Testing the **.. figure::** directive

.. figure:: _static/hood.jpg
   :scale: 50 %
