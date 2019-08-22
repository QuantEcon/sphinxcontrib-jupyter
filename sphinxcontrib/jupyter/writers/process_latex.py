import os
import sys
import glob
from io import open
import subprocess
from sphinx.util.osutil import ensuredir
from sphinx.util import logging

def make_texList(f):
    texList = []
    for line in f:
        texList.append(line)
    return texList

def func_replace(a, b, f):
    #convert to string:
    data = f.read()
    f.seek(0)
    f.write(data.replace(a, b))
    f.truncate()


def func_delete(a, b, f):
    texLista = make_texList(f)
    for i in range(0,len(texLista)):
        srr = ""
        srr += re.sub(a+'.*?'+b,'',texLista[i])
        f.write(srr)

def make_changes(f):
    func_replace("Section \\ref{equation-", "Eq.~\eqref{eq:", f)
    func_replace("href{zreferences.ipynb\#", "cite{zreferences.ipynb\#", f)
    # func_replace("href{zreferences.html\#", "cite{zreferences.html\#", f)
    # func_replace("\\paragraph", "\\textbf", f)
    # func_replace("\\maketitle", "\\maketitle"+"\n"+"    \\parskip 0.090in", f)
    # func_replace("% Add a bibliography block to the postdoc", "% Add a bibliography block to the postdoc"+"\n"+"    \\bibliographystyle{plain}"+"\n"+"    \\bibliography{_static/quant-econ}", f)
    #func_delete("zreferences","#", f)
    # func_replace("}{{[}","}ywqp", f)
    # func_replace("tp{]}}", "glbu", f)
    # func_delete("ywqp", "glbu", f)

def main(self, filename):
    with open(filename,'r+', encoding="utf8") as f:
        print(f, "name")
        make_changes(f)
            

