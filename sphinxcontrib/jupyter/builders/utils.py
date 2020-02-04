"""
Utility Functions to support Builders
"""
import os
import json
from hashlib import md5
from sphinx.util.osutil import ensuredir
from shutil import copy
from munch import munchify
import subprocess
import sys


def normalize_cell(cell):
    cell.source = cell.source.strip().replace('\n','')
    return cell

def create_hash(cell):
    hashcode = md5(cell.source.encode()).hexdigest()
    cell.metadata.hashcode = hashcode
    return cell

#TODO: @aakash Does this need logger messages for failure cases?
def combine_executed_files(executedir, nb, docname):
    codetreeFile = executedir + "/" + docname + ".codetree"
    execution_count = 0
    count = 0
    if os.path.exists(codetreeFile):
        with open(codetreeFile, "r", encoding="UTF-8") as f:
            codetree = json.load(f)

        for cell in nb.cells:
            if cell['cell_type'] == "code":
                execution_count += 1
                cellcopy = normalize_cell(cell.copy())
                hashcode = md5(cellcopy.source.encode()).hexdigest()
                if hashcode in codetree:
                    output = codetree[hashcode]['outputs']
                    cell['execution_count'] = execution_count
                    cell['outputs'] = munchify(output)
                    if 'hide-output' in cell['metadata']:
                        cell['outputs'] = []

    return nb

def check_codetree_validity(builder, nb, docname):
    """
    Check the validity of a codetree for each code block
    This checks the md5 hash to see if the codetree data needs to be 
    updated
    """
    if os.path.exists(builder.executedir):
        codetreeFile = builder.executedir + "/" + docname + ".codetree"
        if os.path.exists(codetreeFile):
            with open(codetreeFile, "r", encoding="UTF-8") as f:
                codetree = json.load(f)
            for cell in nb.cells:
                if cell['cell_type'] == "code":
                    cellcopy = normalize_cell(cell.copy())
                    cellcopy = create_hash(cellcopy)
                    if cellcopy.metadata.hashcode not in codetree.keys():
                        return True
        else:
            return True
    else:
        return True

    return False

def run_build(target):
    if sys.platform == 'win32':
        makecmd = os.environ.get('MAKE', 'make.bat')
    else:
        makecmd = 'make'
    try:
        return subprocess.call([makecmd, target])
    except OSError:
        print('Error: Failed to run: %s' % makecmd)
        return 1

def copy_dependencies(builderSelf, outdir = None):
    """
    Copies the dependencies of source files or folders specified in the config to their respective output directories
    """
    if outdir is None:
        outdir = builderSelf.outdir
    else:
        outdir = outdir
    srcdir = builderSelf.srcdir
    if 'jupyter_dependencies' in builderSelf.config and builderSelf.config['jupyter_dependencies'] is not None:
        depenencyObj = builderSelf.config['jupyter_dependencies']
        for key, deps in depenencyObj.items():
            full_src_path = srcdir + "/" + key
            if full_src_path.find('.') == -1:
                ## handling the case of key being a directory
                full_dest_path = outdir + "/" + key
                ensuredir(full_dest_path)
                for dep in deps:
                    copy(full_src_path + "/" + dep, full_dest_path,follow_symlinks=True)
            elif os.path.isfile(full_src_path):
                ## handling the case of key being a file
                # removing the filename to get the directory path
                index = key.rfind('/')
                if index!=0 and index != -1:
                    key = key[0:index]
                
                full_src_path = srcdir + "/" + key
                full_dest_path = outdir + "/" + key
                for dep in deps:
                    copy(full_src_path + "/" + dep, full_dest_path,follow_symlinks=True)