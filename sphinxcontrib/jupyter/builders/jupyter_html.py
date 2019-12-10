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
from .utils import copy_dependencies, combine_executed_files, check_codetree_validity, run_build
from ..writers.utils import get_subdirectory_and_filename
from hashlib import md5

logger = logging.getLogger(__name__)

class JupyterHtmlBuilder(Builder):
    """
    Builds html notebooks
    """
    name="jupyterhtml"
    format = "ipynb"
    out_suffix = ".ipynb"

    allow_parallel = True
    _writer_class = JupyterWriter
    def init(self):
        ### initializing required classes
        self.executedir = self.confdir + '/_build/codetree'
        self.downloadsdir = self.outdir + "/_downloads"
        self.downloadsExecutedir = self.downloadsdir + "/executed"
        self._convert_class = convertToHtmlWriter(self)
        self._make_site_class = MakeSiteWriter(self)

    def get_target_uri(self, docname: str, typ: str = None):
        return docname

    def get_outdated_docs(self):
        return self.env.found_docs

    def prepare_writing(self, docnames):
        self.writer = self._writer_class(self)

        # if (self.config["jupyter_download_nb_execute"]):
        #     copy_dependencies(self, self.downloadsExecutedir)
    
    def write_doc(self, docname, doctree):
        # work around multiple string % tuple issues in docutils;
        # replace tuples in attribute values with lists
        doctree = doctree.deepcopy()
        destination = docutils.io.StringOutput(encoding="utf-8")
        
        ### processing for downloaded notebooks
        if "jupyter_download_nb" in self.config and self.config["jupyter_download_nb"]:
            nb, outfilename = self.process_doctree_to_notebook(doctree, destination, docname, True)
            nb = self.add_download_metadata(nb) ## add metadata for the downloaded notebooks

        self.save_notebook(outfilename, nb)

        ### processing for html notebooks
        nb, outfilename = self.process_doctree_to_notebook(doctree, destination, docname)
        #self.save_notebook(outfilename, nb)

        ### converting to HTML
        language_info = nb.metadata.kernelspec.language
        self._convert_class.convert(nb, docname, language_info, nb['metadata']['path'])

    def process_doctree_to_notebook(self, doctree, destination, docname, download_nb=False):
        ref_urlpath = None
        jupyter_download_nb_image_urlpath = None
        outdir = self.outdir

        ### check for codetree else, create it
        update = check_codetree_validity(self, nb, docname)

        if update:
            run_build('execute')

        if download_nb:
            ref_urlpath = self.config["jupyter_download_nb_urlpath"]
            jupyter_download_nb_image_urlpath = self.config["jupyter_download_nb_image_urlpath"]
            outdir = self.downloadsdir

        self.writer._set_ref_urlpath(ref_urlpath)
        self.writer._set_jupyter_download_nb_image_urlpath(jupyter_download_nb_image_urlpath)
        
        ## combine the executed code with output of this builder
        self.writer.write(doctree, destination)

        nb = nbformat.reads(self.writer.output, as_version=4)

        ## adding the site metadata here
        nb = self.add_site_metadata(nb, docname)
        
        nb = combine_executed_files(self.executedir, nb, docname)

        outfilename = os.path.join(outdir, os_path(docname) + self.out_suffix)
        ensuredir(os.path.dirname(outfilename))

        return nb, outfilename

    def save_notebook(self, outfilename, nb):
        try:
            with codecs.open(outfilename, "w", "utf-8") as f:
                self.writer.output = nbformat.writes(nb, version=4)
                f.write(self.writer.output)
        except (IOError, OSError) as err:
            self.logger.warning("error writing file %s: %s" % (outfilename, err))

    def copy_static_files(self):
        # copy all static files
        logger.info(bold("copying static files... "), nonl=True)
        ensuredir(os.path.join(self.outdir, '_static'))


        # excluded = Matcher(self.config.exclude_patterns + ["**/.*"])
        for static_path in self.config["jupyter_static_file_path"]:
            entry = os.path.join(self.confdir, static_path)
            if not os.path.exists(entry):
                logger.warning(
                    "jupyter_static_path entry {} does not exist"
                    .format(entry))
            else:
                copy_asset(entry, os.path.join(self.outdir, "_static"))
        logger.info("done")

    def add_site_metadata(self, nb, docname):
        subdirectory, filename = get_subdirectory_and_filename(docname)
        nb['metadata']['path'] = subdirectory
        nb['metadata']['filename'] = filename
        nb['metadata']['filename_with_path'] = docname
        return nb

    def add_download_metadata(self, nb):
        nb['metadata']['download_nb'] = self.config['jupyter_download_nb']
        nb['metadata']['download_nb_path'] = self.config['jupyter_download_nb_urlpath']
        return nb

    def finish(self):
        self.finish_tasks.add_task(self.copy_static_files)

        if "jupyter_make_site" in self.config and self.config['jupyter_make_site']:
            self._make_site_class.build_website(self)
