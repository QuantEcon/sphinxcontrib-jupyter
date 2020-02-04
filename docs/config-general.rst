.. _config_general:

General Configuration
=====================

.. contents:: Options
    :depth: 1
    :local:

jupyter_language
----------------

Specifies default language for Jupyter Kernel

.. list-table:: 
   :header-rows: 1

   * - Option 
     - Description
   * - "python3" (**default**)
     - Str, default(use the python3 kernel)

``conf.py`` usage:

.. code-block:: python

    jupyter_language = "julia"

.. note::

   Other languages can be displayed (i.e. julia). This option sets the 
   primary execution language for the collection of notebooks


jupyter_lang_synonyms
---------------------

Specify any language synonyms.

This will be used when parsing code blocks. For example, python and ipython 
have slightly different highlighting directives but contain code that can both be executed on
the same kernel

``conf.py`` usage:

.. code-block:: python

    jupyter_lang_synonyms = ["pycon", "ipython"]

jupyter_execute_notebooks
-------------------------

Enables the execution of generated notebooks by calling the
`execute` builder

.. list-table:: 
   :header-rows: 1

   * - Values
   * - False (**default**)
   * - True 

``conf.py`` usage:

.. code-block:: python

    jupyter_execute_notebooks = True

.. note::

    `jupyter_dependencies <config_execution>`__ can be specified to support notebook
    execution. 

jupyter_static_file_path
-------------------------

Specify path to `_static` folder.

``conf.py`` usage:

.. code-block:: python

    jupyter_static_file_path = ["source/_static"]

.. todo::

    Is this required?