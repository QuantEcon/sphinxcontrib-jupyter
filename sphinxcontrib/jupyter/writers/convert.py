import nbformat
from nbconvert import HTMLExporter
import glob
import os
from sphinx.util.osutil import ensuredir

SOURCE_PY = "_build/jupyter/executed/Python"
BUILD_PY = "_build/html/Python"
SOURCE_JL = "_build/jupyter/executed/Julia"
BUILD_JL = "_build/html/Julia"

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
        #Convert to HTML
        if (language.name == 'python'):
            fl_nb = SOURCE_PY + "{}.ipynb".format(filename)
            fl_html = BUILD_PY + "{}.html".format(filename)
        elif (language.name == 'julia'):
            fl_nb = SOURCE_JL + "{}.ipynb".format(filename)
            fl_html = BUILD_JL + "{}.html".format(filename)
            
        print("{} -> {}".format(fl_nb, fl_html))

        with open(fl_html, "w") as f:
            html, resources = self.html_exporter.from_notebook_node(nb)
            f.write(html)
        
        download_nb = BUILD_PY+"_downloads/" + "{}.ipynb".format(filename)
        print("{} -> {}".format(fl_nb, download_nb))

        nb['cells'] = nb['cells'][1:]                #skip first code-cell as preamble

        #Write Executed Notebook as File
        with open(download_nb, "wt", encoding="UTF-8") as f:
                nbformat.write(nb, f)