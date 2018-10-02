Math
----

Inline maths with inline role: :math:`x^3+\frac{1+\sqrt{2}}{\pi}`

Inline maths using dollar signs (not supported yet): $x^3+\frac{1+\sqrt{2}}{\pi}$ as the 
backslashes are removed.

.. math::

   x^3+\frac{1+\sqrt{2}}{\pi}

check math with some more advanced LaTeX, previously reported as an issue.

.. math::

    \mathbb P\{z = v \mid x \}
    = \begin{cases} 
        f_0(v) & \mbox{if } x = x_0, \\
        f_1(v) & \mbox{if } x = x_1
    \end{cases} 

and labeled test cases

.. math::
   :label: firsteq

    \mathbb P\{z = v \mid x \}
    = \begin{cases} 
        f_0(v) & \mbox{if } x = x_0, \\
        f_1(v) & \mbox{if } x = x_1
    \end{cases} 

Further Inline
--------------

A continuation Ramsey planner at :math:`t \geq 1` takes 
:math:`(x_{t-1}, s_{t-1}) = (x_-, s_-)` as given and before 
:math:`s` is realized chooses 
:math:`(n_t(s_t), x_t(s_t)) = (n(s), x(s))` for :math:`s \in  {\cal S}`

Referenced Math
---------------

Simple test case with reference in text

.. math::
   :label: test

    v = p + \beta v

this is a reference to :eq:`test` which is the above equation