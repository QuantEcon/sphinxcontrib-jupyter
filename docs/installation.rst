.. _installation:

Installation
============

To install the extension:

.. code-block:: bash

   pip install sphinxcontrib-jupyter

to upgrade your current installation to the latest version:

.. code-block:: bash

    pip install sphinxcontrib-jupyter --upgrade

Alternative
~~~~~~~~~~~

Anothe way to get the **latest** version it is to install directly 
by getting a copy of the `repository <https://github.com/QuantEcon/sphinxcontrib-jupyter>`__, 
and:

.. code-block:: bash

   git clone https://github.com/QuantEcon/sphinxcontrib-jupyter

and then use

.. code-block:: bash

   python setup.py install

for developers or contributors it can be useful to install using the `develop` option:

.. code-block:: bash

    python setup.py develop

this will install the package into the `site-wide` package directory which is linked to
the code in your local copy of the repository. It is **not** recommended to install this 
way for common use. 
