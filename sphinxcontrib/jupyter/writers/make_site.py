import os
import shutil
from sphinx.util.osutil import ensuredir
from distutils.dir_util import copy_tree
from sphinx.util import logging

class MakeSiteWriter():
    """
    Compile website from components
    """
    logger = logging.getLogger(__name__)
    
    def __init__(self, builder):
        self.builder = builder

        ## removing the /jupyter from path to get the top directory
        index = self.builder.outdir.rfind('/jupyter')
        if index > 0:
            self.outdir = self.builder.outdir[0:index]
        
        ## defining directories
        self.website_folder = self.outdir + "/jupyter_html/"
        self.download_ipynb_folder = self.website_folder + "/_downloads/ipynb/"

    def copy_theme_assets(self):
        """ copies theme assets """
        self.theme_path = self.builder.config['jupyter_theme_path']
        self.theme_folder = self.builder.config['jupyter_theme']
        if self.theme_folder is not None:
            self.theme_path = self.theme_path + "/" + self.theme_folder
        #-Check Theme Path-#
        if not os.path.exists(self.theme_path):
            self.logger.warning("[copy_theme_assets] the theme directory {} is not found".format(self.theme_path))
            exit(1)
        #-Copy HTML theme files to self.website_dir-#
        self.html_assets_source = self.theme_path + "/html/"
        if os.path.exists(self.html_assets_source):
            copy_tree(self.html_assets_source, self.website_folder, preserve_symlinks=1)
        else:
            self.logger.warning("[copy_theme_assets] html folder not present in the themes directory")   #@AAKASH will there always be an html folder required in theme folder?
        #-Copy other static assets to _static-#
        self.static_theme_source = self.theme_path + "/static"
        if os.path.exists(self.static_theme_source):
            copy_tree(self.static_theme_source, self.website_folder + "_static/", preserve_symlinks=1)
        else:
            self.logger.warning("[copy_theme_assets] static folder not present in the themes directory")

    def copy_image_library(self):
        """ copies image library """
        image_path = os.path.join(self.outdir, "_images")
        if os.path.exists(image_path):
            shutil.copytree(image_path, self.website_folder + "_images/", symlinks=True)

    def copy_download_library(self):
        """ copies download library """
        download_path = os.path.join(self.outdir, "_downloads")
        if os.path.exists(download_path):
            shutil.copytree(download_path, self.website_folder + "_downloads/", symlinks=True)

    def build_website(self):
        # clean old website
        if os.path.exists(self.website_folder):
            shutil.rmtree(self.website_folder)

        # copies html and downloads folder
        shutil.copytree(self.outdir + "/html/", self.website_folder, symlinks=True)
        self.copy_image_library()
        self.copy_download_library()
        self.copy_theme_assets()

        ## copies all the static files (TODO: disable to debug!)
        # shutil.copytree(self.outdir + "/_static/", self.website_folder + "_static/", symlinks=True)

        if "jupyter_coverage_dir" in self.builder.config and self.builder.config["jupyter_coverage_dir"]:
            if os.path.exists(self.builder.config['jupyter_coverage_dir']):
                self.coveragedir = self.builder.config['jupyter_coverage_dir']
                ## copies the report of execution results
                if os.path.exists(self.coveragedir + "/jupyter/reports/code-execution-results.json"):
                    shutil.copy2(self.coveragedir + "/jupyter/reports/code-execution-results.json", self.website_folder + "_static/")
            else:
                self.logger.error("[coverage] coverage directory {} not found. Please ensure to run coverage build \
                                    before running website build".format(self.builder.config['jupyter_coverage_dir'])
                                )

        ## copies the downloadable ipynb assets to downloads ipynb support folder
        if "jupyter_download_nb" in self.builder.config and self.builder.config["jupyter_download_nb"]:
            download_ipynb_source = self.outdir + "/_download_ipynb"
            if os.path.exists(download_ipynb_source):
                shutil.copytree(download_ipynb_source, self.download_ipynb_folder, symlinks=True)
            else:
                self.logger.warning("[make_site] IPYNB downloads folder {} not created during build".format(download_ipynb_source))



