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
from .utils import copy_dependencies, create_hashcode, normalize_cell
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
            
    def write_doc(self, docname, doctree):
        # work around multiple string % tuple issues in docutils;
        # replace tuples in attribute values with lists
        doctree = doctree.deepcopy()
        destination = docutils.io.StringOutput(encoding="utf-8")

        self.writer.write(doctree, destination)

        # get a NotebookNode object from a string
        nb = nbformat.reads(self.writer.output, as_version=4)
        nb = self.update_Metadata(nb)

        ### mkdir if the directory does not exist
        nb = self.combine_executed_files(nb, docname)

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

    def finish(self):
        self.finish_tasks.add_task(self.copy_static_files)

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
                    cell = normalize_cell(cell)
                    hashcode = create_hashcode(cell)
                    output = json_obj[hashcode]['outputs']
                    cell['execution_count'] = execution_count
                    cell['outputs'] = munchify(output)
                    if cell['metadata']['hide-output']:
                        cell['outputs'] = []

        return nb