import nbformat
from nbconvert import HTMLExporter
import glob
import os
from io import open
from sphinx.util.osutil import ensuredir

JUPYTER_WEBSITE = "_build_website/"
#JUPYTER_COVERAGE = "_build_coverage/{}/jupyter"
#JUPYTER_ERROR = "_build_coverage/reports/{}"
#JUPYTER_COVERAGE = "_build_coverage/{}/jupyter"

class makeSiteWriter():
    """
    Makes website for each package
    """
    def __init__(self):
        mkdir _build_website/
	mkdir _build_website/_static
	mkdir _build_website/_downloads
	mkdir _build_website/_downloads/ipynb
	mkdir _build_website/_downloads/ipynb/py
	mkdir _build_website/_downloads/ipynb/jl
	#Assemble
	rsync _build/jupyter/html/*.html _build_website/
	rsync -r _build/jupyter/jupyter/_static/ _build_website/_static/
	rsync -r theme/qe/ _build_website/_static
	-rsync _build/jupyter/reports/code-execution-results.json _build_website/_static/
	#FrontEnd
	rsync source.frontend/*.html _build_website/
	#Download Notebooks
	rsync _build/jupyter/html/_downloads/*.ipynb _build_website/_downloads/ipynb/py
	rsync _build/jupyter/html/_downloads/*.ipynb _build_website/_downloads/ipynb/jl



