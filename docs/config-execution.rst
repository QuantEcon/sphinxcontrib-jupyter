.. _config_execution:

Execution Configuration
=======================

.. contents:: Options
    :depth: 1
    :local:

Code execution is handled by a specialised `execute` builder.

jupyter_file_dependencies
--------------------------

Specify support (dependencies) for notebook collection at the `file` or 
the `directory` level.

``conf.py`` usage:

.. code-block:: python

   jupyter_dependencies = {
       <dir> : ['file1', 'file2'],
       {<dir>}/<file.rst> : ['file1']
   }

.. note::

    to specify a support file at the root level of the source directory
    the key should be `""`

jupyter_notebook_dependencies
-----------------------------

Dependency of notebooks on other notebooks for execution can 
be added to the configuration file above in the form of a dictionary. 
The key/value pairs will contain the names of the notebook files.

``conf.py`` usage:

.. code-block:: python

   # add your dependency lists here
   jupyter_notebook_dependencies = {
      'python_advanced_features' : ['python_essentials','python_oop'],
      'discrete_dp' : ['dp_essentials'],
   }

jupyter_number_workers
-------------------------

Specify the number cores to use with dask

.. list-table:: 
   :header-rows: 1

   * - Values
   * - Integer (**default** = 1)

``conf.py`` usage:

    jupyter_number_workers = 4


jupyter_execution_threads_per_worker
------------------------------------

Specify the number of threads per worker for dask

.. list-table:: 
   :header-rows: 1

   * - Values
   * - Integer (**default** = 1)

``conf.py`` usage:

    jupyter_threads_per_worker = 1

jupyter_coverage_report_template
-----------------------------------

Provide path to template coverage report file

.. todo::

    Document format for template

``conf.py`` usage:

.. code-block:: python

    jupyter_template_coverage_file_path = "theme/templates/<file>.json"

.. warning::

    ``coverage`` will currently produce a ``json`` report
    that can be used to support an execution status page. But adding
    badges and a status page needs to be made into an option and 
    specified via the default theme. 
    See `#237 <https://github.com/QuantEcon/sphinxcontrib-jupyter/issues/237>`__


jupyter_options
---------------

An dict-type object that is used by dask to control execution


.. TODO:: 

    @aakash is this used?

jupyter_drop_tests
------------------

**Note:** Future Feature?

Drop ``code-blocks` that include ``:class: test``

.. list-table:: 
   :header-rows: 1

   * - Values
   * - False (**default**)
   * - True 

.. TODO::

    This option should be added to `execute` builder so tests can 
    be switched on/off for execution testing

jupyter_ignore_no_execute:
--------------------------

**Note:** Deprecate?

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

.. todo::

    @aakash this is no longer required as all code-blocks are run correct?

jupyter_ignore_skip_test
------------------------

**Note:** Deprecate?

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

.. todo::

    @aakash is this required?