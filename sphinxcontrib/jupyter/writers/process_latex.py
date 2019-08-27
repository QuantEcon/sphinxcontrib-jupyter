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

def func_replace(f, data):
    #convert to string:
    f.seek(0)
    # print(data)
    # import pdb
    # pdb.set_trace()
    #data = data.replace(a, b)
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

    clearFile("vbnmc", "jhgbnm")

    data = data.replace("\\label{contents}}", "\\label{contents}}"+"\n"+"vbnmc")

    data = data.replace("}"+"\n"+"\n"+"  \\begin{itemize}"+"\n"+"  \\tightlist"+"\n"+"  \\item"+"\n"+"    Section \\ref{", "jhgbnm"+"\n"+"  \\begin{itemize}"+"\n"+"  \\item"+"\n"+"    Section \\ref{")

    clearFile("vbnmc", "jhgbnm")

    data = data.replace("\\subsection{", "\\section{")

    data = data.replace("\\subsubsection{", "\\subsection{")

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


def func_delete(a, b, f, data):
    texLista = make_texList(f)
    srr = ""
    for i in range(0,len(texLista)):
        srr = ""
        srr += re.sub(a+'.*?'+b,'',texLista[i])
    return srr

def clearFile(beginDelete, stopDelete, path):

        input = open(path, "r")
        lines = input.readlines()
        input.close()

        currentFlag = False
        nextFlag = False
        deleteFlag =  False

        output = open(path, "w")

        for line in lines:
        if nextFlag == True:
        nextFlag = False
        deleteFlag = False

        if beginDelete in line:
        deleteFlag = True
        elif stopDelete in line:
        nextFlag = True

        if deleteFlag == False:
        output.write(line)

def make_changes(f):
    ## read the file contents

    data = f.read()
    data += "Section \\ref{equation- \\n href{zreferences.ipynb\#  href{zreferences.html\# "
    data = func_replace(f, data)
    # data = func_replace("href{zreferences.ipynb\#", "cite{zreferences.ipynb\#", f, data)
    # data = func_replace("Section \\ref{equation-", "Eq.~\eqref{eq:", f, data)
    # func_replace("href{zreferences.html\#", "cite{zreferences.html\#", f, data)
    # func_replace("\\paragraph", "\\textbf", f, data)
    # func_replace("\\maketitle", "\\maketitle"+"\n"+"    \\parskip 0.090in", f, data)
    # #func_delete("zreferences","#", f)
    # func_replace("}{{[}","}ywqp", f, data)
    # func_replace("tp{]}}", "glbu", f, data)
    # func_delete("ywqp", "glbu", f)
    data = func_delete("aghdwmz", "}", f, data)
    #data = func_delete(f, data)
    f.write(data)

def main(self, filename):
    with open(filename,'r+', encoding="utf8") as f:
        make_changes(f)
            

