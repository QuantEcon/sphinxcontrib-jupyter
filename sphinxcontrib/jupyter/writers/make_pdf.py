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

        ## copies all theme folder images to static folder
        if os.path.exists(builderSelf.confdir + "/theme/static/img"):
            copy_tree(builderSelf.confdir + "/theme/static/img", builderSelf.executed_notebook_dir + "/_static/img/", preserve_symlinks=1)
        else:
            self.logger.warning("Theme folder not present. Consider creating a theme folder for static assets")

        fl_ipynb = builderSelf.executed_notebook_dir + "/" + "{}.ipynb".format(filename)
        fl_tex = builderSelf.executed_notebook_dir + "/" + "{}.tex".format(filename)

        fl_tex_template = builderSelf.confdir + "/" + builderSelf.config['jupyter_latex_template']

        ## do not convert index and zreferences to latex
        if filename.find('index') == -1 or filename.find('zreferences') == -1:  
            ## --output-dir - forms a directory in the same path as fl_ipynb - need a way to specify properly?
            ### converting to pdf using xelatex subprocess
            subprocess.run(["jupyter", "nbconvert","--to","latex","--template",fl_tex_template,"from", fl_ipynb])
            latexProcessing(self, fl_tex)
            #p = None
            #try:
            #p = subprocess.Popen(('xelatex',"-interaction=nonstopmode","-output-directory",pdf_build_path, fl_tex),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            #subprocess.run(["xelatex","-interaction=nonstopmode","-output-directory",pdf_build_path, fl_tex])
            #p.communicate()
            #print(p.stdout)
            #     assert (p.returncode == 0), 'xelatex exited with %d' % p.returncode
            # except OSError as e:
            #     print("or here ?")
            #     print >> sys.stderr, 'Failed to run pygmentize: %s' % str(e)
            # except AssertionError as e:
            #     print("here?")
            #     print(p.stdout)
            #     print(e)
            #     exit()
            subprocess.run(["xelatex","-interaction=nonstopmode","-output-directory",pdf_build_path, fl_tex])
            subprocess.run(["bibtex", ])
            subprocess.run(["xelatex","-interaction=nonstopmode","-output-directory",pdf_build_path, fl_tex])
            subprocess.run(["bibtex"])
