SHELL := bash
#
# Makefile for Sphinx Extension Test Cases
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = python -msphinx
SPHINXPROJ    = sphinxcontrib-jupyter-testcases
#JupyterCodeBlockTranslator
SOURCEEXECUTE     = execute/
BUILDEXECUTE      = execute/_build
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

test: test-base test-execute test-no-inline

test-base: clean jupyter
	python check_diffs.py base

test-execute: clean-execute build-execute
	python check_diffs.py execute

test-no-inline: clean-no-inline no-inline
	python check_diffs.py no_inline_exercises

build-execute:
	@$(SPHINXBUILD) -M jupyter "$(SOURCEEXECUTE)" "$(BUILDEXECUTE)" $(SPHINXOPTS) $(O)

build-no-inline:
	@$(SPHINXBUILD) -M jupyter "$(SOURCENOEX)" "$(BUILDNOEX)" $(SPHINXOPTS) $(O)

clean-execute:
	rm -rf $(BUILDEXECUTE)

clean-no-inline:
	rm -rf $(BUILDNOEX)

clean-html:
	rm -rf $(BUILDHTML)

clean-pdf:
	rm -rf $(BUILDPDF)

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
