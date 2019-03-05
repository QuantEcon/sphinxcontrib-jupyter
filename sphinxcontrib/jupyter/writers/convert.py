import nbformat
from nbconvert import HTMLExporter
import glob
import os
from sphinx.util.osutil import ensuredir

SOURCE_PY = "_build/jupyter/executed/Python"
BUILD_PY = "_build/html/Python"

class convertToHtmlWriter():
    
    """
    Convert IPYNB to HTML using nbconvert and QuantEcon Template
    """
    def __init__(self, context):
        for path in [BUILD_PY, BUILD_PY+"_downloads/"]:
            ensuredir(path)
        self.html_exporter = HTMLExporter()
        self.html_exporter.template_file = context.config["jupyter_html_template"]

    def convert(self, nb, filename):
        #Convert to HTML
        #fl_html = nb.replace(SOURCE_PY, BUILD_PY).replace(".ipynb", ".html")
        html_path = BUILD_PY + "{}.html".format(filename)
        #print("{} -> {}".format(nb, fl_html))
        with open(html_path, "w") as f:
            html, resources = self.html_exporter.from_notebook_node(nb)
            f.write(html)
        # Generate set of download notebooks (removing preamble)
        # download_nb = nb.replace(SOURCE_PY, BUILD_PY+"_downloads/")
        # print("{} -> {}".format(nb, download_nb))
        # with open(nb, encoding="UTF-8") as f:
        #     nb = nbformat.read(f, as_version=4)
        # nb['cells'] = nb['cells'][1:]                #skip first code-cell as preamble
        # #Write Executed Notebook as File
        # with open(download_nb, "wt", encoding="UTF-8") as f:
        #         nbformat.write(nb, f)