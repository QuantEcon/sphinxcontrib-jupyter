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
from .process_latex import main as latexProcessing 

class MakePdfWriter():
    """
    Makes pdf for each notebook
    """
    logger = logging.getLogger(__name__)
    def __init__(self, builderSelf):
        self.pdfdir = builderSelf.outdir + "/pdf" #pdf directory 
        self.texdir = builderSelf.outdir + "/executed" #latex directory 

        for path in [self.pdfdir, self.texdir]:
            ensuredir(path)

        self.pdf_exporter = PDFExporter()
        self.tex_exporter = LatexExporter()
    
    def movePdf(self, builderSelf):
        dirLists = []
        movefiles = True
        for root, dirs, files in os.walk(self.texdir, topdown=True):
            if movefiles:
                for f in files:
                    if ".pdf" in f:
                        source = root + "/" + f
                        self.checkAndRemoveDestFile(self.pdfdir, f)
                        shutil.move(source, self.pdfdir)
                movefiles = False
            for name in dirs:
                presentdir = os.path.join(root, name)
                source = root + "/" + name
                subdirectory = source.replace(self.texdir, "")
                destination = self.pdfdir + subdirectory
                pdfs = glob.glob(presentdir + "/*.pdf", recursive=True)
                if subdirectory in dirLists:
                    continue
                if len(pdfs):
                    ensuredir(destination)
                    dirLists.append(subdirectory)
                else:
                    continue
                for pdf in pdfs:
                    filename = pdf.split('/')[-1]
                    self.checkAndRemoveDestFile(destination, filename)
                    shutil.move(pdf, destination)

    def checkAndRemoveDestFile(self, destination, filename):
        print(filename, "filename")
        destinationFile = destination + "/"  + filename
        if os.path.exists(destinationFile):
            os.remove(destinationFile)

    def convertToLatex(self, builderSelf, filename, latex_metadata):
        """
        function to convert notebooks to latex
        """
        relative_path = ''
        tex_data = ''
        tex_build_path = self.texdir + relative_path
        pdf_build_path = self.pdfdir + relative_path
        templateFolder = builderSelf.config['jupyter_template_path']

        ensuredir(tex_build_path)
        ensuredir(pdf_build_path)

        ## setting the working directory
        os.chdir(self.texdir)

        ## copies all theme folder images to static folder
        if os.path.exists(builderSelf.confdir + "/theme/static/img"):
            copy_tree(builderSelf.confdir + "/theme/static/img", self.texdir + "/_static/img/", preserve_symlinks=1)
        else:
            self.logger.warning("Image folder not present inside the theme folder")

        fl_ipynb = self.texdir + "/" + "{}.ipynb".format(filename)
        fl_tex = self.texdir + "/" + "{}.tex".format(filename)
        fl_tex_template = builderSelf.confdir + "/" + templateFolder + "/" + builderSelf.config['jupyter_latex_template']

        ## do not convert excluded patterns to latex
        excludedFileArr = [x in filename for x in builderSelf.config['jupyter_pdf_excludepatterns']]
        if not True in excludedFileArr:  
            ## --output-dir - forms a directory in the same path as fl_ipynb - need a way to specify properly?
            ### converting to pdf using xelatex subprocess
            subprocess.run(["jupyter", "nbconvert","--to","latex","--template",fl_tex_template,"from", fl_ipynb])
            latexProcessing(self, fl_tex)

            ### check if subdirectory
            subdirectory = ""
            index = filename.rfind('/')
            if index > 0:
                subdirectory = filename[0:index]
                filename = filename[index + 1:]

            ### set working directory for xelatex processing
            os.chdir(self.texdir + "/" + subdirectory)

            try:
                self.subprocessXelatex(fl_tex, filename)
                if 'bib_include' in latex_metadata:
                    self.subprocessBibtex(filename)
                self.subprocessXelatex(fl_tex, filename)
                self.subprocessXelatex(fl_tex, filename)
            except OSError as e:
                print(e)
            except AssertionError as e:
                pass
                # exit() - to be used when we want the execution to stop on error

    def subprocessXelatex(self, fl_tex, filename):
        p = subprocess.Popen(("xelatex", "-interaction=nonstopmode", fl_tex), stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        output, error = p.communicate()
        if (p.returncode != 0):
            self.logger.warning('xelatex exited with returncode {} , encounterd in {} with error -- {}'.format(p.returncode , filename, error))

        # assert (p.returncode == 0), self.logger.warning('xelatex exited with returncode {} , encounterd in {} with error -- {}'.format(p.returncode , filename, error)) ---- assert statement stops the program, will handle it later

    def subprocessBibtex(self, filename):
        p = subprocess.Popen(('bibtex',filename), stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        output, error = p.communicate()
        if (p.returncode != 0):
            self.logger.warning('bibtex exited with returncode {} , encounterd in {} with error -- {} {}'.format(p.returncode , filename, output, error))
        
        # assert (p.returncode == 0), self.logger.warning('bibtex exited with returncode {} , encounterd in {} with error -- {} {}'.format(p.returncode , filename, output, error)) ---- assert statement stops the program, will handle it later
