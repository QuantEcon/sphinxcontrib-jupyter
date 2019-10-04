"""
PDF Converter from IPYNB to TEX to PDF
"""

import nbformat
from nbconvert import PDFExporter
from nbconvert import LatexExporter
import os
import sys
import shutil
import glob
from io import open
import subprocess
from sphinx.util.osutil import ensuredir
from sphinx.util import logging
from nbconvert.preprocessors import LatexPreprocessor
from distutils.dir_util import copy_tree
from .utils import python27_glob

class MakePDFWriter():
    """
    Makes pdf for each notebook
    """
    logger = logging.getLogger(__name__)
    def __init__(self, builder):
        self.pdfdir = builder.outdir + "/pdf" #pdf directory 
        self.texdir = builder.outdir + "/executed" #latex directory 

        for path in [self.pdfdir, self.texdir]:
            ensuredir(path)

        self.pdf_exporter = PDFExporter()
        self.tex_exporter = LatexExporter()
    
    def move_pdf(self, builder):
        dir_lists = []
        move_files = True
        for root, dirs, files in os.walk(self.texdir, topdown=True):
            if move_files:
                for f in files:
                    if ".pdf" in f:
                        source = root + "/" + f
                        self.check_remove_destination_file(self.pdfdir, f)
                        shutil.move(source, self.pdfdir)
                move_files = False
            for name in dirs:
                presentdir = os.path.join(root, name)
                source = root + "/" + name
                subdirectory = source.replace(self.texdir, "")
                destination = self.pdfdir + subdirectory
                if sys.version_info[0] < 3:
                    pdfs = python27_glob(presentdir +"/", "*.pdf")
                else:
                    pdfs = glob.glob(presentdir + "/*.pdf", recursive=True)
                if subdirectory in dir_lists:
                    continue
                if len(pdfs):
                    ensuredir(destination)
                    dir_lists.append(subdirectory)
                else:
                    continue
                for pdf in pdfs:
                    filename = pdf.split('/')[-1]
                    self.check_remove_destination_file(destination, filename)
                    shutil.move(pdf, destination)

    def check_remove_destination_file(self, destination, filename):
        destinationFile = destination + "/"  + filename
        if os.path.exists(destinationFile):
            os.remove(destinationFile)

    def convert_to_latex(self, builder, filename, latex_metadata):
        """
        function to convert notebooks to latex
        """
        relative_path = ''
        tex_data = ''
        tex_build_path = self.texdir + relative_path
        pdf_build_path = self.pdfdir + relative_path
        template_folder = builder.config['jupyter_template_path']

        ensuredir(tex_build_path)
        ensuredir(pdf_build_path)

        ## setting the working directory
        os.chdir(self.texdir)

        ## copies all theme folder images to static folder
        if os.path.exists(builder.confdir + "/theme/static/img"):
            copy_tree(builder.confdir + "/theme/static/img", self.texdir + "/_static/img/", preserve_symlinks=1)
        else:
            self.logger.warning("Image folder not present inside the theme folder")

        fl_ipynb = self.texdir + "/" + "{}.ipynb".format(filename)
        fl_tex = self.texdir + "/" + "{}.tex".format(filename)
        fl_tex_template = builder.confdir + "/" + template_folder + "/" + builder.config['jupyter_latex_template']

        ## do not convert excluded patterns to latex
        excluded_files = [x in filename for x in builder.config['jupyter_pdf_excludepatterns']]
        if not True in excluded_files:  
            ## --output-dir - forms a directory in the same path as fl_ipynb - need a way to specify properly?
            ### converting to pdf using xelatex subprocess
            if sys.version_info[0] < 3:
                subprocess.call(["jupyter", "nbconvert","--to","latex","--template",fl_tex_template,"from", fl_ipynb])
            else:
                subprocess.run(["jupyter", "nbconvert","--to","latex","--template",fl_tex_template,"from", fl_ipynb])

            ### check if subdirectory
            subdirectory = ""
            index = filename.rfind('/')
            if index > 0:
                subdirectory = filename[0:index]
                filename = filename[index + 1:]

            ### set working directory for xelatex processing
            os.chdir(self.texdir + "/" + subdirectory)

            try:
                self.subprocess_xelatex(fl_tex, filename)
                if 'bib_include' in latex_metadata:
                    self.subprocess_bibtex(filename)
                self.subprocess_xelatex(fl_tex, filename)
                self.subprocess_xelatex(fl_tex, filename)
            except OSError as e:
                print(e)
            except AssertionError as e:
                pass
                # exit() - to be used when we want the execution to stop on error

    def subprocess_xelatex(self, fl_tex, filename):
        p = subprocess.Popen(("xelatex", "-interaction=nonstopmode", fl_tex), stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        output, error = p.communicate()
        if (p.returncode != 0):
            self.logger.warning('xelatex exited with returncode {} , encounterd in {} with error -- {}'.format(p.returncode , filename, error))

        # assert (p.returncode == 0), self.logger.warning('xelatex exited with returncode {} , encounterd in {} with error -- {}'.format(p.returncode , filename, error)) ---- assert statement stops the program, will handle it later

    def subprocess_bibtex(self, filename):
        p = subprocess.Popen(('bibtex',filename), stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        output, error = p.communicate()
        if (p.returncode != 0):
            self.logger.warning('bibtex exited with returncode {} , encounterd in {} with error -- {} {}'.format(p.returncode , filename, output, error))
        
        # assert (p.returncode == 0), self.logger.warning('bibtex exited with returncode {} , encounterd in {} with error -- {} {}'.format(p.returncode , filename, output, error)) ---- assert statement stops the program, will handle it later
