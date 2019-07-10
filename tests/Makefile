SHELL := bash
#
# Makefile for Sphinx Extension Test Cases
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = python -msphinx
SPHINXPROJ    = sphinxcontrib-jupyter-testcases
#BASE
SOURCEDIR     = base/
BUILDDIR      = base/_build
BUILDCOVERAGE = base/_build_coverage
#PDF
SOURCEPDF = pdf/
BUILDPDF = pdf/_build/

CORES 		  = 4

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

rst-test: clean jupyter pdf
	python check_diffs.py

pdf:
	@$(SPHINXBUILD) -M jupyter "$(SOURCEPDF)" "$(BUILDPDF)" $(SPHINXOPTS) $(O)

server:
	cd _build/jupyter && jupyter notebook

clean-coverage:
	rm -rf $(BUILDCOVERAGE)

coverage: clean-coverage
	@$(SPHINXBUILD) -M jupyter "$(SOURCEDIR)" "$(BUILDCOVERAGE)" $(SPHINXOPTS) $(O) -D jupyter_make_coverage=1 -D jupyter_make_site=0 -D jupyter_generate_html=0 -D jupyter_ignore_skip_test=0 -D jupyter_download_nb=0 

coverage-parallel: clean-coverage
	@$(SPHINXBUILD) -M jupyter "$(SOURCEDIR)" "$(BUILDCOVERAGE)" $(SPHINXOPTS) $(O) -D jupyter_make_coverage=1 -D jupyter_make_site=0 -D jupyter_generate_html=0 -D jupyter_ignore_skip_test=0 -D jupyter_download_nb=0 -D jupyter_number_workers=$(CORES)

jupyter-parallel:
	@$(SPHINXBUILD) -M jupyter "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O) -D jupyter_number_workers=$(CORES)

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O) -P