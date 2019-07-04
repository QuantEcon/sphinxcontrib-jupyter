Extension Configuration and Options
===================================

+--------------------------------+-----------------------------------------------------------------------+-----------------------+
| Option                         | Description                                                           | Default               |
+================================+=======================================================================+=======================+
| jupyter_conversion_mode        | **["all", "code"]** This option specifies which writer to use when    | "all"                 |
|                                | constructing notebooks. The "all" option produces complete notebooks  |                       |
|                                | which includes text, figures, and code. The "code" option produces    |                       |
|                                | notebooks that only contain the code blocks.                          |                       |
+--------------------------------+-----------------------------------------------------------------------+-----------------------+
| jupyter_static_file_path       | Specify path to `_static`__ folder                                    | []                    |
+--------------------------------+-----------------------------------------------------------------------+-----------------------+
| jupyter_header_block           | Add a header block to each generated notebook                         | ""                    |
+--------------------------------+-----------------------------------------------------------------------+-----------------------+
| jupyter_default_lang           | Specify default language for collection of RST files                  | "python3"             |
+--------------------------------+-----------------------------------------------------------------------+-----------------------+
| jupyter_lang_synonyms          | Specify any language synonyms. This will be used when parsing code   |                        |
|                                | blocks. For example, python and ipython have slightly different       |                       |
|                                | highlighting directives but contain code that can both be executed on |                       |
|                                | the same kernel                                                       |                       |
+--------------------------------+-----------------------------------------------------------------------+-----------------------+



.. TODO::

    jupyter_kernels
    jupyter_write_metadata
    jupyter_options
    jupyter_drop_solutions
    jupyter_drop_tests
    jupyter_ignore_no_execute
    jupyter_ignore_skip_test
    jupyter_execute_nb
    jupyter_template_coverage_file_path
    jupyter_generate_html
    jupyter_html_template
    jupyter_execute_notebooks
    jupyter_make_site
    jupyter_dependency_lists
    jupyter_threads_per_worker
    jupyter_number_workers
    jupyter_make_coverage
    jupyter_allow_html_only
    jupyter_target_html
    jupyter_download_nb
    jupyter_download_nb_urlpath
    jupyter_images_urlpath
    jupyter_images_markdown



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



Example conf.py file
---------------------

.. code:: python

    # --------------------------------------------
    # sphinxcontrib-jupyter Configuration Settings
    # --------------------------------------------

    # Conversion Mode Settings
    # If "all", convert codes and texts into jupyter notebook
    # If "code", convert code-blocks only
    jupyter_conversion_mode = "all"

    jupyter_write_metadata = True

    # Location for _static folder
    jupyter_static_file_path = ["_static"]

    # Configure Jupyter Kernels
    jupyter_kernels = {
        "python3": {
            "kernelspec": {
                "display_name": "Python",
                "language": "python3",
                "name": "python3"
                },
            "file_extension": ".py",
        },
        "julia": {
            "kernelspec": {
                "display_name": "Julia 0.6.0",
                "language": "julia",
                "name": "julia-0.6"
                },
            "file_extension": ".jl"
        }
    }

    # Configure default language for Jupyter notebooks
    # Can be changed in each notebook thanks to the ..highlight:: directive
    jupyter_default_lang = "python3"
 
    # Configure Jupyter headers
    jupyter_headers = {
        "python3": [
        ],
        "julia": [
        ],
    }

    # Prepend a Welcome Message to Each Notebook
    jupyter_welcome_block = "welcome.rst"

    # Solutions Configuration
    jupyter_drop_solutions = True

    # Tests configurations 
    jupyter_drop_tests = True

    # Add Ipython as Synonym for tests
    jupyter_lang_synonyms = ["ipython"]

    # Image Prefix (enable web storage references)
    # jupyter_images_urlpath = "https://github.com/QuantEcon/sphinxcontrib-jupyter/raw/master/tests/_static/"

    #allow execution of notebooks
    jupyter_execute_notebooks = True 

    # Location of template folder for coverage reports
    jupyter_template_coverage_file_path = "/path_to_coverage_template.html"

    # generate html from IPYNB files
    jupyter_generate_html = True
    
    # html template specific to your website needs
    jupyter_html_template = "/path_to_html_template.tpl"
    
    #path to download notebooks from 
    jupyter_download_nb_urlpath = "https://lectures.quantecon.org"

    #allow downloading of notebooks
    jupyter_download_nb = True