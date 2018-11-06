# Testing RST Conversion

This provides a collection of source RST documents and compiled ``jupyter`` notebooks for testing against. 



Usage of local static folders
=============================

The following additions must be made to ``conf.py`` file.

.. code:: python

    # Add static folders per lecture
    jupyter_static_folder = True

    # Location for _static folder
    # Include in *folders* the name of each one of the lecture folders
    # in this case given by "images", "simple_notebook" and "test_static"
    folders =  ["images", "simple_notebook", "test_static"]

    # We will include the path to the subfolder _static to copy their elements
    # its first element is "_static" to have a global static folder
    jupyter_static_file_path = ["_static"]
    for i in range(len(folders)):
        jupyter_static_file_path.append(folders[i]+"/_static")


