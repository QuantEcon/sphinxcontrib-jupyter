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









jupyter_template_html
---------------------

Specify ``html`` template to be used by ``nbconvert``

``conf.py`` usage:

.. code-block:: python

    jupyter_template_html = <path to tpl file>

The template file should be located in the path of ``jupyter_template_path``. 
The default path would be: ``templates/<tpl file>``
