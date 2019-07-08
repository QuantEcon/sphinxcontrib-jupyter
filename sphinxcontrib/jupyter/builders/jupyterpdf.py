import codecs
import os.path
import docutils.io

from sphinx.util.osutil import ensuredir, os_path
from sphinx.builders import Builder
from sphinx.util.console import bold
from ..writers.jupyter import JupyterWriter
from ..writers.execute_nb import ExecuteNotebookWriter
from dask.distributed import Client
from sphinx.util import logging

class JupyterpdfBuilder(Builder):
    """
    Builds pdf notebooks
    """
    name="jupyterpdf"
    _writer_class = JupyterWriter
    _execute_notebook_class = ExecuteNotebookWriter()
    out_suffix = ".ipynb"
    dask_log = dict()
    futuresInfo = dict()
    futures = []
    threads_per_worker = 1
    n_workers = 1
    logger = logging.getLogger(__name__)

    def init(self):
        # Check default language is defined in the jupyter kernels
        def_lng = self.config["jupyter_default_lang"]
        if  def_lng not in self.config["jupyter_kernels"]:
            self.logger.warning(
                "Default language defined in conf.py ({}) is not "
                "defined in the jupyter_kernels in conf.py. "
                "Set default language to python3"
                .format(def_lng))
            self.config["jupyter_default_lang"] = "python3"
        # If the user has overridden anything on the command line, set these things which have been overridden.
        instructions = []
        overrides = self.config['jupyter_options']
        if overrides:
            instructions = overrides.split(",")

        for instruction in instructions:
            if instruction:
                if instruction == 'code_only':
                    self.config["jupyter_conversion_mode"] = "code"
                else:
                    # Fail on unrecognised command.
                    self.logger.warning("Unrecognise command line parameter " + instruction + ", ignoring.")

        #threads per worker for dask distributed processing
        if "jupyter_threads_per_worker" in self.config:
            self.threads_per_worker = self.config["jupyter_threads_per_worker"]

        #number of workers for dask distributed processing
        if "jupyter_number_workers" in self.config:
            self.n_workers = self.config["jupyter_number_workers"]

        # start a dask client to process the notebooks efficiently. 
        # processes = False. This is sometimes preferable if you want to avoid inter-worker communication and your computations release the GIL. This is common when primarily using NumPy or Dask Array.
        self.client = Client(processes=False, threads_per_worker = self.threads_per_worker, n_workers = self.n_workers)
        self.dependency_lists = self.config["jupyter_dependency_lists"]
        self.executed_notebooks = []
        self.delayed_notebooks = dict()
        self.futures = []
        self.delayed_futures = []
        
    def get_outdated_docs(self):
        for docname in self.env.found_docs:
            if docname not in self.env.all_docs:
                yield docname
                continue
            targetname = self.env.doc2path(docname, self.outdir,
                                           self.out_suffix)
            try:
                targetmtime = os.path.getmtime(targetname)
            except OSError:
                targetmtime = 0
            try:
                srcmtime = os.path.getmtime(self.env.doc2path(docname))
                if srcmtime > targetmtime:
                    yield docname
            except EnvironmentError:
                pass
    def get_target_uri(self, docname, typ=None):
        """
		Return the target URI for a document name.
		typ can be used to qualify the link characteristic for individual builders.
		"""
        return docname

    def write_doc(self, docname, doctree):
        doctree = doctree.deepcopy()
        destination = docutils.io.StringOutput(encoding="utf-8")

         ### output notebooks for executing
        self.writer._set_urlpath(None)
        self.writer.write(doctree, destination)

		### execute the notebook
        strDocname = str(docname)
        if strDocname in self.dependency_lists.keys():
            self.delayed_notebooks.update({strDocname: self.writer.output})
        else:        
            self._execute_notebook_class.execute_notebook(self, self.writer.output, docname, self.futures)


        ### mkdir if the directory does not exist
        outfilename = os.path.join(self.outdir, os_path(docname) + self.out_suffix)
        ensuredir(os.path.dirname(outfilename))
        try:
            with codecs.open(outfilename, "w", "utf-8") as f:
                f.write(self.writer.output)
        except (IOError, OSError) as err:
            self.logger.warning("error writing file %s: %s" % (outfilename, err))

    def prepare_writing(self, docnames):
        self.writer = self._writer_class(self)
	
    def finish(self):
        self.logger.info(bold("Starting notebook execution and html conversion(if set in config)..."))

        # save executed notebook
        error_results = self._execute_notebook_class.save_executed_notebook(self)