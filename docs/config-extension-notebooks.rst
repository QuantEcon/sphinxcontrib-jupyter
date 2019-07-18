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



.. TODO::

    #. jupyter_write_metadata
    #. jupyter_options
    #. jupyter_drop_solutions
    #. jupyter_drop_tests
    #. jupyter_ignore_no_execute
    #. jupyter_ignore_skip_test
    #. jupyter_allow_html_only
    #. jupyter_target_html
    #. jupyter_images_markdown


