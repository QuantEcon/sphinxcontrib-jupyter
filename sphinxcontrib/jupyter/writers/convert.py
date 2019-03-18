import nbformat
from nbconvert import HTMLExporter
import glob
import os
from sphinx.util.osutil import ensuredir

SOURCE_PY = "_build/jupyter/executed/python/"
BUILD_PY = "_build/jupyter/html/python/"
SOURCE_JL = "_build/jupyter/executed/julia/"
BUILD_JL = "_build/jupyter/html/julia/"
DOWNLOAD_PY = BUILD_PY + "_downloads/"
DOWNLOAD_JL = BUILD_JL + "_downloads/"

class convertToHtmlWriter():
    
    """
    Convert IPYNB to HTML using nbconvert and QuantEcon Template
    """
    def __init__(self, parentSelf):
        for path in [BUILD_PY, BUILD_PY+"_downloads/"]:
            ensuredir(path)
        self.html_exporter = HTMLExporter()
        self.html_exporter.template_file = parentSelf.config["jupyter_html_template"]

    def convert(self, nb, filename, language):
        fl_nb = ''
        fl_html = ''
        #Convert to HTML
        if (language.language.find('python') != -1):
            fl_nb = SOURCE_PY + "{}.ipynb".format(filename)
            fl_html = BUILD_PY + "{}.html".format(filename)
            download_nb = DOWNLOAD_PY + "{}.ipynb".format(filename)
            ensuredir(BUILD_PY)
            ensuredir(DOWNLOAD_PY)
        elif (language.language.find('julia') != -1):
            fl_nb = SOURCE_JL + "{}.ipynb".format(filename)
            fl_html = BUILD_JL + "{}.html".format(filename)
            download_nb = DOWNLOAD_JL + "{}.ipynb".format(filename)
            ensuredir(BUILD_JL)
            ensuredir(DOWNLOAD_JL)
        print("{} -> {}".format(fl_nb, fl_html))

        with open(fl_html, "w") as f:
            html, resources = self.html_exporter.from_notebook_node(nb)
            f.write(html)

        print("{} -> {}".format(fl_nb, download_nb))

        nb['cells'] = nb['cells'][1:]                #skip first code-cell as preamble

        #Write Executed Notebook as File
        with open(download_nb, "wt", encoding="UTF-8") as f:
                nbformat.write(nb, f)