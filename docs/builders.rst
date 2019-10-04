.. _builders:

Builders
=========

This extension has the following Builders

jupyter
-------

This builder currently handles `jupyter`, `html`, and `coverage` output

.. code-block:: bash

    @$(SPHINXBUILD) -M jupyter "$(SOURCEDIR)" "$(BUILDCOVERAGE)" $(FILES) $(SPHINXOPTS) $(O)


.. warning::

    If your project needs to build `jupyter` and `html` then configuration for `html` 
    and `coverage` is currently handled through Makefile overrides. 
    The project is working on separate builders for html and coverage

Example Configuration for `HTML` production

.. code-block:: bash

    @$(SPHINXBUILD) -M jupyter "$(SOURCEDIR)" "$(BUILDWEBSITE)" $(FILES) $(SPHINXOPTS) $(O) -D jupyter_make_site=1 -D jupyter_generate_html=1 -D jupyter_download_nb=1 -D jupyter_execute_notebooks=1 -D jupyter_target_html=1 -D jupyter_download_nb_image_urlpath="https://s3-ap-southeast-2.amazonaws.com/lectures.quantecon.org/py/_static/" -D jupyter_images_markdown=0 -D jupyter_html_template="python-html.tpl" -D jupyter_download_nb_urlpath="https://lectures.quantecon.org/" -D jupyter_coverage_dir=$(BUILDCOVERAGE)


jupyterpdf
----------

This builder handles production of `pdf`

.. code-block:: bash

    @$(SPHINXBUILD) -M jupyterpdf "$(SOURCEDIR)" "$(BUILDCOVERAGE)" $(FILES) $(SPHINXOPTS) $(O)