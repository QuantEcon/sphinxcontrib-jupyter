Sphinx Setup
============

To initially setup a Sphinx project, please refer `here <https://www.sphinx-doc.org/en/master/usage/quickstart.html>`__

Update the project ``conf.py`` file to include the jupyter extension
and add the desired **configuration** settings (see :doc:`Extension Configuration <extension-config>` section):

.. code:: python

    extensions = ["sphinxcontrib.jupyter"]

once the extension is installed and added to the configuration you can then run

.. code:: bash

    make jupyter

See :doc:`Extension Configuration <extension-config>` section for details on how to configure the extension.