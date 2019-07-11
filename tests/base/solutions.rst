Notebook without solutions
==========================

The idea is with the use of classes, we can  decide whether to show or not the solutions
of a particular lecture, creating two different types of jupyter notebooks. For now it only 
works with *code blocks*, you have to include **:class: solution**, and set in  the conf.py file
*jupyter_drop_solutions=True*.


Here is a small example

Question 1
----------

Plot the area under the curve 

.. math::

    f(x)=\sin(4\pi x) exp(-5x)

when :math:`x \in [0,1]`

.. code-block:: python3
    :class: solution

    import numpy as np
    import matplotlib.pyplot as plt

    x = np.linspace(0, 1, 500)
    y = np.sin(4 * np.pi * x) * np.exp(-5 * x)

    fig, ax = plt.subplots()

    ax.fill(x, y, zorder=10)
    ax.grid(True, zorder=5)
    plt.show()
