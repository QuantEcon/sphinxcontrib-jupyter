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
    def __init__(self, builder):
        builddir = builder.outdir

        ## removing the /jupyter from path to get the top directory
        index = builddir.rfind('/jupyter')
        if index > 0:
            builddir = builddir[0:index]    
        
        ## defining directories
        self.websitedir = builddir + "/jupyter_html/"
        self.downloadipynbdir = self.websitedir + "/_downloads/ipynb/"

    def build_website(self, builder):
        if os.path.exists(self.websitedir):
            shutil.rmtree(self.websitedir)

        builder.themePath = builder.config['jupyter_theme_path']
        themeFolder = builder.config['jupyter_theme']
    
        if themeFolder is not None:
            builder.themePath = builder.themePath + "/" + themeFolder

        if os.path.exists(builder.themePath):
            pass
        else:
            self.logger.warning("theme directory not found")
            exit()

        htmlFolder = builder.themePath + "/html/"
        staticFolder = builder.themePath + "/static"

        ## copies the html and downloads folder
        shutil.copytree(builder.outdir + "/html/", self.websitedir, symlinks=True)

        ## copies all the static files
        shutil.copytree(builder.outdir + "/_static/", self.websitedir + "_static/", symlinks=True)

        ## copies all theme files to _static folder 
        if os.path.exists(staticFolder):
            copy_tree(staticFolder, self.websitedir + "_static/", preserve_symlinks=1)
        else:
            self.logger.warning("static folder not present in the themes directory")

        ## copies the helper html files 
        if os.path.exists(htmlFolder):
            copy_tree(htmlFolder, self.websitedir, preserve_symlinks=1)

        if os.path.exists(builder.executedir):
            self.coveragereport = builder.executedir + "/reports/code-execution-results.json"
            ## copies the report of execution results
            if os.path.exists(self.coveragereport):
                    shutil.copy2(self.coveragereport, self.websitedir + "_static/")
            else:
                self.logger.error("coverage report not found. Please ensure to run make execute for creating website reports")
        else:
            self.logger.error("Notebooks are not executed. Please run make execute for creating website reports")

        
        ## copies the downloads folder
        sourceDownloads = builder.outdir + "/_downloads"
        if os.path.exists(sourceDownloads):
            shutil.copytree(sourceDownloads, self.downloadipynbdir, symlinks=True)
        else:
            self.logger.warning("Downloads folder not created during build")




