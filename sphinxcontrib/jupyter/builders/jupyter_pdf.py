import codecs
import os.path
import docutils.io

import nbformat
import json
from sphinx.util.osutil import ensuredir, os_path
from ..writers.jupyter import JupyterWriter
from sphinx.builders import Builder
from sphinx.util.console import bold
from sphinx.util.fileutil import copy_asset
from ..writers.make_pdf import MakePDFWriter
from sphinx.util import logging
import shutil
from distutils.spawn import find_executable
import time
from .utils import combine_executed_files, check_codetree_validity, run_build
from ..writers.utils import get_subdirectory_and_filename

logger = logging.getLogger(__name__)

class JupyterPDFBuilder(Builder):

    name="jupyterpdf"
    docformat = "ipynb"
    out_suffix = ".pdf"
    allow_parallel = True
    _writer_class = JupyterWriter

    def init(self):
        """
        Builds IPYNB(PDF) notebooks
        """
        self.executedir = self.confdir + '/_build/execute'
        self.texdir = self.outdir + "/latex"
        self.texbookdir = self.outdir + "/texbook"
        self.pdfdir = self.outdir + "/pdf"

        for path in [self.pdfdir, self.texdir]:
            ensuredir(path)

        if not find_executable('xelatex'):
            logger.warning(
                "Cannot find xelatex executable for pdf compilation"
            )
            exit(1)

        # TODO: We should write a separate function/class to check configs
        if  self.config["jupyter_pdf_book"] and ("jupyter_pdf_book_index" not in self.config or not self.config["jupyter_pdf_book_index"]):
            logger.warning(
                "You have switched on the book conversion option but not specified an index/contents file for book pdf"
            )
            exit(1)
        
        #PDF Writer Object
        self.pdf = MakePDFWriter(self)

    def get_outdated_docs(self):
        for docname in self.env.found_docs:
            if docname in self.config['jupyter_pdf_excludepatterns']:
                continue
            if docname not in self.env.all_docs:
                yield docname
                continue
            targetname = self.env.doc2path(docname, self.outdir + "/pdf",
                                           self.out_suffix)
            try:
                targetmtime = os.path.getmtime(targetname)
            except OSError:
                targetmtime = 0
            try:
                srcmtime = os.path.getmtime(self.env.doc2path(docname))
                # checks if the source file edited time is later then the html build time
                if srcmtime > targetmtime:
                    yield docname
            except EnvironmentError:
                pass

    def get_target_uri(self, docname, typ=None):
        return docname

    def prepare_writing(self, docnames):
        self.writer = self._writer_class(self)

        self.copy_static_files()

    def write_doc(self, docname, doctree):
        # work around multiple string % tuple issues in docutils;
        # replace tuples in attribute values with lists
        doctree = doctree.deepcopy()
        destination = docutils.io.StringOutput(encoding="utf-8")

        ### output notebooks for executing for single pdfs, the urlpath should be set to website url
        self.writer._set_ref_urlpath(self.config["jupyter_pdf_urlpath"])
        self.writer._set_jupyter_download_nb_image_urlpath(None)
        self.writer.write(doctree, destination)

        ## get a NotebookNode object from a string
        nb = nbformat.reads(self.writer.output, as_version=4)

        os.chdir(self.confdir)
        if self.config["jupyter_execute"]:
            ### check for codetree else, create it
            update = check_codetree_validity(self, nb, docname)
            
            if update:
                run_build('execute')

            ## combine the executed code with output of this builder
            nb = combine_executed_files(self.executedir, nb, docname)

        ## adding latex metadata
        nb = self.add_latex_metadata(nb, docname)

        ### mkdir if the directory does not exist
        outfilename = os.path.join(self.texdir, os_path(docname) + ".ipynb")
        ensuredir(os.path.dirname(outfilename))

        try:
            with codecs.open(outfilename, "w", "utf-8") as f:
                self.writer.output = nbformat.writes(nb, version=4)
                f.write(self.writer.output)
        except (IOError, OSError) as err:
            logger.warning("error writing file %s: %s" % (outfilename, err))

        self.pdf.convert_to_latex(self, docname, nb['metadata']['latex_metadata'])
        self.pdf.move_pdf(self)

    def copy_static_files(self):
        # copy all static files
        logger.info(bold("copying static files... "), nonl=True)
        ensuredir(os.path.join(self.texdir, '_static'))


        # excluded = Matcher(self.config.exclude_patterns + ["**/.*"])
        for static_path in self.config["jupyter_static_file_path"]:
            entry = os.path.join(self.confdir, static_path)
            if not os.path.exists(entry):
                logger.warning(
                    "jupyter_static_path entry {} does not exist"
                    .format(entry))
            else:
                copy_asset(entry, os.path.join(self.texdir, "_static"))
        self.copy_static_folder_to_subfolders(self.texdir, True)

    # Copying static folder to subfolders - TODO: will remove this later
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

    def finish(self):
        #self.finish_tasks.add_task(self.copy_static_files)

        ### making book pdf
        if self.config["jupyter_pdf_book"]:
            self.pdf.process_tex_for_book(self)

    def add_latex_metadata(self, nb, docname=""):
        ## initialize latex metadata
        if 'latex_metadata' not in nb['metadata']:
            nb['metadata']['latex_metadata'] = {}

        ## check for relative paths
        subdirectory, filename = get_subdirectory_and_filename(docname)

        path = ''
        if subdirectory != '':
            path = "../"
            slashes = subdirectory.count('/')
            for i in range(slashes):
                path += "../"

        ## add check for logo here as well
        if nb.metadata.title:
            nb.metadata.latex_metadata.title = nb.metadata.title
        if "jupyter_pdf_logo" in self.config and self.config['jupyter_pdf_logo']:
            nb.metadata.latex_metadata.logo = path + self.config['jupyter_pdf_logo']
        
        if self.config["jupyter_bib_file"]:
            nb.metadata.latex_metadata.bib = path + self.config["jupyter_bib_file"]

        if self.config["jupyter_pdf_author"]:
            nb.metadata.latex_metadata.author = self.config["jupyter_pdf_author"]
        
        if self.config["jupyter_pdf_book_index"] is not None and (filename and self.config["jupyter_pdf_book_index"] in filename):
            nb.metadata.latex_metadata.jupyter_pdf_book_title = self.config["jupyter_pdf_book_title"]

        return nb 