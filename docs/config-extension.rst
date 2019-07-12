.. _config_extension:

Extension Configuration and Options
===================================

This section provides documentation on the full suite of options available in the extension. A summary of each
option is provided in the table below along with more detailed information about each option including examples
It can be useful to have multiple configurations when working on a large project, such as compiling notebooks for
working on locally and editing and compiling the project for HTML. An example of how to set this up is 
`here <project-config>`__

An example *conf.py* is available `here <config_example>`__

The options are split into the different parts of the compilation pipeline that is available in this extension:

1. `Constructing Jupyter Notebooks`_ (General Settings)
2. `Executing Notebooks`_
3. `Converting Notebooks to HTML`_
4. `Computing Coverage Statistics`_

Summary of Options
------------------

Constructing Jupyter notebooks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

+--------------------------------+-----------------------------------------------------------------------+-----------------------+
| Option                         | Description                                                           | Default               |
+================================+=======================================================================+=======================+
| jupyter_conversion_mode        | **["all", "code"]** This option specifies which writer to use when    | None                  |
|                                | constructing notebooks. The "all" option produces complete notebooks  |                       |
|                                | which includes text, figures, and code. The "code" option produces    |                       |
|                                | notebooks that only contain the code blocks.                          |                       |
+--------------------------------+-----------------------------------------------------------------------+-----------------------+
| jupyter_static_file_path       | Specify path to `_static` folder                                      | []                    |
+--------------------------------+-----------------------------------------------------------------------+-----------------------+
| jupyter_header_block           | Add a header block to every generated notebook as a Path to RST file  | ""                    |
+--------------------------------+-----------------------------------------------------------------------+-----------------------+
| jupyter_default_lang           | Specify default language for collection of RST files                  | "python3"             |
+--------------------------------+-----------------------------------------------------------------------+-----------------------+
| jupyter_lang_synonyms          | Specify any language synonyms. This will be used when parsing code    | []                    |
|                                | blocks. For example, python and ipython have slightly different       |                       |
|                                | highlighting directives but contain code that can both be executed on |                       |
|                                | the same kernel                                                       |                       |
+--------------------------------+-----------------------------------------------------------------------+-----------------------+
| `jupyter_kernels`_             | specify kernel information for the jupyter notebook metadata          |                       |
+--------------------------------+-----------------------------------------------------------------------+-----------------------+

.. TODO::

    jupyter_write_metadata
    jupyter_options
    jupyter_drop_solutions
    jupyter_drop_tests
    jupyter_ignore_no_execute
    jupyter_ignore_skip_test
    jupyter_allow_html_only
    jupyter_target_html
    jupyter_images_markdown

Executing Notebooks
~~~~~~~~~~~~~~~~~~~

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

Converting Notebooks to HTML
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

+--------------------------------+-----------------------------------------------------------------------+-----------------------+
| Option                         | Description                                                           | Default               |
+================================+=======================================================================+=======================+
| jupyter_generate_html          | Enable sphinx to generate HTML version of notebooks                   | False                 |
+--------------------------------+-----------------------------------------------------------------------+-----------------------+
| jupyter_html_template          | Specify path to nbconvert html template file                          | ""                    |
+--------------------------------+-----------------------------------------------------------------------+-----------------------+


.. TODO:: 

    jupyter_make_site
    jupyter_template_coverage_file_path
    jupyter_download_nb
    jupyter_download_nb_urlpath
    jupyter_images_urlpath
    
    
Computing Coverage Statistics
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

+--------------------------------+-----------------------------------------------------------------------+-----------------------+
| Option                         | Description                                                           | Default               |
+================================+=======================================================================+=======================+
| jupyter_make_coverage          | Enable coverage statistics to be computed                             | False                 |
+--------------------------------+-----------------------------------------------------------------------+-----------------------+
    

Detailed Option Descriptions and Examples
-----------------------------------------

jupyter_kernels
~~~~~~~~~~~~~~~

*Default Value:* None 

Specify kernel information for the jupyter notebook metadata. This is **required** in `conf.py`.

.. code-block:: text

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

This information is used to connect to the desired jupyter kernel when starting the notebook.

.. TODO:: 

    See Issue `196 <https://github.com/QuantEcon/sphinxcontrib-jupyter/issues/196)>`__




Execution
---------

Dependency of notebooks on other notebooks for execution can also be added to the configuration file above in the form of a dictionary. 
The key/value pairs will contain the names of the notebook files. An example to illustrate this is as follows :-

.. code:: python

   # add your dependency lists here
   jupyter_dependency_lists = {
      'python_advanced_features' : ['python_essentials','python_oop'],
      'discrete_dp' : ['dp_essentials'],
   }

