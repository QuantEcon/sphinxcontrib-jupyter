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

def func_replace(f, data):
    #convert to string:
    f.seek(0)
    # print(data)
    # import pdb
    # pdb.set_trace()
    #data = data.replace(a, b)
    data = data.replace("href{zreferences.ipynb\#", "cite{zreferences.ipynb\#")
    data = data.replace("Section \\ref{equation-", "Eq.~\eqref{eq:")
    data = data.replace("href{zreferences.html\#", "cite{zreferences.html\#")
    data = data.replace("\\paragraph", "\\textbf")
    data = data.replace("\\maketitle", "\\maketitle"+"\n"+"    \\parskip 0.090in")
    data = data.replace("}{{[}","}ywqp")
    data = data.replace("tp{]}}", "glbu")
    data = data.replace(".png}\\\\", ".png}"+"\n"+"\\end{figure}")
    data = data.replace("{muth19}", "{muth1960}")
    data = data.replace("0.9\\paperheight}}{", "0.9\\paperheight}}{executed/")
    return data


def func_delete(a, b, f):
    texLista = make_texList(f)
    for i in range(0,len(texLista)):
        srr = ""
        srr += re.sub(a+'.*?'+b,'',texLista[i])
        f.write(srr)

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
    f.write(data)

def main(self, filename):
    with open(filename,'r+', encoding="utf8") as f:
        make_changes(f)
            

