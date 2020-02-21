.. _config_html_translator:

IPYNB(HTML) Notebook Translator
===============================

.. contents:: Options
    :depth: 1
    :local:

Options available when constructing Jupyter notebooks that are
targeting HTML and website support

jupyter_html_template  
---------------------

Specify path to nbconvert html template file

.. note::

    Documentation on nbconvert templates can be found 
    `here <https://nbconvert.readthedocs.io/en/latest/customizing.html#Customizing-nbconvert>`_

``conf.py`` usage:

.. code-block:: python

    jupyter_html_template = "theme/template/<file>.tpl"

jupyter_template_path
---------------------

Specify path for templates

.. list-table:: 
   :header-rows: 1

   * - Value
   * - "templates" (**default**)

``conf.py`` usage:

.. code-block:: python

    jupyter_template_path = "templates"

.. TODO: Should this be in general settings

jupyter_make_site
-----------------

Enable sphinx to construct a complete website

.. todo::

    Document all the extra elements this option does over jupyter_generate_html

This option:

#. fetches coverage statistics if `coverage <coverage_extension_coverage>`_ is enabled. 

``conf.py`` usage:

.. code-block:: python

    jupyter_make_site = True

jupyter_download_nb
-------------------

Request Sphinx to generate a collection of download notebooks to support a website

``conf.py`` usage:

.. code-block:: python

    jupyter_download_nb = True

jupyter_download_nb_images_urlpath
----------------------------------

Apply a url prefix when writing images in Jupyter notebooks for `download` notebook set. 

``conf.py`` usage:

.. code-block:: python

    jupyter_images_urlpath = "s3://<path>/_static/img/"

jupyter_theme
-------------

Specify theme name

``conf.py`` usage:

.. code-block:: python

    jupyter_theme = <theme-name>

The theme should be located in the path of `jupyter_theme_path`. The default
path would be: ``theme/<theme-name>/``

jupyter_theme_path
------------------

Specify location for theme files

.. list-table:: 
   :header-rows: 1

   * - Value
   * - "theme" (**default**)

``conf.py`` usage:

.. code-block:: python

    jupyter_theme_path = "theme"

.. TODO: should this be general settings?