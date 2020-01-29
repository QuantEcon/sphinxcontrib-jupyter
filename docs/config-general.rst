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


jupyter_dependencies
--------------------

Specify file or directory level dependencies

``conf.py`` usage:

.. code-block:: python

    jupyter_dependencies = {
        <dir> : ['file1', 'file2'],
        {<dir>}/<file.rst> : ['file1']
    }

this allows you to specify a companion data file for 
a given ``RST`` document and it will get copied through sphinx
to the ``_build`` folder.