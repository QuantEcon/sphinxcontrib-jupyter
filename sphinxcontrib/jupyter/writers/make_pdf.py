import nbformat
from nbconvert import PDFExporter
from nbconvert import LatexExporter
import os
import sys
from io import open
import subprocess
from sphinx.util.osutil import ensuredir
from sphinx.util import logging

class MakePdfWriter():
    """
    Makes pdf for each notebook
    """
    logger = logging.getLogger(__name__)
    def __init__(self, builderSelf):
        self.pdfdir = builderSelf.outdir + "/pdf" #pdf directory 
        self.texdir = builderSelf.outdir #latex directory 

        ## setting the working directory
        os.chdir(builderSelf.outdir)

        for path in [self.pdfdir, self.texdir]:
            ensuredir(path)

        self.pdf_exporter = PDFExporter()
        self.tex_exporter = LatexExporter()

    def convertToLatex(self, nb, filename):
        """
        function to convert notebooks to latex
        """
        relative_path = ''
        tex_data = ''
        tex_build_path = self.texdir + relative_path
        pdf_build_path = self.pdfdir + relative_path

        ensuredir(tex_build_path)
        ensuredir(pdf_build_path)

        fl_tex = tex_build_path + "/" + "{}.tex".format(filename)
        fl_pdf = pdf_build_path + "/" + "{}.pdf".format(filename)

        with open(fl_tex, "w") as f:
            tex_data, resources = self.tex_exporter.from_notebook_node(nb)
            f.write(tex_data)
            ### need to output resources here ---- 
            f.close()
        
        ### converting to pdf using xelatex subprocess
        if sys.version_info.major == 2:
            subprocess.call(["xelatex","-output-directory",pdf_build_path, fl_tex])
        else:
            subprocess.run(["xelatex","-output-directory",pdf_build_path, fl_tex])
