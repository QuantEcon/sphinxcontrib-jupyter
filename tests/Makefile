SHELL := bash
#
# Makefile for Sphinx Extension Test Cases
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = python -msphinx
SPHINXPROJ    = sphinxcontrib-jupyter-testcases
#JupyterCodeTranslator (Code Only)
SOURCECODE     = code/
BUILDCODE      = code/_build
#BASE
SOURCEDIR     = base/
BUILDDIR      = base/_build
BUILDCOVERAGE = base/_build_coverage
BUILDWEBSITE  = base/_build_website
#PDF
SOURCEPDF = pdf/
BUILDPDF = pdf/_build/
#no_inline_exercises
SOURCENOEX     = no_inline_exercises/
BUILDNOEX      = no_inline_exercises/_build

CORES 		  = 4

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile pdf rst-test code

test: clean clean-pdf jupyter pdf
	python check_diffs.py

no-inline:
	@$(SPHINXBUILD) -M jupyter "$(SOURCENOEX)" "$(BUILDNOEX)" $(SPHINXOPTS) $(O)

clean-no-inline:
	rm -rf $(BUILDNOEX)

no-inline-test: clean-no-inline no-inline
	python check_diffs.py

preview:
ifneq (,$(filter $(parallel),website Website))
	cd _build/jupyter_html/ && python -m http.server
else
ifdef lecture
	cd _build/jupyter/ && jupyter notebook $(basename $(lecture)).ipynb
else
	cd _build/jupyter/ && jupyter notebook
endif
endif

clean-execute:
	rm -rf $(BUILDDIR)/execute

clean-coverage:
	rm -rf $(BUILDCOVERAGE)

clean-website:
	rm -rf $(BUILDDIR)/jupyterhtml
	rm -rf $(BUILDDIR)/jupyter_html


clean-pdf:
	rm -rf $(BUILDDIR)/jupyterpdf

clean-jupyter:
	rm -rf $(BUILDDIR)

#### TODO - Add these back in once test cases are setup ####
coverage:
ifneq (,$(filter $(parallel),true True))
	@$(SPHINXBUILD) -M jupyter "$(SOURCEDIR)" "$(BUILDCOVERAGE)" $(SPHINXOPTS) $(O) -D jupyter_make_coverage=1 -D jupyter_execute_notebooks=1 -D jupyter_ignore_skip_test=0 -D jupyter_number_workers=$(CORES)
else
	@$(SPHINXBUILD) -M jupyter "$(SOURCEDIR)" "$(BUILDCOVERAGE)" $(SPHINXOPTS) $(O) -D jupyter_make_coverage=1 -D jupyter_execute_notebooks=1 -D jupyter_ignore_skip_test=0
endif

website:
ifneq ($(strip $(parallel)),)
	@$(SPHINXBUILD) -M jupyterhtml "$(SOURCEDIR)" "$(BUILDWEBSITE)" $(FILES) $(SPHINXOPTS) $(O) -D jupyter_make_site=1 -D jupyter_generate_html=1 -D jupyter_download_nb=1 -D jupyter_execute_notebooks=1 -D jupyter_target_html=1 -D jupyter_download_nb_image_urlpath="https://s3-ap-southeast-2.amazonaws.com/python.quantecon.org/_static/" -D jupyter_images_markdown=0 -D jupyter_html_template="python-html.tpl" -D jupyter_download_nb_urlpath="https://python.quantecon.org/" -D jupyter_coverage_dir=$(BUILDCOVERAGE) -D jupyter_number_workers=$(parallel)

else
	@$(SPHINXBUILD) -M jupyterhtml "$(SOURCEDIR)" "$(BUILDWEBSITE)" $(FILES) $(SPHINXOPTS) $(O) -D jupyter_make_site=1 -D jupyter_generate_html=1 -D jupyter_download_nb=1 -D jupyter_execute_notebooks=1 -D jupyter_target_html=1 -D jupyter_download_nb_image_urlpath="https://s3-ap-southeast-2.amazonaws.com/python.quantecon.org/_static/" -D jupyter_images_markdown=0 -D jupyter_html_template="python-html.tpl" -D jupyter_download_nb_urlpath="https://python.quantecon.org/" -D jupyter_coverage_dir=$(BUILDCOVERAGE)
endif

pdf:
ifneq ($(strip $(parallel)),)
	@$(SPHINXBUILD) -M jupyterpdf "$(SOURCEDIR)" "$(BUILDDIR)" $(FILES) $(SPHINXOPTS) $(O) -D jupyter_latex_template="latex.tpl" -D jupyter_latex_template_book="latex_book.tpl" -D jupyter_images_markdown=1 -D jupyter_execute_notebooks=1 -D jupyter_target_pdf=1 -D jupyter_number_workers=$(parallel)

else
	@$(SPHINXBUILD) -M jupyterpdf "$(SOURCEDIR)" "$(BUILDDIR)" $(FILES) $(SPHINXOPTS) $(O) -D jupyter_latex_template="latex.tpl" -D jupyter_latex_template_book="latex_book.tpl" -D jupyter_images_markdown=1 -D jupyter_execute_notebooks=1 -D jupyter_target_pdf=1
endif

execute:
ifneq ($(strip $(parallel)),)
	@@$(SPHINXBUILD) -M execute "$(SOURCEDIR)" "$(BUILDDIR)" $(FILES) $(SPHINXOPTS) $(O) -D jupyter_template_coverage_file_path="error_report_template.html" -D jupyter_number_workers=$(parallel)

else
	@$(SPHINXBUILD) -M execute "$(SOURCEDIR)" "$(BUILDDIR)" $(FILES) $(SPHINXOPTS) $(O) -D jupyter_template_coverage_file_path="error_report_template.html"
endif

code:
	@$(SPHINXBUILD) -M jupytercode "$(SOURCECODE)" "$(BUILDCODE)" $(SPHINXOPTS) $(O)

jupyterbase:
	@$(SPHINXBUILD) -M jupyterbase "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
