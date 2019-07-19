.. _config_extension_execution:

Executing Notebooks
===================

jupyter_execute_nb
------------------

Enables the execution of generated notebooks

.. list-table:: 
   :header-rows: 1

   * - Values
   * - False (**default**)
   * - True 

.. todo::

    deprecate this option in favour of jupyter_execute_notebooks

jupyter_execute_notebooks
-------------------------

Enables the execution of generated notebooks

.. list-table:: 
   :header-rows: 1

   * - Values
   * - False (**default**)
   * - True 

``conf.py`` usage:

.. code-block:: python

    jupyter_execute_notebooks = True

jupyter_dependency_lists
------------------------

Dependency of notebooks on other notebooks for execution can also 
be added to the configuration file above in the form of a dictionary. 
The key/value pairs will contain the names of the notebook files.

``conf.py`` usage:

.. code-block:: python

   # add your dependency lists here
   jupyter_dependency_lists = {
      'python_advanced_features' : ['python_essentials','python_oop'],
      'discrete_dp' : ['dp_essentials'],
   }


jupyter_number_workers
----------------------

Specify the number cores to use with dask

.. list-table:: 
   :header-rows: 1

   * - Values
   * - Integer (**default** = 1)

``conf.py`` usage:

    jupyter_number_workers = 4


jupyter_threads_per_worker
--------------------------

Specify the number of threads per worker for dask

.. list-table:: 
   :header-rows: 1

   * - Values
   * - Integer (**default** = 1)

``conf.py`` usage:

    jupyter_threads_per_worker = 1

