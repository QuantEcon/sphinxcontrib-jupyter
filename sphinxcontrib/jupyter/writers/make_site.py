import os
import shutil
from sphinx.util.osutil import ensuredir
from distutils.dir_util import copy_tree
from sphinx.util import logging

class MakeSiteWriter():
    """
    Makes website for each package
    """
    logger = logging.getLogger(__name__)
    def __init__(self, builderSelf):
        builddir = builderSelf.outdir

        ## removing the /jupyter from path to get the top directory
        index = builddir.rfind('/jupyter')
        if index > 0:
            builddir = builddir[0:index]    
        
        ## defining directories
        self.websitedir = builddir + "/jupyter_html/"
        self.downloadipynbdir = self.websitedir + "/_downloads/ipynb/"

    def build_website(self, builderSelf):
        if os.path.exists(self.websitedir):
            shutil.rmtree(self.websitedir)

        builderSelf.themePath = builderSelf.config['jupyter_theme_path']
        themeFolder = builderSelf.config['jupyter_theme']
    
        if themeFolder is not None:
            builderSelf.themePath = builderSelf.themePath + "/" + themeFolder

        if os.path.exists(builderSelf.themePath):
            pass
        else:
            self.logger.warning("theme directory not found")
            exit()

        htmlFolder = builderSelf.themePath + "/html/"
        staticFolder = builderSelf.themePath + "/static"

        ## copies the html and downloads folder
        shutil.copytree(builderSelf.outdir + "/html/", self.websitedir, symlinks=True)

        ## copies all the static files
        shutil.copytree(builderSelf.outdir + "/_static/", self.websitedir + "_static/", symlinks=True)

        ## copies all theme files to _static folder 
        if os.path.exists(staticFolder):
            copy_tree(staticFolder, self.websitedir + "_static/", preserve_symlinks=1)
        else:
            self.logger.warning("static folder not present in the themes directory")

        ## copies the helper html files 
        if os.path.exists(htmlFolder):
            copy_tree(htmlFolder, self.websitedir, preserve_symlinks=1)
        else:
            self.logger.warning("html folder not present in the themes directory")


        if "jupyter_coverage_dir" in builderSelf.config and builderSelf.config["jupyter_coverage_dir"]:
            if os.path.exists(builderSelf.config['jupyter_coverage_dir']):
                self.coveragedir = builderSelf.config['jupyter_coverage_dir']
                ## copies the report of execution results
                if os.path.exists(self.coveragedir + "/jupyter/reports/code-execution-results.json"):
                    shutil.copy2(self.coveragedir + "/jupyter/reports/code-execution-results.json", self.websitedir + "_static/")
            else:
                self.logger.error("coverage directory not found. Please ensure to run coverage build before running website build")
        else:
            self.logger.error(" coverage directory nbot specified. Please specify coverage directory for creating website reports ")

        
        ## copies the downloads folder
        if "jupyter_download_nb" in builderSelf.config and builderSelf.config["jupyter_download_nb"]:
            if builderSelf.config["jupyter_download_nb_execute"]:
                sourceDownloads = builderSelf.outdir + "/_downloads/executed"
            else: 
                sourceDownloads = builderSelf.outdir + "/_downloads"
            if os.path.exists(sourceDownloads):
                shutil.copytree(sourceDownloads, self.downloadipynbdir, symlinks=True)
            else:
                self.logger.warning("Downloads folder not created during build")




