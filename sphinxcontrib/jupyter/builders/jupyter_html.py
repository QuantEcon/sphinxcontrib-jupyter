import codecs
import os.path
import docutils.io

import nbformat
from sphinx.util.osutil import ensuredir, os_path
from ..writers.jupyter import JupyterWriter
from sphinx.builders import Builder
from sphinx.util.console import bold, darkgreen, brown
from sphinx.util.fileutil import copy_asset
from ..writers.execute_nb import ExecuteNotebookWriter
from ..writers.make_site import MakeSiteWriter
from ..writers.convert import convertToHtmlWriter
from dask.distributed import Client, progress
from sphinx.util import logging
from docutils import nodes
from docutils.nodes import Node
import pdb
import time
from .utils import copy_dependencies
from hashlib import md5
import json

class JupyterHtmlBuilder(Builder):
    """
    Builds html notebooks
    """
    name="jupyterhtml"
    format = "html"
    out_suffix = ".html"
    allow_parallel = True

    _make_site_class = MakeSiteWriter
    logger = logging.getLogger(__name__)

    def init(self):
        ### initializing required classes
        self._make_site_class = MakeSiteWriter(self)
        self.downloadsdir = self.outdir + "/_downloads"
        self.downloadsExecutedir = self.downloadsdir + "/executed"
        self.client = None

        if (self.config["jupyter_download_nb_execute"]):
            self.download_execution_vars = {
                'target': 'downloads',
                'dependency_lists': self.config["jupyter_dependency_lists"],
                'executed_notebooks': [],
                'delayed_notebooks': dict(),
                'futures': [],
                'delayed_futures': [],
                'destination': self.downloadsExecutedir
            }

    def get_target_uri(self, docname: str, typ: str = None):
        return ''

    def get_outdated_docs(self):
        return self.env.found_docs

    def prepare_writing(self, docnames):
        self.writer = self._writer_class(self)

        if (self.config["jupyter_download_nb_execute"]):
            copy_dependencies(self, self.downloadsExecutedir)
    
    def write_doc(self, docname, doctree):
        # work around multiple string % tuple issues in docutils;
        # replace tuples in attribute values with lists
        doctree = doctree.deepcopy()
        destination = docutils.io.StringOutput(encoding="utf-8")
        ### print an output for downloading notebooks as well with proper links if variable is set
        if "jupyter_download_nb" in self.config and self.config["jupyter_download_nb"]:

            outfilename = os.path.join(self.downloadsdir, os_path(docname) + self.out_suffix)
            ensuredir(os.path.dirname(outfilename))
            self.writer._set_ref_urlpath(self.config["jupyter_download_nb_urlpath"])
            self.writer._set_jupyter_download_nb_image_urlpath((self.config["jupyter_download_nb_image_urlpath"]))
            self.writer.write(doctree, destination)

            # get a NotebookNode object from a string
            nb = nbformat.reads(self.writer.output, as_version=4)
            nb = self.update_Metadata(nb)
            try:
                with codecs.open(outfilename, "w", "utf-8") as f:
                    self.writer.output = nbformat.writes(nb, version=4)
                    f.write(self.writer.output)
            except (IOError, OSError) as err:
                self.warn("error writing file %s: %s" % (outfilename, err))

            ### executing downloaded notebooks
            if (self.config['jupyter_download_nb_execute']):
                strDocname = str(docname)
                if strDocname in self.download_execution_vars['dependency_lists'].keys():
                    self.download_execution_vars['delayed_notebooks'].update({strDocname: nb})
                else:        
                    self._execute_notebook_class.execute_notebook(self, nb, docname, self.download_execution_vars, self.download_execution_vars['futures'])


    def update_Metadata(self, nb):
        nb.metadata.date = time.time()
        return nb

    def copy_static_files(self):
        # copy all static files
        self.logger.info(bold("copying static files... "), nonl=True)
        ensuredir(os.path.join(self.outdir, '_static'))


        # excluded = Matcher(self.config.exclude_patterns + ["**/.*"])
        for static_path in self.config["jupyter_static_file_path"]:
            entry = os.path.join(self.confdir, static_path)
            if not os.path.exists(entry):
                self.logger.warning(
                    "jupyter_static_path entry {} does not exist"
                    .format(entry))
            else:
                copy_asset(entry, os.path.join(self.outdir, "_static"))
                if (self.config["jupyter_execute_notebooks"]):
                    copy_asset(entry, os.path.join(self.executed_notebook_dir, "_static"))
        self.logger.info("done")


    def finish(self):

        self.finish_tasks.add_task(self.copy_static_files)

        if self.config["jupyter_download_nb_execute"]:
            self.save_executed_and_generate_coverage(self.download_execution_vars, 'downloads')

        if "jupyter_make_site" in self.config and self.config['jupyter_make_site']:
            self._make_site_class.build_website(self)

    def save_executed_and_generate_coverage(self, params, target, coverage = False):

            # watch progress of the execution of futures
            self.logger.info(bold("Starting notebook execution for %s and html conversion(if set in config)..."), target)
            #progress(self.futures)

            # save executed notebook
            error_results = self._execute_notebook_class.save_executed_notebook(self, params)

            ##generate coverage if config value set
            if coverage:
                ## produces a JSON file of dask execution
                self._execute_notebook_class.produce_dask_processing_report(self, params)
                
                ## generate the JSON code execution reports file
                error_results  = self._execute_notebook_class.produce_code_execution_report(self, error_results, params)

                self._execute_notebook_class.create_coverage_report(self, error_results, params)

#### html code down here
# ## generate html if needed
# if (builderSelf.config['jupyter_generate_html'] and params['target'] == 'website'):
#     builderSelf._convert_class.convert(executed_nb, filename, language_info, params['destination'], passed_metadata['path'])

#### metadata of files in excuted ones

## {"metadata": {"path": builderSelf.executed_notebook_dir, "filename": filename, "filename_with_path": full_path}}
