.. _installation:

Installation
============

To install the project you will need to install it using ``pip``

.. code:: bash

   pip install sphinxcontrib-jupyter

Update project ``conf.py`` file to include the jupyter extension
and configuration values shown in section below:

.. code:: python

    extensions = ["sphinxcontrib.jupyter"]

Once you have updated the ``conf.py`` file with the additional configuration as
specified in :ref:`configuration`, you will be able to run the jupyter builder

.. code:: bash

    make jupyter

.. _configuration:

Configuration
-------------

The following additions must be made to ``conf.py`` file.

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

    # Define default language of Jupyter notebooks
    # Can be changed in each notebook thanks to the ..highlight:: directive
    jupyter_default_lang = "python3"

    # Prepend a Welcome Message to Each Notebook
    jupyter_welcome_block = "welcome.rst"
