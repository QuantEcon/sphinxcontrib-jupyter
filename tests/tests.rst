Notebook without Tests 
======================

This is an almost exact analogue to the solutions class. The idea is that we can include test blocks using **:class: test** that we can toggle on or off with *jupyter_drop_tests = True*. A primary use case is for regression testing for the 0.6 => 1.0 port, which we will not want to show to the end user. 

Here is a small example: 

Question 1
------------

.. code-block:: julia 

    x = 3 
    foo = n -> (x -> x + n)

.. code-block:: julia 
    :class: test 

    import Test 
    @test x == 3
    @test foo(3) isa Function 
    @test foo(3)(4) == 7 