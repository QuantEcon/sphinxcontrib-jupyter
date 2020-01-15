Slide option activated
----------------------

.. jupyter::
    :slide: enable

This is a collection of different types of cells where the toolbar: Slideshow has been activated

.. jupyter::
    :cell-break:

The idea is that eventually we will assign a type (*slide*, *subslide*, *skip*, *note*) for each one. We used our **jupyter** directive  to break the markdown cell into two different cells.


.. jupyter::
    :slide-type: subslide

.. code:: python3

    import numpy as np

    x = np.linspace(0, 1, 5)
    y = np.sin(4 * np.pi * x) * np.exp(-5 * x)

    print(y)

.. code:: python3

    import numpy as np

    z = np.cos(3 * np.pi * x) * np.exp(-2 * x)
    w = z*y

    print(w)


Math 
++++


    
The previous function was 

.. math:: f(x)=\sin(4\pi x)\cos(4\pi x)e^{-7x}


.. jupyter::
    :cell-break:
    :slide-type: fragment

We can also include the figures from some folder


.. figure:: _static/hood.jpg


Slide: Should have 2 code blocks as fragments (test)
++++++++++++++++++++++++++++++++++++++++++++++++++++

.. jupyter::
    :slide-type: fragment

.. code-block:: ipython3

    # This code block should be a Fragment!
    fibonacci_functional = (lambda n, first=1, second=1:
        [] if n == 0 else
        [first] + fibonacci_functional(n - 1, second, first + second))

.. jupyter::
    :slide-type: fragment

.. code-block:: ipython3

    for k in fibonacci_functional(10):print(k,end=' ')