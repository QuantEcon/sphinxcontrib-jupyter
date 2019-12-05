"""
    Utility functions needed primarily in builders
"""
import os
import json
from hashlib import md5
from sphinx.util.osutil import ensuredir
from shutil import copy
from munch import munchify


def normalize_cell(cell):
    cell.source = cell.source.strip().replace('\n','')
    return cell

def create_hashcode(cell):
    hashcode = md5(cell.source.encode()).hexdigest()
    return hashcode

def create_hash(cell):
    hashcode = create_hashcode(cell)
    cell.metadata.hashcode = hashcode
    return cell

def combine_executed_files(executedir, nb, docname):
    codetreeFile = executedir + "/" + docname + ".codetree"
    execution_count = 0
    count = 0
    if os.path.exists(codetreeFile):
        with open(codetreeFile, "r", encoding="UTF-8") as f:
            json_obj = json.load(f)

        for cell in nb.cells:
            if cell['cell_type'] == "code":
                execution_count += 1
                cellcopy = normalize_cell(cell.copy())
                hashcode = create_hashcode(cellcopy)
                output = json_obj[hashcode]['outputs']
                cell['execution_count'] = execution_count
                cell['outputs'] = munchify(output)
                if cell['metadata']['hide-output']:
                    cell['outputs'] = []

    return nb

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