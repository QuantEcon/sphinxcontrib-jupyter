Tool bar activated
------------------

This is a collection of different types of cells where the toolbar: Slideshow has been activated

.. jupyter::
	:cell-break:

The idea is that eventually we will assign a type (*Slide*, *Sub-Slide*, *skip*, *flag*) for each one. We used our **jupyter** directive  (not merged into the master yet) to break the markdown cell into two different cells.

Code
++++
.. code:: python3

    import numpy as np

    x = np.linspace(0, 1, 5)
    y = np.sin(4 * np.pi * x) * np.exp(-5 * x)

    print(y)

Math 
++++

The previous function was 

.. math:: f(x)=\sin(4\pi x)e^{-5x}


.. jupyter::
	:cell-break:

We can also include the figures from some folder

.. figure:: _static/hood.jpg



    

