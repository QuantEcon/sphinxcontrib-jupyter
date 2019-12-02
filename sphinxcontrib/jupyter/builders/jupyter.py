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
import pdb
import time
import json
from hashlib import md5
from ..writers.utils import copy_dependencies
from munch import munchify

class JupyterBuilder(Builder):
    """
    Builds Jupyter Notebook
    """
    name = "jupyter"
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
        ### initializing required classes
        self.executedir = self.confdir + '/_build/jupytercode/codetree'

        ########## RECHECK THESE CHECKS
        # # Check default language is defined in the jupyter kernels
        # def_lng = self.config["jupyter_default_lang"]
        # if  def_lng not in self.config["jupyter_kernels"]:
        #     self.logger.warning(
        #         "Default language defined in conf.py ({}) is not "
        #         "defined in the jupyter_kernels in conf.py. "
        #         "Set default language to python3"
        #         .format(def_lng))
        #     self.config["jupyter_default_lang"] = "python3"
        # # If the user has overridden anything on the command line, set these things which have been overridden.
        # instructions = []
        # overrides = self.config['jupyter_options']
        # if overrides:
        #     instructions = overrides.split(",")

        # for instruction in instructions:
        #     if instruction:
        #         if instruction == 'code_only':
        #             self.config["jupyter_conversion_mode"] = "code"
        #         else:
        #             # Fail on unrecognised command.
        #             self.logger.warning("Unrecognise command line parameter " + instruction + ", ignoring.")
        
        # if (self.config["jupyter_download_nb_execute"]):
        #     if self.client is None:
        #         self.client = Client(processes=False, threads_per_worker = self.threads_per_worker, n_workers = self.n_workers)
        #     self.download_execution_vars = {
        #         'target': 'downloads',
        #         'dependency_lists': self.config["jupyter_dependency_lists"],
        #         'executed_notebooks': [],
        #         'delayed_notebooks': dict(),
        #         'futures': [],
        #         'delayed_futures': [],
        #         'destination': self.downloadsExecutedir
        #     }

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

        ## copies the dependencies to the notebook folder
        copy_dependencies(self)

        # if (self.config["jupyter_download_nb_execute"]):
        #     copy_dependencies(self, self.downloadsExecutedir)
            
    def write_doc(self, docname, doctree):
        # work around multiple string % tuple issues in docutils;
        # replace tuples in attribute values with lists
        doctree = doctree.deepcopy()
        destination = docutils.io.StringOutput(encoding="utf-8")
        ### print an output for downloading notebooks as well with proper links if variable is set
        # if "jupyter_download_nb" in self.config and self.config["jupyter_download_nb"]:

        #     outfilename = os.path.join(self.downloadsdir, os_path(docname) + self.out_suffix)
        #     ensuredir(os.path.dirname(outfilename))
        #     self.writer._set_ref_urlpath(self.config["jupyter_download_nb_urlpath"])
        #     self.writer._set_jupyter_download_nb_image_urlpath((self.config["jupyter_download_nb_image_urlpath"]))
        #     self.writer.write(doctree, destination)

        #     # get a NotebookNode object from a string
        #     nb = nbformat.reads(self.writer.output, as_version=4)
        #     nb = self.update_Metadata(nb)
        #     try:
        #         with codecs.open(outfilename, "w", "utf-8") as f:
        #             self.writer.output = nbformat.writes(nb, version=4)
        #             f.write(self.writer.output)
        #     except (IOError, OSError) as err:
        #         self.warn("error writing file %s: %s" % (outfilename, err))

        #     ### executing downloaded notebooks
        #     if (self.config['jupyter_download_nb_execute']):
        #         strDocname = str(docname)
        #         if strDocname in self.download_execution_vars['dependency_lists'].keys():
        #             self.download_execution_vars['delayed_notebooks'].update({strDocname: nb})
        #         else:        
        #             self._execute_notebook_class.execute_notebook(self, nb, docname, self.download_execution_vars, self.download_execution_vars['futures'])

        ### output notebooks for executing
        # self.writer._set_ref_urlpath(None)
        # self.writer._set_jupyter_download_nb_image_urlpath(None)
        self.writer.write(doctree, destination)

        # get a NotebookNode object from a string
        nb = nbformat.reads(self.writer.output, as_version=4)
        nb = self.update_Metadata(nb)

        # ### execute the notebook
        # if (self.config["jupyter_execute_notebooks"]):
        #     strDocname = str(docname)
        #     if strDocname in self.execution_vars['dependency_lists'].keys():
        #         self.execution_vars['delayed_notebooks'].update({strDocname: nb})
        #     else:        
        #         self._execute_notebook_class.execute_notebook(self, nb, docname, self.execution_vars, self.execution_vars['futures'])
        # else:
        #     #do not execute
        #     if (self.config['jupyter_generate_html']):
        #         language_info = nb.metadata.kernelspec.language
        #         self._convert_class = convertToHtmlWriter(self)
        #         self._convert_class.convert(nb, docname, language_info, self.outdir)

        ### mkdir if the directory does not exist
        nb = self.combine_executed_files(nb, docname)
        # import pdb;
        # pdb.set_trace()
        outfilename = os.path.join(self.outdir, os_path(docname) + self.out_suffix)
        ensuredir(os.path.dirname(outfilename))
        print(outfilename, "outfilename")
        try:
            with open(outfilename, "wt", encoding="UTF-8") as f:
                nbformat.write(nb, f)
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

    def normalize_cell(self, cell):
        cell.source = cell.source.strip().replace('\n','')
        return cell
        
    def create_hashcode(self, cell):
        hashcode = md5(cell.source.encode()).hexdigest()
        return hashcode

    def finish(self):

        self.finish_tasks.add_task(self.copy_static_files)
        
        # if self.config["jupyter_execute_notebooks"]:
        #     self.save_executed_and_generate_coverage(self.execution_vars,'website', self.config['jupyter_make_coverage'])

        # if self.config["jupyter_download_nb_execute"]:
        #     self.save_executed_and_generate_coverage(self.download_execution_vars, 'downloads')

        # if "jupyter_make_site" in self.config and self.config['jupyter_make_site']:
        #     self._make_site_class.build_website(self)

    def combine_executed_files(self, nb, docname):
        codetreeFile = self.executedir + "/" + docname + ".codetree"
        execution_count = 0
        count = 0
        if os.path.exists(codetreeFile):
            with open(codetreeFile, "r", encoding="UTF-8") as f:
                json_obj = json.load(f)

            for cell in nb.cells:
                if cell['cell_type'] == "code":
                    execution_count += 1
                    cell = self.normalize_cell(cell)
                    hashcode = self.create_hashcode(cell)
                    output = json_obj[hashcode]['outputs']
                    cell['execution_count'] = execution_count
                    cell['outputs'] = munchify(output)
                    if cell['metadata']['hide-output']:
                        cell['outputs'] = []

        return nb