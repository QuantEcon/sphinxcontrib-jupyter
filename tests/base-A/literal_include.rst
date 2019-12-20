Literal Includes
================

Testing literal Includes

.. literalinclude:: ./simple_program.py

should list a python highlighted program

.. literalinclude:: ./simple_program.jl
   :language: julia

this is a julia highlighted program but is in a markdown cell as the default language for the notebook is **python**

Literal includes can also have hidden output

.. literalinclude:: ./simple_program.py
   :class: hide-output