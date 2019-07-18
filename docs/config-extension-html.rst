.. config_extension_html:

Converting Notebooks to HTML
============================

.. contents:: Options
    :depth: 1
    :local:

jupyter_generate_html
---------------------  

Enable sphinx to generate HTML versions of notebooks

.. list-table:: 
   :header-rows: 1

   * - Values
   * - False (**default**)
   * - True 

``conf.py`` usage:

.. code-block:: python

    jupyter_generate_html = True

jupyter_html_template  
---------------------

Specify path to nbconvert html template file

.. note::

    Documentation on nbconvert templates can be found 
    `here<https://nbconvert.readthedocs.io/en/latest/customizing.html#Customizing-nbconvert>`__

``conf.py`` usage:

.. code-block:: python

    jupyter_html_template = "theme/template/<file>.tpl"

jupyter_make_site
-----------------

Enable sphinx to construct a complete website

.. todo::

    Document all the extra elements this option does over jupyter_generate_html

This option:

#. fetches coverage statistics if `coverage<coverage_extension_coverage>`_ is enabled. 

``conf.py`` usage:

.. code-block:: python

    jupyter_make_site = True


jupyter_download_nb
-------------------

Request Sphinx to generate a collection of download notebooks to support a website

``conf.py`` usage:

.. code-block:: python

    jupyter_download_nb = True


jupyter_images_urlpath
----------------------

Apply a url prefix when writing images in Jupyter notebooks. This is useful when
paired with ``jupyter_download_nb`` so that download notebooks are complete with
web referenced images.

``conf.py`` usage:

.. code-block:: python

    jupyter_images_urlpath = "s3://<path>/_static/img/"



