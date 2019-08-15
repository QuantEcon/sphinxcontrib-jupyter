.. _installation:

Installation
============

To install the extension:

.. code-block:: bash

   pip install sphinxcontrib-jupyter

to upgrade your current installation to the latest version:

.. code-block:: bash

    pip install --upgrade sphinxcontrib-jupyter

.. todo:: 

    Add installation to distribute via conda-forge.
    See Issue `#160 <https://github.com/QuantEcon/sphinxcontrib-jupyter/issues/160>`__.

You can refer to the `release notes <https://github.com/QuantEcon/sphinxcontrib-jupyter/releases>`__
for information on each release.

Alternative
~~~~~~~~~~~

Another way to get the **latest** version it is to install directly 
by getting a copy of the `repository <https://github.com/QuantEcon/sphinxcontrib-jupyter>`__:

.. code-block:: bash

   git clone https://github.com/QuantEcon/sphinxcontrib-jupyter

and then use

.. code-block:: bash

   python setup.py install

Developers
~~~~~~~~~~

For developers it can be useful to install using the `develop` option:

.. code-block:: bash

    python setup.py develop

this will install the package into the `site-wide` package directory which is linked to
the code in your local copy of the repository. It is **not** recommended to install this 
way for common use. 
