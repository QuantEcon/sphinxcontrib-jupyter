.. _config_example:

Example `conf.py` file
======================

After running a sphinx-quickstart you can add the `jupyter` options needed
for your project in a similar fashion to what is shown belows. 

The below configuration settings are the default ones provided by the
`jupinx quickstart tool <https://jupinx.readthedocs.io/en/latest/quickstart.html>`__

.. code:: python

    # Configuration file for the Jupinx documentation builder.
    #
    # This file only contains a selection of the most common options. For a full
    # list see the documentation:
    # http://www.sphinx-doc.org/en/master/config

    # -- Path setup --------------------------------------------------------------

    # If extensions (or modules to document with autodoc) are in another directory,
    # add these directories to sys.path here. If the directory is relative to the
    # documentation root, use os.path.abspath to make it absolute, like shown here.
    #
    # import os
    # import sys
    # sys.path.insert(0, os.path.abspath('.'))


    # -- Project information -----------------------------------------------------

    project = 'DEMO'
    copyright = '2019, AUTHOR'
    author = 'AUTHOR'

    # The short X.Y version
    version = '0.1'

    # The full version, including alpha/beta/rc tags
    release = '0.1'


    # -- General configuration ---------------------------------------------------

    # Add any Sphinx extension module names here, as strings. They can be
    # extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
    # ones.
    extensions = [
        'sphinxcontrib.jupyter',
        'sphinxcontrib.bibtex',
    ]

    # Add any paths that contain templates here, relative to this directory.
    templates_path = ['templates']

    # The suffix(es) of source filenames.
    # You can specify multiple suffix as a list of string:
    #
    # source_suffix = ['.rst', '.md']
    source_suffix = '.rst'

    # The master toctree document.
    master_doc = 'index'

    # List of patterns, relative to source directory, that match files and
    # directories to ignore when looking for source files.
    # This pattern also affects html_static_path and html_extra_path.
    exclude_patterns = []


    # -- Options for HTML output -------------------------------------------------

    # The theme to use for HTML and HTML Help pages.  See the documentation for
    # a list of builtin themes.
    #
    html_theme = 'alabaster'

    # Add any paths that contain custom static files (such as style sheets) here,
    # relative to this directory. They are copied after the builtin static files,
    # so a file named "default.css" will overwrite the builtin "default.css".
    html_static_path = ['static']


    # -- Extension configuration -------------------------------------------------

    # -- jupyter build configuration ---------------------------------------------------
    jupyter_kernels = {
        'python3': {
            'kernelspec': {
                'display_name': 'Python', 
                'language': 'python3', 
                'name': 'python3'
            }, 
            'file_extension': '.py'
        }, 
        'python2': {
            'kernelspec': {
                'display_name': 'Python', 
                'language': 'python2', 
                'name': 'python2'
            }, 
            'file_extension': '.py'
        }, 
        'julia-1.1': {
            'kernelspec': {
                'display_name': 'Julia 1.1', 
                'language': 'julia', 
                'name': 'julia-1.1'
            }, 
            'file_extension': '.jl'
        }
    }

    # --------------------------------------------
    # jupyter Sphinx Extension conversion settings
    # --------------------------------------------

    # Conversion Mode Settings
    # If "all", convert codes and texts into notebook
    # If "code", convert codes only
    jupyter_conversion_mode = "all"

    jupyter_write_metadata = False

    # Location for _static folder
    jupyter_static_file_path = ["source/_static"]

    # Configure jupyter headers
    jupyter_headers = {
        "python3": [
            # nbformat.v4.new_code_cell("%autosave 0")      #@mmcky please make this an option
            ],
        "julia": [
            ],
    }

    # Filename for the file containing the welcome block
    jupyter_welcome_block = ""

    #Adjust links to target html (rather than ipynb)
    jupyter_target_html = False

    #path to download notebooks from 
    jupyter_download_nb_urlpath = None

    #allow downloading of notebooks
    jupyter_download_nb = False

    #Use urlprefix images
    jupyter_download_nb_image_urlpath = None

    #Allow ipython as a language synonym for blocks to be ipython highlighted
    jupyter_lang_synonyms = ["ipython"]

    #Execute skip-test code blocks for rendering of website (this will need to be ignored in coverage testing)
    jupyter_ignore_skip_test = True

    #allow execution of notebooks
    jupyter_execute_notebooks = False

    # Location of template folder for coverage reports
    jupyter_template_coverage_file_path = False

    # generate html from IPYNB files
    jupyter_generate_html = False

    # html template specific to your website needs
    jupyter_html_template = ""

    # latex template specific to your website needs
    jupyter_latex_template = ""

    #make website
    jupyter_make_site = False

    #force markdown image inclusion
    jupyter_images_markdown = True

    #This is set true by default to pass html to the notebooks
    jupyter_allow_html_only=True
