.. _sphinx_setup:

Sphinx Setup
============

To initially setup a Sphinx project, please refer `here <https://www.sphinx-doc.org/en/master/usage/quickstart.html>`__

.. note::

    QuantEcon is currently developing a quickstart to assist with setting up a
    sphinx project customised to use this extension and provide more guidance
    with configuration.

Update the project ``conf.py`` file to include the jupyter extension
and add the desired **configuration** settings 
(see :doc:`Extension Configuration <config-extension>` section):

.. code:: python

    extensions = ["sphinxcontrib.jupyter"]

once the extension is installed you can then run:

.. code:: bash

    make jupyter

See :doc:`Extension Configuration <config-extension>` section for details 
on how to configure the extension.