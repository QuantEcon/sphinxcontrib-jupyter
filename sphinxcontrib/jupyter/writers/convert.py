import nbformat
from nbconvert import HTMLExporter
import os
from io import open
from sphinx.util.osutil import ensuredir

BUILD = "_build/jupyter/html/"

class convertToHtmlWriter():
    
    """
    Convert IPYNB to HTML using nbconvert and QuantEcon Template
    """
    def __init__(self, parentSelf):
        for path in [BUILD]:
            ensuredir(path)
        self.html_exporter = HTMLExporter()
        if (parentSelf):
            self.html_exporter.template_file = parentSelf.config["jupyter_html_template"]
        else:
            self.html_exporter.template_file = self.config["jupyter_html_template"]

    def convert(self, nb, filename, language, base_path, path=None):
        fl_nb = ''
        fl_html = ''
        relative_path = ''
        #Convert to HTML
        if path:
            relative_path = path.replace(base_path,'')
            relative_path = relative_path[1:]
        build_path = BUILD +  relative_path
        ensuredir(build_path)
        fl_html = build_path + "/" + "{}.html".format(filename)
        
        with open(fl_html, "w") as f:
            html, resources = self.html_exporter.from_notebook_node(nb)
            f.write(html)

        nb['cells'] = nb['cells'][1:] #skip first code-cell as preamble

        # #Write Executed Notebook as File
        # if (nb['metadata']['download_nb'] == True):
        #     with open(download_nb, "wt", encoding="UTF-8") as f:
        #             nbformat.write(nb, f)
