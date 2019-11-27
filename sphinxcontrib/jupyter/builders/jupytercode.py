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
from ..writers.utils import copy_dependencies

class JupyterCodeBuilder(Builder):
    """
    Builds Code Builder
    """
    name="jupytercodeexec"
    format = "ipynb"
    out_suffix = ".ipynb"
    allow_parallel = True

    dask_log = dict()
    futuresInfo = dict()
    futures = []
    threads_per_worker = 1
    n_workers = 1
    logger = logging.getLogger(__name__)
    _writer_class = JupyterWriter

    def init(self):
        ### initializing required classes
        self._execute_notebook_class = ExecuteNotebookWriter(self)
        self.executedir = self.outdir + '/executed'
        self.client = None

        #threads per worker for dask distributed processing
        if "jupyter_threads_per_worker" in self.config:
            self.threads_per_worker = self.config["jupyter_threads_per_worker"]

        #number of workers for dask distributed processing
        if "jupyter_number_workers" in self.config:
            self.n_workers = self.config["jupyter_number_workers"]

        # # start a dask client to process the notebooks efficiently. 
        # # processes = False. This is sometimes preferable if you want to avoid inter-worker communication and your computations release the GIL. This is common when primarily using NumPy or Dask Array.

        self.client = Client(processes=False, threads_per_worker = self.threads_per_worker, n_workers = self.n_workers)
        self.execution_vars = {
            'target': 'website',
            'dependency_lists': self.config["jupyter_dependency_lists"],
            'executed_notebooks': [],
            'delayed_notebooks': dict(),
            'futures': [],
            'delayed_futures': [],
            'destination': self.executedir
        }
        
    def get_target_uri(self, docname: str, typ: str = None):
        return ''

    def get_outdated_docs(self):
        return self.env.found_docs

    def prepare_writing(self, docnames):
        code_only = True
        self.writer = self._writer_class(self, code_only)

    def write_doc(self, docname, doctree):
        doctree = doctree.deepcopy()
        destination = docutils.io.StringOutput(encoding="utf-8")

        self.writer.write(doctree, destination)
        nb = nbformat.reads(self.writer.output, as_version=4)

        ### execute the notebook
        strDocname = str(docname)
        if strDocname in self.execution_vars['dependency_lists'].keys():
            self.execution_vars['delayed_notebooks'].update({strDocname: nb})
        else:        
            self._execute_notebook_class.execute_notebook(self, nb, docname, self.execution_vars, self.execution_vars['futures'])

        ### mkdir if the directory does not exist
        outfilename = os.path.join(self.outdir, os_path(docname) + self.out_suffix)
        ensuredir(os.path.dirname(outfilename))


    def copy_static_files(self):
        # copy all static files
        self.logger.info(bold("copying static files... "), nonl=True)
        ensuredir(os.path.join(self.outdir, '_static'))
        if (self.config["jupyter_execute_notebooks"]):
            self.logger.info(bold("copying static files to executed folder... \n"), nonl=True)
            ensuredir(os.path.join(self.executed_notebook_dir, '_static'))


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
        self.save_executed_and_generate_coverage(self.execution_vars,'website', self.config['jupyter_make_coverage'])

    def save_executed_and_generate_coverage(self, params, target, coverage = False):

            # watch progress of the execution of futures
            self.logger.info(bold("Starting notebook execution for %s)..."), target)
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