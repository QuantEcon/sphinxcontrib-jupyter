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
from .utils import get_list_of_files, get_subdirectory_and_filename

class MakePDFWriter():
    """
    Makes pdf for each notebook
    """
    logger = logging.getLogger(__name__)
    def __init__(self, builder):
        self.pdf_exporter = PDFExporter()
        self.tex_exporter = LatexExporter()
        self.index_book = builder.config['jupyter_pdf_book_index']
    
    def move_pdf(self, builder):
        dir_lists = []
        move_files = True
        for root, dirs, files in os.walk(builder.texdir, topdown=True):
            if move_files:
                for f in files:
                    if ".pdf" in f:
                        source = root + "/" + f
                        self.check_remove_destination_file(builder.pdfdir, f)
                        shutil.move(source, builder.pdfdir)
                move_files = False
            for name in dirs:
                presentdir = os.path.join(root, name)
                source = root + "/" + name
                subdirectory = source.replace(builder.texdir, "")
                destination = builder.pdfdir + subdirectory
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
        tex_build_path = builder.texdir + relative_path
        pdf_build_path = builder.pdfdir + relative_path


        ensuredir(tex_build_path)
        ensuredir(pdf_build_path)

        ## setting the working directory
        os.chdir(builder.texdir)

        ## copies all theme folder images to static folder
        if os.path.exists(builder.confdir + "/theme/static/img"):
            copy_tree(builder.confdir + "/theme/static/img", builder.texdir + "/_static/img/", preserve_symlinks=1)
        else:
            self.logger.warning("Image folder not present inside the theme folder")

        fl_ipynb = builder.texdir + "/" + "{}.ipynb".format(filename)
        fl_tex = builder.texdir + "/" + "{}.tex".format(filename)
        fl_tex_template = builder.confdir + "/" + builder.config['jupyter_template_latex']

        ## do not convert excluded patterns to latex
        excluded_files = [x in filename for x in builder.config['jupyter_pdf_excludepatterns']]

        if not True in excluded_files:    
            ## --output-dir - forms a directory in the same path as fl_ipynb - need a way to specify properly?
            ### converting to pdf using xelatex subprocess
            subprocess.run(["jupyter", "nbconvert","--to","latex","--template",fl_tex_template,"from", fl_ipynb])

            ### check if subdirectory
            subdirectory, filename = get_subdirectory_and_filename(filename)

            ### set working directory for xelatex processing
            os.chdir(builder.texdir + "/" + subdirectory)

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
        p = subprocess.Popen(("xelatex", "-interaction=nonstopmode","-jobname=" + filename, fl_tex), stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
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


    #### functions relevant to book pdf ####

    def nbconvert_index(self, builder):
        ## converts index ipynb file of book to tex with the help of the specified template
        fl_ipynb = builder.texbookdir + "/" + self.index_book + ".ipynb"
        fl_tex_template = builder.confdir + "/" + builder.config['jupyter_template_latexbook']

        subprocess.run(["jupyter", "nbconvert","--to","latex","--template",fl_tex_template,"from", fl_ipynb])

    def create_pdf_from_latex(self, fl_tex, filename):
        ## parses the latex file to create pdf
        try:
            self.subprocess_xelatex(fl_tex, filename)
            self.subprocess_bibtex(filename)
            self.subprocess_xelatex(fl_tex, filename)
            self.subprocess_xelatex(fl_tex, filename)
        except OSError as e:
            print(e)
        except AssertionError as e:
            pass

    def delete_lines(self,f):
        ## deletes all the lines except between the given comments
        edited = []
        add = False
        for line in f.readlines():
            if "% delete-from-here-book %" in line:
                add = False
            if add:
                edited.append(line)
            if "% delete-till-here-book %" in line:
                add = True
        return ''.join(edited)

    def alter(self, line, filename, char):
        ## alters the character to have a -{filename} attached to it 
        if char in line:
            indexchar = line.find(char)
            subline= line[indexchar:]
            indexa = subline.find('{')
            indexb = subline.find('}')
            srr = subline[indexa+1:indexb]
            srr2 = srr + "-" + filename
            line = line.replace(char + srr, char + srr2)
        return line

    def append_subdirectory_to_images_path(self, fullpath, line):
        ### function to add subdirectory to individual tex image files - for julia lectures - should be made more robust
        subdirectory = None
        srr = ''
        srr2 = ''
        imagepathstart = line.rfind("{")
        imagepathend = line.rfind("}")

        patha = fullpath.rfind("/")
        pathb = fullpath[0:patha].rfind("/")
        folder_name = fullpath[0:patha]
        if pathb > 1:
            subdirectory = fullpath[pathb + 1:patha]
        if subdirectory and "texbook" not in subdirectory:
            srr = line[imagepathstart+1:imagepathend]
            srr2 = subdirectory + "/" + srr
        line = line.replace(srr, srr2)
        return line


    def make_changes_tex(self, data, fullpath):
        ## function to do preprocessing to make all section ids and labels unique
        arraylist = data.split('\n')
        alteredarr = []
        image_exts = ['.jpg', '.png', '.jpeg']

        ## removes extension and path from fullpath
        if "." in fullpath or "/" in fullpath:
            index = fullpath.rfind('/')
            index1 = fullpath.rfind('.')
            filename = fullpath[index + 1:index1]

        ## appends filename at the end of ids to make it unique
        for index, line in enumerate(arraylist):
            for ext in image_exts:
                if ext in arraylist[index] and '_static' not in arraylist[index] and 'http' not in arraylist[index] and '_files' in arraylist[index]:
                    line = self.append_subdirectory_to_images_path(fullpath, line)
            if '\section{' in line or '\section{' in arraylist[index - 1]:
                line = self.alter(line, filename, '\\label{')
            line = self.alter(line, filename, "\\hypertarget{")
            line = self.alter(line, filename, '\\ref{')
            alteredarr.append(line)
        return '\n'.join(alteredarr) 

    def copy_tex_for_book(self, builder):
        ## make a separate directory for tex files relevant to book
        if os.path.exists(builder.texbookdir):
            shutil.rmtree(builder.texbookdir)

        shutil.copytree(builder.texdir, builder.texbookdir)

    def process_tex_for_book(self, builder):
        ## does all the preprocessing of latex files before calling them from the index file
        ## of the book and converting them to pdf.
        ## converts the index ipynb of the book and converts it to pdf via latex
        self.copy_tex_for_book(builder)

        files = get_list_of_files(builder.texbookdir)
        for filename in files:
            if ".tex" in filename:
                with open(filename, 'r', encoding="utf8") as f:
                    data = f.read()
                    f.seek(0)
                    data = self.delete_lines(f)
                    data = self.make_changes_tex(data, filename)
                    output = open(filename, 'w', encoding="utf8")
                    output.write(data)
                    f.close()
                    output.close()
                    
        os.chdir(builder.texbookdir)
        self.nbconvert_index(builder)
        fl_tex = builder.texbookdir + "/" + self.index_book + ".tex"
        filename = self.index_book

        ## checking if an explicit output filename is specified in the config file
        if "jupyter_pdf_book_name" in builder.config and builder.config["jupyter_pdf_book_name"]:
            filename = builder.config["jupyter_pdf_book_name"]
        self.create_pdf_from_latex(fl_tex, filename)