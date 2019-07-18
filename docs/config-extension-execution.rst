.. _config_extension_execution:

Executing Notebooks
===================

+--------------------------------+-----------------------------------------------------------------------+-----------------------+
| Option                         | Description                                                           | Default               |
+================================+=======================================================================+=======================+
| jupyter_execute_nb             | Enables the execution of generated notebooks                          | False                 |
+--------------------------------+-----------------------------------------------------------------------+-----------------------+


.. TODO::

    jupyter_execute_notebooks
    jupyter_dependency_lists
    jupyter_threads_per_worker
    jupyter_number_workers
    jupyter_target_html = True

Dependencies
------------

Dependency of notebooks on other notebooks for execution can also be added to the configuration file above in the form of a dictionary. 
The key/value pairs will contain the names of the notebook files. An example to illustrate this is as follows :-

.. code:: python

   # add your dependency lists here
   jupyter_dependency_lists = {
      'python_advanced_features' : ['python_essentials','python_oop'],
      'discrete_dp' : ['dp_essentials'],
   }