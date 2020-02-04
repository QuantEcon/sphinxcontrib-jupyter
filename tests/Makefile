SHELL := bash
#
# Makefile for Sphinx Extension Test Cases
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = python -msphinx
SPHINXPROJ    = sphinxcontrib-jupyter-testcases
#JupyterCodeBlockTranslator
SOURCECODE     = execute/
BUILDCODE      = execute/_build
#BASE JupyterIPYNBTranlsator
SOURCEDIR     = base/
BUILDDIR      = base/_build
#PDF JupyterHTMLTranslator
SOURCEHTML = html/
BUILDHTML = html/_build/
#PDF JupyterPDFTranslator
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

test: clean clean-pdf jupyter
	python check_diffs.py

test-base: clean jupyter
	python check_diffs.py base

no-inline:
	@$(SPHINXBUILD) -M jupyter "$(SOURCENOEX)" "$(BUILDNOEX)" $(SPHINXOPTS) $(O)

clean-no-inline:
	rm -rf $(BUILDNOEX)

no-inline-test: clean-no-inline no-inline
	python check_diffs.py

clean-website:
	rm -rf $(BUILDDIR)/jupyterhtml
	rm -rf $(BUILDDIR)/jupyter_html

clean-pdf:
	rm -rf $(BUILDDIR)/jupyterpdf

clean-jupyter:
	rm -rf $(BUILDDIR)

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
