import nbformat
from nbconvert import PDFExporter
from nbconvert import LatexExporter
import os
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
        self.pdfdir = builderSelf.outdir + "/pdf" #html directory 
        self.texdir = builderSelf.outdir + "/tex" #html directory 

        for path in [self.pdfdir, self.texdir]:
            ensuredir(path)

        self.pdf_exporter = PDFExporter()
        self.tex_exporter = LatexExporter()

    def convertToLatex(self, nb, filename):
        relative_path = ''
        tex_data = ''
        tex_build_path = self.texdir + relative_path
        pdf_build_path = self.pdfdir + relative_path

        ensuredir(tex_build_path)
        ensuredir(pdf_build_path)

        fl_tex = tex_build_path + "/" + "{}.tex".format(filename)
        fl_pdf = pdf_build_path + "/" + "{}.pdf".format(filename)

        print(nb, "notebook")
        print(fl_tex, "fl tex")
        with open(fl_tex, "w") as f:
            tex_data, resources = self.tex_exporter.from_notebook_node(nb)
            f.write(tex_data)
            f.close()
        
        subprocess.run(["xelatex","--shell-escape",fl_tex, "-output-directory",pdf_build_path])
        

    def convertToPdf(self, nb, filename):
        relative_path = ''
        build_path = self.pdfdir +  relative_path
        ensuredir(build_path)
        fl_pdf = build_path + "/" + "{}.pdf".format(filename)
        
        print(nb, "notebook")
        print(fl_pdf, "fl pdf")
        with open(fl_pdf, "wb") as f:
            pdf_data, resources = self.pdf_exporter.from_notebook_node(nb)
            f.write(pdf_data)
            f.close()

