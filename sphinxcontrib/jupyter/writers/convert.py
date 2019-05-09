import nbformat
from nbconvert import HTMLExporter
import glob
import os
from io import open
from sphinx.util.osutil import ensuredir

SOURCE_PY = "_build/jupyter/executed/python"
BUILD_PY = "_build/jupyter/html/python/"
SOURCE_JL = "_build/jupyter/executed/julia"
BUILD_JL = "_build/jupyter/html/julia/"
DOWNLOAD_PY = BUILD_PY + "_downloads/"
DOWNLOAD_JL = BUILD_JL + "_downloads/"

class convertToHtmlWriter():
    
    """
    Convert IPYNB to HTML using nbconvert and QuantEcon Template
    """
    def __init__(self, parentSelf):
        self.html_exporter = HTMLExporter()
        self.html_exporter.template_file = parentSelf.config["jupyter_html_template"]

    def convert(self, nb, path, filename, language):
        fl_nb = ''
        fl_html = ''
        #Convert to HTML
        if (language.language.find('python') != -1):
            for path in [BUILD_PY, DOWNLOAD_PY]:
                ensuredir(path)
            relative_path = path.replace(SOURCE_PY,'')
            if relative_path:
                relative_path = relative_path[1:]
            build_path = BUILD_PY + relative_path
            download_path = DOWNLOAD_PY + relative_path
            ensuredir(build_path)
            ensuredir(download_path)
            fl_html = build_path + "/" + "{}.html".format(filename)
            download_nb = download_path + "/" + "{}.ipynb".format(filename)
        elif (language.language.find('julia') != -1):
            for path in [BUILD_JL, DOWNLOAD_JL]:
                ensuredir(path)
            relative_path = path.replace(SOURCE_JL,'')
            if relative_path:
                relative_path = relative_path[1:]
            build_path = BUILD_JL +  relative_path
            download_path = DOWNLOAD_JL + relative_path 
            ensuredir(build_path)
            ensuredir(download_path)
            fl_html = build_path + "/" + "{}.html".format(filename)
            download_nb = download_path + "/" + "{}.ipynb".format(filename)
        #print("{} -> {}".format(fl_nb, fl_html))
        with open(fl_html, "w") as f:
            html, resources = self.html_exporter.from_notebook_node(nb)
            f.write(html)

        #print("{} -> {}".format(fl_nb, download_nb))

        nb['cells'] = nb['cells'][1:]                #skip first code-cell as preamble

        #Write Executed Notebook as File
        with open(download_nb, "wt", encoding="UTF-8") as f:
                nbformat.write(nb, f)