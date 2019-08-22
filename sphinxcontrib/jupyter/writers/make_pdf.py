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
            subprocess.run(["xelatex","-output-directory",pdf_build_path, fl_tex])
            subprocess.run(["xelatex","-output-directory",pdf_build_path, fl_tex])

    def add_labels():
        f = open(file1, "r", encoding="utf8")
        rstList = []
        for line in f:
            rstList.append(line)
        f.close()

        g=[]
        g.append('s')
        # appended this 's' so that actual label list can be at 1st position and not 0
        for i in range(0,len(rstList)):
            a = rstList[i].split()
            if(len(a)!=0 and a[0]==":label:"):
                a[1] = a[1].lower()
                srr=""
                for x in range(0,len(a[1])):
                    if(a[1][x] == "_" or a[1][x] == ":" or a[1][x] == ";" or a[1][x]=="\\"):
                        srr+= "-"
                    else:
                        srr+=a[1][x]
                g.append(srr)

        latest_list = make_texList(file2)

        f = open(file2, "w", encoding="utf8")
        for i in range(0,len(latest_list)):
            a = latest_list[i].split()
            if(len(a)!=0 and "\\tag" in a[-1]):
                z = int(re.findall(r'[0-9]+', a[-1])[0])
                f.write(latest_list[i][:-1]+"\label{eq:"+g[z]+"}\n")
            else:
                f.write(latest_list[i])

        f.close()

