.. _config_extension_notebooks:

Constructing Jupyter Notebooks
==============================

.. contents:: Options
    :depth: 1
    :local:

jupyter_conversion_mode
-----------------------  

Specifies which writer to use when constructing notebooks. 

.. list-table:: 
   :header-rows: 1

   * - Option 
     - Description
   * - "all" (**default**)
     - compile complete notebooks which include ``markdown cells`` and ``code blocks``
   * - "code"
     - compile notebooks that only contain the ``code blocks``.

``conf.py`` usage:

.. code-block:: python

    jupyter_conversion_mode = "all"

jupyter_static_file_path
-------------------------

Specify path to `_static` folder.

``conf.py`` usage:

.. code-block:: python

    jupyter_static_file_path = ["source/_static"]


jupyter_header_block
---------------------

Add a header block to every generated notebook by specifying an RST file

``conf.py`` usage:

.. code-block:: python

    jupyter_header_block = ["source/welcome.rst"]

jupyter_default_lang
--------------------

Specify default language for collection of RST files

``conf.py`` usage:

.. code-block:: python

    jupyter_default_lang = "python3"

jupyter_lang_synonyms
---------------------

Specify any language synonyms.

This will be used when parsing code blocks. For example, python and ipython 
have slightly different highlighting directives but contain code that can both be executed on
the same kernel

``conf.py`` usage:

.. code-block:: python

    jupyter_lang_synonyms = ["pycon", "ipython"]

jupyter_kernels
---------------

Specify kernel information for the jupyter notebook metadata. 

This is used by jupyter to connect the correct language kernel and is **required** in ``conf.py``.

``conf.py`` usage:

.. code-block:: python

    jupyter_kernels = {
        "python3": {
            "kernelspec": {
                "display_name": "Python",
                "language": "python3",
                "name": "python3"
                },
            "file_extension": ".py",
        },
    }

.. TODO:: 

    See Issue `196 <https://github.com/QuantEcon/sphinxcontrib-jupyter/issues/196)>`__

jupyter_write_metadata
----------------------

write time and date information at the top of each notebook as notebook metadata

.. note::

    This option is slated to be deprecated

jupyter_options
---------------

An dict-type object that is used by dask to control execution


.. TODO:: 

    This option needs to be reviewed

jupyter_drop_solutions
----------------------

Drop ``code-blocks`` that include ``:class: solution``

.. TODO:: 

    This option needs to be reviewed

jupyter_drop_tests
------------------

.. list-table:: 
   :header-rows: 1

   * - Values
   * - False (**default**)
   * - True 

Drop ``code-blocks` that include ``:class: test``

.. TODO::

    This option needs to be reviewed

jupyter_ignore_no_execute:
--------------------------

.. list-table:: 
   :header-rows: 1

   * - Values
   * - False (**default**)
   * - True 

When constructing notebooks this option can be enabled to ignore `:class: no-execute`
for `code-blocks`. This is useful for `html` writer for pages that are meant to fail 
but shouldn't be included in `coverage` tests. 

``conf.py`` usage:

.. code-block:: python

    jupyter_ignore_no_execute = True

jupyter_ignore_skip_test
------------------------

When constructing notebooks this option can be enabled to ignore `:class: skip-test`
for `code-blocks`.

.. list-table:: 
   :header-rows: 1

   * - Values
   * - False (**default**)
   * - True

``conf.py`` usage:

.. code-block:: python

    jupyter_ignore_skip_test = True

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

jupyter_target_html
-------------------

Enable this option to generate notebooks that favour the inclusion of ``html``
in notebooks to support more advanced features.

.. list-table:: 
   :header-rows: 1

   * - Values
   * - False (**default**)
   * - True

Supported Features:

#. html based table support
#. image inclusion as ``html`` figures

``conf.py`` usage:

.. code-block:: python

    jupyter_target_html = True


jupyter_images_markdown
-----------------------

Force the inclusion of images as native markdown

.. list-table:: 
   :header-rows: 1

   * - Values
   * - False (**default**)
   * - True

.. note::

    when this option is enabled the `:scale:` option is not supported
    in RST.

``conf.py`` usage:

.. code-block:: python

    jupyter_images_markdown = True



