sphinxcontrib.jupyter
=====================

A `Sphinx <http://www.sphinx-doc.org/en/stable/>`__ Extension for
Generating Jupyter Notebooks

.. |status-docs| image:: https://readthedocs.org/projects/sphinxcontrib-jupyter/badge/?version=latest
   :target: http://sphinxcontrib-jupyter.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. |status-travis| image:: https://travis-ci.org/QuantEcon/sphinxcontrib-jupyter.svg?branch=master
    :target: https://travis-ci.org/QuantEcon/sphinxcontrib-jupyter

+---------------+-----------------+
| |status-docs| | |status-travis| |
+---------------+-----------------+

Summary
-------

This sphinx extension can be used to build a collection of
`Jupyter <http://jupyter.org>`__ notebooks for Sphinx Projects.

**Note:** It has mainly been written to support the use case of
scientific publishing and hasn't been well tested outside of this
domain. Please provide feedback as an issue to this repository.

**Requires:** Sphinx >= 1.7.2 (for running tests)

Installation
------------

.. code:: bash

   pip install sphinxcontrib-jupyter

to get the latest version it is best to install directly by getting a copy of the repository, and

.. code:: bash

   python setup.py install

Usage
-----

Update project ``conf.py`` file to include the jupyter extension
and the desired **Configuration** settings (see configuration_ section below):

.. code:: python

    extensions = ["sphinxcontrib.jupyter"]

then run

.. code:: bash

    make jupyter

Usage in RST Files
------------------

A minimum configured sphinx repo is available `here <https://github.com/QuantEcon/sphinxcontrib-jupyter.minimal>`__
which generates a `sample notebook <https://github.com/QuantEcon/sphinxcontrib-jupyter.minimal#simple_notebookrst>`__

To generate an ``In`` style executable block you can use

.. code:: rst

    .. code-block:: python

.. code:: rst

    .. literalinclude::  

To include code in the notebook that is not meant for execution can be
included using ``:class: no-execute``. This is useful when writing code
that is meant to throw errors, for example.

.. code:: rst

    .. code-block:: python
        :class: no-execute

this will generate a highlighted markdown cell of the contents of the
code-block. An alias for this is ``:class: skip-test``. This is used
in the context of a test environment that is using the collection of 
notebooks to test a collection of code snippets.

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

TODO
----

1. remove need for Jupyter headers from configuration
2. include support for adding output to In cells to give a precompiled look to generated notebook
3. `Issues list <https://github.com/QuantEcon/sphinxcontrib-jupyter/issues>`__


Credits
-------

This project is supported by `QuantEcon <https://www.quantecon.org>`__

Many thanks to the contributors of this project.

* `@mmcky <https://github.com/mmcky>`__
* `@myuuuuun <https://github.com/myuuuuun>`__ 
* `@NickSifniotis <https://github.com/NickSifniotis>`__

Projects using Extension
------------------------

1. `QuantEcon Lectures <https://lectures.quantecon.org>`__

If you find this extension useful please let us know at
contact@quantecon.org

LICENSE
-------

Copyright © 2018 QuantEcon Development Team: BSD-3 All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
