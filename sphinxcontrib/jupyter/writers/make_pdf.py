import nbformat
from nbconvert import PDFExporter
from nbconvert import LatexExporter
import os
import sys
from io import open
import subprocess
from sphinx.util.osutil import ensuredir
from sphinx.util import logging
from nbconvert.preprocessors import LatexPreprocessor

class MakePdfWriter():
    """
    Makes pdf for each notebook
    """
    logger = logging.getLogger(__name__)
    def __init__(self, builderSelf):
        self.pdfdir = builderSelf.outdir + "/pdf" #pdf directory 
        self.texdir = builderSelf.outdir + "/executed" #latex directory 

        ## setting the working directory
        os.chdir(builderSelf.outdir)

        for path in [self.pdfdir, self.texdir]:
            ensuredir(path)

        self.pdf_exporter = PDFExporter()
        self.tex_exporter = LatexExporter()

    def convertToLatex(self, builderSelf, filename):
        """
        function to convert notebooks to latex
        """
        relative_path = ''
        tex_data = ''
        tex_build_path = self.texdir + relative_path
        pdf_build_path = self.pdfdir + relative_path

        ensuredir(tex_build_path)
        ensuredir(pdf_build_path)

        ## setting the working directory
        os.chdir(self.texdir)

        # fl_pdf = pdf_build_path + "/" + "{}.pdf".format(filename)
        
        # print(builderSelf.executed_notebook_dir, "executed_notebook_dir")
        # import pdb
        # pdb.set_trace()
        fl_ipynb = builderSelf.executed_notebook_dir + "/" + "{}.ipynb".format(filename)
        fl_tex = builderSelf.executed_notebook_dir + "/" + "{}.tex".format(filename)

        ## --output-dir - forms a directory in the same path as fl_ipynb - need a way to specify properly?
        ### converting to pdf using xelatex subprocess
        if sys.version_info.major == 2:
            subprocess.call(["jupyter", "nbconvert","--to","latex","from", fl_ipynb])
            subprocess.call(["xelatex","-output-directory",pdf_build_path, fl_tex])
            subprocess.call(["xelatex","-output-directory",pdf_build_path, fl_tex])
        else:
            subprocess.run(["jupyter", "nbconvert","--to","latex","from", fl_ipynb])
            subprocess.run(["xelatex","-output-directory",pdf_build_path, fl_tex])
            subprocess.run(["xelatex","-output-directory",pdf_build_path, fl_tex])
