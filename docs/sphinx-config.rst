Sphinx Setup
============

Update project ``conf.py`` file to include the jupyter extension
and the desired **Configuration** settings (see :doc:`Extension Configuration <extension-config>` section below):

.. code:: python

    extensions = ["sphinxcontrib.jupyter"]

then run

.. code:: bash

    make jupyter