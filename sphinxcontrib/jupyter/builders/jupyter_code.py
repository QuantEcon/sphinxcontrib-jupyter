import codecs
import os.path
import docutils.io

import nbformat
from ..writers.jupyter import JupyterWriter
from sphinx.builders import Builder
from ..writers.execute_nb import ExecuteNotebookWriter
from dask.distributed import Client
from sphinx.util import logging
from sphinx.util.console import bold
import time
from .utils import copy_dependencies, create_hash, normalize_cell, check_codetree_validity
import json
from collections import OrderedDict

logger = logging.getLogger(__name__)

class JupyterCodeBuilder(Builder):
    """
    Builds Code Builder
    """
    name="codetree"
    format = "json"
    out_suffix = ".codetree"
    allow_parallel = True

    threads_per_worker = 1
    n_workers = 1
    _writer_class = JupyterWriter

    def init(self):
        ### initializing required classes
        self._execute_notebook_class = ExecuteNotebookWriter(self)
        self.executedir = self.outdir
        self.reportdir = self.outdir + '/reports/'
        self.errordir = self.outdir + "/reports/{}"
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
            'dependency_lists': self.config["jupyter_dependency_lists"],
            'executed_notebooks': [],
            'delayed_notebooks': dict(),
            'futures': [],
            'delayed_futures': [],
            'destination': self.executedir
        }
        
    def get_target_uri(self, docname: str, typ: str = None):
        return docname

    def get_outdated_docs(self):
        for docname in self.env.found_docs:
            if docname not in self.env.all_docs:
                yield docname
                continue
            targetname = self.env.doc2path(docname, self.executedir,
                                           self.out_suffix)
            if not os.path.exists(targetname):
                yield docname


    def prepare_writing(self, docnames):
        ## instantiates the writer class with code only config value
        code_only = True
        self.writer = self._writer_class(self, code_only)

    def write_doc(self, docname, doctree):
        doctree = doctree.deepcopy()
        destination = docutils.io.StringOutput(encoding="utf-8")

        self.writer.write(doctree, destination)
        nb = nbformat.reads(self.writer.output, as_version=4)


        ### check validity of codetree and prevent execution if needed
        update = check_codetree_validity(self, nb, docname)
        if not update:
            return

        ### execute the notebook
        strDocname = str(docname)
        if strDocname in self.execution_vars['dependency_lists'].keys():
            self.execution_vars['delayed_notebooks'].update({strDocname: nb})
        else:        
            self._execute_notebook_class.execute_notebook(self, nb, docname, self.execution_vars, self.execution_vars['futures'])

    def create_codetree(self, nb):
        codetree_ds = OrderedDict()
        for cell in nb.cells:
            cell = normalize_cell(cell)
            cell = create_hash(cell)
            codetree_ds = self.create_codetree_ds(codetree_ds, cell)

        filename = self.executedir + "/" + nb.metadata.filename_with_path + self.out_suffix
        with open(filename, "wt", encoding="UTF-8") as json_file:
            json.dump(codetree_ds, json_file)

    def create_codetree_ds(self, codetree_ds, cell):
        codetree_ds[cell.metadata.hashcode] = dict()
        key = codetree_ds[cell.metadata.hashcode]
        if hasattr(cell, 'source'): key['source']= cell.source
        if hasattr(cell, 'outputs'): key['outputs'] = cell.outputs
        return codetree_ds

    def finish(self):
        # watch progress of the execution of futures
        logger.info(bold("Starting notebook execution"))

        # save executed notebook
        error_results = self._execute_notebook_class.save_executed_notebook(self, self.execution_vars)

        ## produces a JSON file of dask execution
        self._execute_notebook_class.produce_dask_processing_report(self, self.execution_vars)
        
        ## generate the JSON code execution reports file
        error_results  = self._execute_notebook_class.produce_code_execution_report(self, error_results, self.execution_vars)

        ## creates a coverage report
        self._execute_notebook_class.create_coverage_report(self, error_results, self.execution_vars)