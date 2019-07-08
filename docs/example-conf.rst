.. _ExampleConf:

Example `conf.py` file
=======================

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