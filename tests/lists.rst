List
----

Basic Lists
-----------

Bullets
~~~~~~~

-  b1
-  b2
-  b3

Bullets
~~~~~~~

*  b1
*  b2
*  b3

List
~~~~

1. l1
2. l2
3. l3

Numbered
~~~~~~~~

#. a numbered list
#. and a second item
#. and a third item 

Nested Lists
------------

Bullets
~~~~~~~

* b1

  * c1
  * c2

* b2

  * d1
  * d2

* b3

Bullets
~~~~~~~

* this is
* a list

  * with a nested list
  * and some subitems

* and here the parent list continues

Mixed Lists
~~~~~~~~~~~

1. bla
  * foo1
  * foo 2
2. bla2
  * foo
3. bla3


Malformed Lists that seem to work in HTML
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* first item

* second item

    * a sub item that is spaced with four spaces rather than two


Complex Lists with Display Math
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here is a computational algorithm:

1.  Start with a guess for the value for :math:`\Phi`, then use the
    first-order conditions and the feasibility conditions to compute
    :math:`c(s_t), n(s_t)` for :math:`s \in [1,\ldots, S]` and
    :math:`c_0(s_0,b_0)` and :math:`n_0(s_0, b_0)`, given :math:`\Phi`

    * these are :math:`2  (S+1)` equations in :math:`2  (S+1)` unknowns

2. Solve the :math:`S` equations for the :math:`S` elements of :math:`\vec x`

    .. math::

        u_{c,0}

3. Find a :math:`\Phi` that satisfies

    .. math::
        :label: Bellman2cons

        u_{c,0} b_0 = u_{c,0} (n_0 - g_0) - u_{l,0} n_0  + \beta \sum_{s=1}^S \Pi(s | s_0) x(s)

   by gradually raising :math:`\Phi` if the left side of :eq:`Bellman2cons`
   exceeds the right side and lowering :math:`\Phi` if the left side is less than the right side

4. After computing a Ramsey allocation,  recover the flat tax rate on
   labor.

Complex Lists with Code Blocks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. foo, and then in your REPL run 

    .. code-block:: julia 
          
            @assert x == 2 

2. and another item in the list. Hopefully this list item can be continued in the next markdown block in the notebook