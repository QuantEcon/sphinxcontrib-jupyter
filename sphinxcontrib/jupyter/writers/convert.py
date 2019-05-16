import nbformat
from nbconvert import HTMLExporter
import os
from io import open
from sphinx.util.osutil import ensuredir

SOURCE = "_build/jupyter/executed"
BUILD = "_build/jupyter/html"
DOWNLOAD = BUILD + "/_downloads/"

class convertToHtmlWriter():
    
    """
    Convert IPYNB to HTML using nbconvert and QuantEcon Template
    """
    def __init__(self, parentSelf):
        for path in [BUILD, DOWNLOAD]:
            ensuredir(path)
        self.html_exporter = HTMLExporter()
        self.html_exporter.template_file = parentSelf.config["jupyter_html_template"]

    def convert(self, nb, path, filename, language):
        fl_nb = ''
        fl_html = ''
        #Convert to HTML
        relative_path = path.replace(SOURCE,'')
        if relative_path:
            relative_path = relative_path[1:]
        build_path = BUILD +  relative_path
        download_path = DOWNLOAD + relative_path 
        ensuredir(build_path)
        ensuredir(download_path)
        fl_html = build_path + "/" + "{}.html".format(filename)
        download_nb = download_path + "/" + "{}.ipynb".format(filename)
        with open(fl_html, "w") as f:
            html, resources = self.html_exporter.from_notebook_node(nb)
            f.write(html)

        #print("{} -> {}".format(fl_nb, download_nb))

        nb['cells'] = nb['cells'][1:]                #skip first code-cell as preamble

        #Write Executed Notebook as File
        with open(download_nb, "wt", encoding="UTF-8") as f:
                nbformat.write(nb, f)