import codecs
import os.path
import docutils.io

import nbformat
import json
from sphinx.util.osutil import ensuredir, os_path
from ..writers.jupyter import JupyterWriter
from sphinx.builders import Builder
from sphinx.util.console import bold, darkgreen, brown
from sphinx.util.fileutil import copy_asset
from dask.distributed import Client, progress
from ..writers.execute_nb import ExecuteNotebookWriter
from ..writers.make_pdf import MakePDFWriter
from sphinx.util import logging
import pdb
import shutil
from distutils.spawn import find_executable
import time

class JupyterPDFBuilder(Builder):
    """
    Builds pdf notebooks
    """
    name="jupyterpdf"
    format = "ipynb"
    out_suffix = ".ipynb"
    allow_parallel = True

    _writer_class = JupyterWriter
    dask_log = dict()
    futuresInfo = dict()
    futures = []
    threads_per_worker = 1
    n_workers = 1
    logger = logging.getLogger(__name__)

    def init(self):
        if not find_executable('xelatex'):
            self.logger.warning(
                "Cannot find xelatex executable for pdf compilation"
            )
            exit(1)

        ### we should write a separate function/class to check configs
        if  self.config["jupyter_pdf_book"] and ("jupyter_pdf_book_index" not in self.config or not self.config["jupyter_pdf_book_index"]):
            self.logger.warning(
                "You have switched on the book conversion option but not specified an index/contents file for book pdf"
            )
            exit(1)
        ### initializing required classes
        self._execute_notebook_class = ExecuteNotebookWriter(self)
        self._pdf_class = MakePDFWriter(self)
        self.executedir = self.outdir + '/executed'
        self.reportdir = self.outdir + '/reports/'
        self.errordir = self.outdir + "/reports/{}"
        self.texbookdir = self.outdir + '/texbook'
        self.client = None

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

        ## check if flags are unset. Give a warning
        if ("jupyter_execute_notebooks" in self.config and self.config['jupyter_execute_notebooks'] is False) or "jupyter_execute_notebooks" not in self.config:
            self.config['jupyter_execute_notebooks'] = True
            self.logger.info("execution of notebooks is mandatory for pdf conversion, so setting it on for pdf builder.")

        if ("jupyter_target_pdf" in self.config and self.config['jupyter_target_pdf'] is False) or "jupyter_target_pdf" not in self.config:
            self.config['jupyter_target_pdf'] = True
            self.logger.info("target pdf flag is mandatory for pdf conversion, so setting it on for pdf builder.")

        # start a dask client to process the notebooks efficiently. 
        # processes = False. This is sometimes preferable if you want to avoid inter-worker communication and your computations release the GIL. This is common when primarily using NumPy or Dask Array.

        #### forced execution of notebook
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
        return docname

    def prepare_writing(self, docnames):
        self.writer = self._writer_class(self)

    def write_doc(self, docname, doctree):
        # work around multiple string % tuple issues in docutils;
        # replace tuples in attribute values with lists
        doctree = doctree.deepcopy()
        destination = docutils.io.StringOutput(encoding="utf-8")

        ### output notebooks for executing for single pdfs, the urlpath should be set to website url
        self.writer._set_ref_urlpath(self.config["jupyter_pdf_urlpath"])
        self.writer._set_jupyter_download_nb_image_urlpath(None)
        self.writer.write(doctree, destination)

        # get a NotebookNode object from a string
        nb = nbformat.reads(self.writer.output, as_version=4)
        nb = self.update_Metadata(nb)

        ### execute the notebook - keep it forcefully on
        strDocname = str(docname)
        if strDocname in self.execution_vars['dependency_lists'].keys():
            self.execution_vars['delayed_notebooks'].update({strDocname: nb})
        else:        
            self._execute_notebook_class.execute_notebook(self, nb, docname, self.execution_vars, self.execution_vars['futures'])

        ### mkdir if the directory does not exist
        outfilename = os.path.join(self.outdir, os_path(docname) + self.out_suffix)
        ensuredir(os.path.dirname(outfilename))

        try:
            with codecs.open(outfilename, "w", "utf-8") as f:
                self.writer.output = nbformat.writes(nb, version=4)
                f.write(self.writer.output)
        except (IOError, OSError) as err:
            self.logger.warning("error writing file %s: %s" % (outfilename, err))

    def update_Metadata(self, nb):
        nb.metadata.date = time.time()
        return nb

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
        self.copy_static_folder_to_subfolders(self.executedir, True)

    ## copying static folder to subfolders - will remove this later
    def copy_static_folder_to_subfolders(self, sourcedir, skiptopdir):
        dirs = os.listdir(sourcedir)
        sourcefolder = sourcedir + "/_static"
        for folder in dirs:
            if skiptopdir and "." in folder:
                continue
            if "_static" not in folder:
                destination = sourcedir + "/" + folder + "/_static"
                if os.path.exists(sourcefolder) and not os.path.exists(destination): #ensure source exists and copy to destination to ensure latest version
                    shutil.copytree(sourcefolder , destination)

    def add_bib_to_latex(self, nb, bool):
        # get a NotebookNode object from a string
        if 'latex_metadata' not in nb.metadata:
            nb.metadata['latex_metadata'] = {}

        nb.metadata['latex_metadata']['bib_include'] = bool

    def finish(self):
        self.finish_tasks.add_task(self.copy_static_files)

        #if (self.config["jupyter_execute_notebooks"]):
        # watch progress of the execution of futures
        self.logger.info(bold("Starting notebook execution and html conversion(if set in config)..."))
        #progress(self.futures)

        # save executed notebook
        error_results = self._execute_notebook_class.save_executed_notebook(self, self.execution_vars)

        ### making book pdf
        #self.copy_static_folder_to_subfolders(self.texbookdir, False)
        if "jupyter_target_pdf" in self.config and self.config["jupyter_target_pdf"] and self.config["jupyter_pdf_book"]:
            self._pdf_class.process_tex_for_book(self)

