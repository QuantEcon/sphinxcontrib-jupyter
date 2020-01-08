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
    Builds Jupyter Notebook ready for pdf (FOR TESTING PURPOSES ONLY) 
    """
    name = "jupyterpdf"
    # name = "jupyter"
    format = "ipynb"            #TODO: best not to override format
    out_suffix = ".ipynb"
    allow_parallel = True

    _writer_class = JupyterWriter
    logger = logging.getLogger(__name__)    #TODO: Should we use Sphinx LOGGING

    def init(self):
        pass

    #TODO: Is this different to what is in Builder?
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
        #self.config["jupyter_conversion_mode"] = "code"
        self.writer = self._writer_class(self)

        ## copies the dependencies to the notebook folder
        #copy_dependencies(self)
            
    def write_doc(self, docname, doctree):
        doctree = doctree.deepcopy()
        destination = docutils.io.StringOutput(encoding="utf-8")
        self.writer.write(doctree, destination)

        # get a NotebookNode object from a string
        nb = nbformat.reads(self.writer.output, as_version=4)

        outfilename = os.path.join(self.outdir, os_path(docname) + self.out_suffix)
        ensuredir(os.path.dirname(outfilename))

        try:
            with open(outfilename, "wt", encoding="UTF-8") as f:
                nbformat.write(nb, f)
        except (IOError, OSError) as err:
            self.logger.warning("error writing file %s: %s" % (outfilename, err))
    
    def finish(self):
        pass

