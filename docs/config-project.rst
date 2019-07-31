
.. _config_project:

Managing Large Projects
=======================

Large projects may require different build pathways due to the time required 
for execution of embedded code. This can be done by modifying the ``Makefile``
to accomodate multiple build pathways. 

You may, for example, wish to leave ``make jupyter`` simply building notebooks
while setting up an alternative ``make`` command to target a full ``website`` 
build. 

In the ``Makefile`` you can add an alternative build target such as:

.. code-block:: bash
    
    BUILDWEBSITE  = _build/website

and then you can modify options (set in the ``conf.py`` file) using the `-D` flag. 

.. code-block:: bash

        website:
            @$(SPHINXBUILD) -M jupyter "$(SOURCEDIR)" "$(BUILDWEBSITE)" $(SPHINXOPTS) $(O) -D jupyter_make_site=1 -D jupyter_generate_html=1 -D jupyter_download_nb=1 -D jupyter_execute_notebooks=1 -D jupyter_target_html=1 -D jupyter_images_markdown=0 -D jupyter_html_template="theme/templates/lectures-nbconvert.tpl" -D jupyter_download_nb_urlpath="https://lectures.quantecon.org/"

this will setup a new folder ``_build/website`` for the new build pathway to 
store resultant files from the options selected.

.. note:: 

    this method also preserves the ``sphinx`` cache mechanism for each build pathway.

.. warning::

    Issue `#199 <https://github.com/QuantEcon/sphinxcontrib-jupyter/issues/199>`_ will
    alter this approach to include all `configuration` settings in the ``conf.py`` file
    and then the different pipelines can be switched off in the Makefile which will 
    be less error prone. 