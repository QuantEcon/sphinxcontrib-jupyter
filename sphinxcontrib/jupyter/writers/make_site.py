import os
import shutil
from sphinx.util.osutil import ensuredir
from distutils.dir_util import copy_tree
from sphinx.util import logging

JUPYTER_WEBSITE = "_build_website/"
#JUPYTER_COVERAGE = "_build_coverage/{}/jupyter"
#JUPYTER_ERROR = "_build_coverage/reports/{}"
#JUPYTER_COVERAGE = "_build_coverage/{}/jupyter"

class MakeSiteWriter():
    """
    Makes website for each package
    """
    logger = logging.getLogger(__name__)
    def __init__(self):
        pass
    def build_website(self):
        if os.path.exists("_build_website"):
            shutil.rmtree("_build_website")

        ## copies the html and downloads folder
        shutil.copytree("_build/jupyter/html/","_build_website/", symlinks=True)

        ## copies all the static files
        shutil.copytree("_build/jupyter/_static/","_build_website/_static/", symlinks=True)

        ## copies all theme files to _static folder 
        if os.path.exists("theme/qe"):
            copy_tree("theme/qe", "_build_website/_static/", preserve_symlinks=1)
        else:
            self.logger.warning("Theme folder not present. Consider creating a theme folder for static assets")

        ## copies the helper html files 
        if os.path.exists("theme/qe"):
            copy_tree("source.frontend", "_build_website/", preserve_symlinks=1)
        else:
            self.logger.warning("Source frontend folder not present. Consider creating a source.frontend folder for html helpers")

        ## copies the report of execution results
        shutil.copy2("_build/jupyter/reports/code-execution-results.json", "_build_website/_static/")



