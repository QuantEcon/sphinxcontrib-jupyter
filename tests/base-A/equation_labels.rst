Equation Numbering
==================

This tests our implementation for Equation Numbering in the Notebook output

Filet mignon tenderloin salami tri-tip frankfurter. Prosciutto venison drumstick 
meatball burgdoggen shankle. Prosciutto pork loin jowl corned beef buffalo ribeye 
pork belly. Ball tip filet mignon cow spare ribs kielbasa turkey. Pork belly frankfurter 
filet mignon cupim kielbasa meatball ground round fatback beef ribs. Pork loin tongue 
bresaola, pig kielbasa capicola chuck short ribs burgdoggen venison spare ribs.

.. math::
    :label: eq_old1

    m_t - p_t = -\alpha(p_{t+1} - p_t) \: , \: \alpha > 0

for :math:`t \geq 0`

Equation :eq:`eq_old1` asserts that the demand for real balances is inversely
related to the public's expected rate of inflation, which here equals
the actual rate of inflation

And an equation that doesn't have a label

.. math::

    \begin{bmatrix}
      1 \\
      \theta_{t+1}
    \end{bmatrix} =
    \begin{bmatrix}
      1 & 0 \\
      0 & \frac{1+\alpha}{\alpha}
    \end{bmatrix}
    \begin{bmatrix}
      1 \\
      \theta_{t}
    \end{bmatrix}  +
    \begin{bmatrix}
      0 \\
      -\frac{1}{\alpha}
    \end{bmatrix}
    \mu_t

should be rendered without an html border

and then the same equation added with a label

.. math::
   :label: eq_old2

    \begin{bmatrix}
      1 \\
      \theta_{t+1}
    \end{bmatrix} =
    \begin{bmatrix}
      1 & 0 \\
      0 & \frac{1+\alpha}{\alpha}
    \end{bmatrix}
    \begin{bmatrix}
      1 \\
      \theta_{t}
    \end{bmatrix}  +
    \begin{bmatrix}
      0 \\
      -\frac{1}{\alpha}
    \end{bmatrix}
    \mu_t

will now have a :eq:`eq_old2` label associated with it in an html box.