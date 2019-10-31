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

This sphinx extension can be used to:

#. build a collection of jupyter notebooks, 
#. execute the `Jupyter <http://jupyter.org>`__ notebooks,
#. convert the executed notebooks to html using `nbconvert` with template support.

**Note:** It has mainly been written to support the use case of
scientific publishing and hasn't been well tested outside of this
domain. Please provide feedback as an issue to this repository.

**Requires:** Sphinx >= 1.7.2 (for running tests). 

Examples
--------

   * https://lectures.quantecon.org/ - series of lectures on quantitative economic modeling

Installation
------------

.. code:: bash

   pip install sphinxcontrib-jupyter

to get the **latest** version it is best to install directly by getting a copy of the repository, and

.. code:: bash

   python setup.py install

if you are wishing to make changes to the project it is best to install using

.. code:: bash

    python setup.py develop

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

The `documentation <http://sphinxcontrib-jupyter.readthedocs.io/en/latest/?badge=latest>`__ is the best resource
to find usage examples.

A minimum configured sphinx repo is available `here <https://github.com/QuantEcon/sphinxcontrib-jupyter.minimal>`__
which generates a `sample notebook <https://github.com/QuantEcon/sphinxcontrib-jupyter.minimal#simple_notebookrst>`__


.. _configuration:

Configuration
-------------

The `documentation <http://sphinxcontrib-jupyter.readthedocs.io/en/latest/?badge=latest>`__ is the best resource for
configuration settings.


Credits
-------

This project is supported by `QuantEcon <https://www.quantecon.org>`__

Many thanks to the contributors of this project.

* `@AakashGfude <https://github.com/AakashGfude>`__
* `@mmcky <https://github.com/mmcky>`__
* `@myuuuuun <https://github.com/myuuuuun>`__ 
* `@NickSifniotis <https://github.com/NickSifniotis>`__


LICENSE
-------

Copyright © 2019 QuantEcon Development Team: BSD-3 All rights reserved.

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
