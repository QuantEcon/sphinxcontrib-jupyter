.. _config_ipynb_translator:

IPYNB Notebook Translator
=========================

.. contents:: Options
    :depth: 1
    :local:

Options available when constructing Jupyter notebooks

jupyter_allow_html_only
-----------------------

Enable this option to allow ``.. only:: html`` pass through to the notebooks. 

.. list-table:: 
   :header-rows: 1

   * - Values
   * - False (**default**)
   * - True

``conf.py`` usage:

.. code-block:: python

    jupyter_allow_html_only = True

.. note::

   This is turned on by default in the HTMLTranslator


jupyter_images_html
-------------------

Force the inclusion of images as html objects in the notebook

.. list-table:: 
   :header-rows: 1

   * - Values
   * - False 
   * - True (**default**)

.. note::

    this is useful to support the full suite of attributes associated
    with the image directive (i.e. scale).

``conf.py`` usage:

.. code-block:: python

    jupyter_images_html = True

jupyter_drop_tests
------------------

Drop ``code-blocks` that include ``:class: test``
Allows notebooks to be constructed without including tests from the 
source RST file

.. list-table:: 
   :header-rows: 1

   * - Values
   * - False
   * - True (**default**)

jupyter_drop_solutions
----------------------

**Note:** Future Feature

Drop ``code-blocks`` that include ``:class: solution``

.. list-table:: 
   :header-rows: 1

   * - Values
   * - False (**default**)
   * - True 

.. TODO:: 

    This option needs to be reviewed. A new implementation should be
    considered where the option builds a set of notebooks with and 
    without solutions so special configuration isn't required. 


