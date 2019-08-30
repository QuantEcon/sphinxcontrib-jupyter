import os
import sys
import glob
from io import open
import subprocess
from sphinx.util.osutil import ensuredir
from sphinx.util import logging
import re

def make_texList(f):
    texList = []
    for line in f:
        texList.append(line)
    return texList

def func_replace(f, data, filename):
    #convert to string:
    f.seek(0)
    data = data.replace("\\paragraph", "\\textbf")
    data = data.replace("\\maketitle", "\\maketitle"+"\n"+"    \\parskip 0.090in")

    data = data.replace("\\hypertarget{qe-notebook-header}{}"+"\n"+"\\begin{verbatim}"+"\n"+"    <a href=\"https://quantecon.org/\" title=\"quantecon.org\">"+"\n"+"            <img style=\"width:250px;display:inline;\" width=\"250px\" src=\"https://assets.quantecon.org/img/qe-menubar-logo.svg\" alt=\"QuantEcon\">"+"\n"+"    </a>"+"\n"+"\\end{verbatim}", "")

    data = data.replace("\\href{http","\\abchref{http")

    data = data.replace("\\href{","\\href{https://lectures.quantecon.org/py/")

    data = data.replace(".ipynb}{", ".html}{")

    data = data.replace("\\abchref","\\href")

    data = data.replace("\\begin{Verbatim}[", "\\begin{Verbatim}[fontsize=\\scriptsize,")

    data = data.replace("0in", "0in"+"\n"+"\n"+"vbnmc")

    data = data.replace("\\hypertarget{contents}{%", "jhgbnm"+"\n"+"\\hypertarget{contents}{%")

    data = data.replace("\\label{contents}}", "\\label{contents}}"+"\n"+"vbnmc")

    data = data.replace("}"+"\n"+"\n"+"  \\begin{itemize}"+"\n"+"  \\tightlist"+"\n"+"  \\item"+"\n"+"    Section \\ref{", "jhgbnm"+"\n"+"  \\begin{itemize}"+"\n"+"  \\item"+"\n"+"    Section \\ref{")

    data = data.replace("\\subsection{", "\\section{")

    data = data.replace("\\subsubsection{", "\\subsection{")
    print(filename, " what is the filename --- ")
    data = data.replace("\\label{contents}","\\label{contents-"+file2[9:len(file2)-4]+"}")

    data = data.replace("\\hypertarget{contents}","\\hypertarget{contents-"+file2[9:len(file2)-4]+"}")

    data = data.replace("\\caption", "aghdwmz\\")
      ## maketitle tex issue  
#     if(file2 =="executed/coase.tex"):
#         func_replace("Coase?s", "Coase's", file2)

#     if(file2 == "executed/dyn_stack.tex"):
#         func_replace("vs.~Stackelberg", "vs. Stackelberg", file2)
#         func_replace("vs.stackelberg", "vs-stackelberg", file2)
    return data


def func_delete(a, b, f, delete_within_line=True):
    beginDelete = False
    endDelete = False
    edited = []
    for line in f.readlines():
        if delete_within_line is True:
           if a in line and b in line:
              line = re.sub(a+'.*?'+b,'',line)
           edited.append(line)
        else:
           if a in line:
              beginDelete = True
           if beginDelete is False or endDelete is True:
              edited.append(line)
           if b in line:
              endDelete = True

    return edited

def make_changes(f, filename):
    ## read the file contents

    data = f.read()
    data += "Section \\ref{equation- \\n href{zreferences.ipynb\#  href{zreferences.html\# "
    data = func_replace(f, data, filename)
    data = func_delete("vbnmc", "jhgbnm", f, False)
    data = func_delete("aghdwmz", "}", f)
    f.write(data)

def main(self, filename):
    with open(filename,'r+', encoding="utf8") as f:
        make_changes(f, filename)
            

