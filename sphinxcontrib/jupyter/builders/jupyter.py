import codecs
import os.path
import docutils.io

from sphinx.util.osutil import ensuredir, os_path
from ..writers.jupyter import JupyterWriter
from sphinx.builders import Builder
from sphinx.util.console import bold, darkgreen, brown
from sphinx.util.fileutil import copy_asset
from ..writers.execute_nb import ExecuteNotebookWriter
from dask.distributed import Client, progress
import pdb

class JupyterBuilder(Builder):
    """
    Builds Jupyter Notebook
    """
    name = "jupyter"
    format = "ipynb"
    out_suffix = ".ipynb"
    allow_parallel = True

    _writer_class = JupyterWriter
    _execute_notebook_class = ExecuteNotebookWriter()
    dask_log = dict()

    futures = []

    def init(self):
        # Check default language is defined in the jupyter kernels
        def_lng = self.config["jupyter_default_lang"]
        if  def_lng not in self.config["jupyter_kernels"]:
            self.warn(
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
                    self.warn("Unrecognise command line parameter " + instruction + ", ignoring.")

        # start a dask client to process the notebooks efficiently. 
        # processes = False. This is sometimes preferable if you want to avoid inter-worker communication and your computations release the GIL. This is common when primarily using NumPy or Dask Array.
        self.client = Client(processes=False)
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
        return docname

    def prepare_writing(self, docnames):
        self.writer = self._writer_class(self)

    def write_doc(self, docname, doctree):
        # work around multiple string % tuple issues in docutils;
        # replace tuples in attribute values with lists
        doctree = doctree.deepcopy()
        destination = docutils.io.StringOutput(encoding="utf-8")

        ### print an output for downloading notebooks as well with proper links if variable is set
        if "jupyter_download_nb" in self.config and self.config["jupyter_download_nb"] is True:

            outfilename = os.path.join(self.outdir + "/_downloads", os_path(docname) + self.out_suffix)
            ensuredir(os.path.dirname(outfilename))
            self.info(bold("starting conversion for downloads folder"))
            self.writer._set_urlpath(self.config["jupyter_download_nb_urlpath"])
            self.writer.write(doctree, destination)

            try:
                with codecs.open(outfilename, "w", "utf-8") as f:
                    f.write(self.writer.output)
            except (IOError, OSError) as err:
                self.warn("error writing file %s: %s" % (outfilename, err))

        ### output notebooks for executing
        self.info(bold("starting conversion for execution"))
        self.writer._set_urlpath(None)
        self.writer.write(doctree, destination)

        ### execute the notebook
        if (self.config["jupyter_execute_notebooks"]):
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
            self.warn("error writing file %s: %s" % (outfilename, err))

    def copy_static_files(self):
        # copy all static files
        self.info(bold("copying static files... "), nonl=True)
        ensuredir(os.path.join(self.outdir, '_static'))
        if (self.config["jupyter_execute_notebooks"]):
            self.info(bold("copying static files to executed folder... \n"), nonl=True)
            ensuredir(os.path.join(self.executed_notebook_dir, '_static'))


        # excluded = Matcher(self.config.exclude_patterns + ["**/.*"])
        for static_path in self.config["jupyter_static_file_path"]:
            entry = os.path.join(self.confdir, static_path)
            if not os.path.exists(entry):
                self.warn(
                    "jupyter_static_path entry {} does not exist"
                    .format(entry))
            else:
                copy_asset(entry, os.path.join(self.outdir, "_static"))
                if (self.config["jupyter_execute_notebooks"]):
                    copy_asset(entry, os.path.join(self.executed_notebook_dir, "_static"))
        self.info("done")


    def finish(self):
        self.finish_tasks.add_task(self.copy_static_files)

        if (self.config["jupyter_execute_notebooks"]):
            # watch progress of the execution of futures
            self.info(bold("distributed dask scheduler progressbar for notebook execution and html conversion(if set in config)..."))
            progress(self.futures)

            # save executed notebook
            error_results = self._execute_notebook_class.save_executed_notebook(self)

            ## produces a JSON file of dask execution
            self._execute_notebook_class.produce_dask_processing_report(self)
            
            # # generate the JSON code execution reports file
            error_results  = self._execute_notebook_class.produce_code_execution_report(self, error_results)

            ##generate coverage if config value set
            if self.config['jupyter_execute_nb']['coverage']:
                self._execute_notebook_class.create_coverage_report(self, error_results)
