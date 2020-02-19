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

    #Builder Settings
    name="execute"
    docformat = "json"
    out_suffix = ".codetree"
    allow_parallel = True
    nbversion = 4
    #Dask Configuration
    threads_per_worker = 1
    n_workers = 1
    #-Sphinx Writer
    _writer_class = JupyterWriter

    def init(self):
        """
        Code Execution Builder

        This builder runs all code-blocks in RST files to compile
        a set of `codetree` objects that include executed outputs.

        The results are saved in `_build/execute` by default

        Notes
        -----
        1. Used by jupyter, jupyterhtml, and jupyterpdf to extract
        executed outputs.
        """
        self.executenb = ExecuteNotebookWriter(self)
        self.executedir = self.outdir
        self.codetreedir = self.outdir + "/execute/"
        self.reportdir = self.outdir + '/reports/'
        self.errordir = self.outdir + "/reports/{}"
        self.client = None

        #threads per worker for dask distributed processing
        if "jupyter_threads_per_worker" in self.config:
            self.threads_per_worker = self.config["jupyter_threads_per_worker"]

        #number of workers for dask distributed processing
        if "jupyter_number_workers" in self.config:
            self.n_workers = self.config["jupyter_number_workers"]

        # start a dask client to process the notebooks efficiently. 
        # processes = False. This is sometimes preferable if you want to avoid 
        # inter-worker communication and your computations release the GIL. 
        # This is common when primarily using NumPy or Dask Array.

        self.client = Client(processes=False, threads_per_worker = self.threads_per_worker, n_workers = self.n_workers)
        self.execution_vars = {
            'dependency_lists': self.config["jupyter_dependency_lists"],
            'executed_notebooks': [],
            'delayed_notebooks': dict(),
            'futures': [],
            'delayed_futures': [],
            'destination': self.executedir
        }
        
    def get_target_uri(self, docname: str, typ: str = None):          #TODO: @aakash is this different to method in sphinx.builder?
        return docname

    def get_outdated_docs(self):                                      #TODO: @aakash is this different to method in sphinx.builder?
        return ''
            

    def prepare_writing(self, docnames):                                #TODO: @aakash is this different to method in sphinx.builder?
        self.writer = self._writer_class(self)

    def write_doc(self, docname, doctree):
        doctree = doctree.deepcopy()
        destination = docutils.io.StringOutput(encoding="utf-8")
        self.writer.write(doctree, destination)
        nb = nbformat.reads(self.writer.output, as_version=self.nbversion)
        #Codetree and Execution
        update = check_codetree_validity(self, nb, docname)
        if not update:
            return
        # Execute the notebook
        strDocname = str(docname)
        if strDocname in self.execution_vars['dependency_lists'].keys():
            self.execution_vars['delayed_notebooks'].update({strDocname: nb})
        else:        
            self.executenb.execute_notebook(self, nb, docname, self.execution_vars, self.execution_vars['futures'])

    def create_codetree(self, nb):
        codetree = OrderedDict()
        for cell in nb.cells:
            cell = normalize_cell(cell)
            cell = create_hash(cell)
            codetree = self.create_codetree_entry(codetree, cell)
        #Build codetree file
        filename = self.executedir + "/" + nb.metadata.filename_with_path + self.out_suffix
        with open(filename, "wt", encoding="UTF-8") as json_file:
            json.dump(codetree, json_file)

    def create_codetree_entry(self, codetree, cell):
        codetree[cell.metadata.hashcode] = dict()
        key = codetree[cell.metadata.hashcode]
        if hasattr(cell, 'source'): key['source']= cell.source
        if hasattr(cell, 'outputs'): key['outputs'] = cell.outputs
        if hasattr(cell, 'metadata'): key['metadata'] = cell.metadata
        return codetree

    def finish(self):
        logger.info(bold("Starting notebook execution"))
        error_results = self.executenb.save_executed_notebook(self, self.execution_vars)
        self.executenb.produce_dask_processing_report(self, self.execution_vars)
        error_results  = self.executenb.produce_code_execution_report(self, error_results, self.execution_vars)
        self.executenb.create_coverage_report(self, error_results, self.execution_vars)