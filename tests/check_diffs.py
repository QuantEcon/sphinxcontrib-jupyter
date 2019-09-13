"""
Check diffs for each test file

Diff Configuration
------------------
Currently this is setup to ignore metadata as the extension will generate
a minimal notebook. So opening a notebook and saving will add metadata
that will cause the diff checker to fail.

"""

import nbformat
import glob
import os
from nbdime.diffing.notebooks import diff_notebooks, set_notebook_diff_targets
import sphinx
import re
import sys
if sys.version_info.major == 2:
    import fnmatch


SPHINX_VERSION = sphinx.version_info
CONFIGSETS = ['base', 'pdf', "no_inline_exercises"]

#-Diff Configuration-#
NB_VERSION = 4
set_notebook_diff_targets(metadata=False)

# Specify which version of sphinx that should exclude comparison files
SPHINX_VERSION_EXCLUDE = {
    1 : ['index*']
}

def python27_glob(path, pattern):
    matches = []
    for root, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, pattern):
            matches.append(os.path.join(root, filename))
    return matches

def check_set(PATH):
    if sys.version_info.major == 2:
        GENERATED_IPYNB_FILES = python27_glob(PATH+"/_build/jupyter/", "*.ipynb")
        ref_files = python27_glob(PATH + "/ipynb/", "*.ipynb")
        REFERENCE_IPYNB_FILES = [fl.split("ipynb/")[-1] for fl in ref_files] 
    else:
        GENERATED_IPYNB_FILES = glob.glob(PATH + "/_build/jupyter/**/*.ipynb", recursive=True)
        ref_files = glob.glob(PATH + "/ipynb/**/*.ipynb", recursive=True)
        REFERENCE_IPYNB_FILES = [fl.split("ipynb/")[-1] for fl in ref_files]
    failed = 0
    for fl in GENERATED_IPYNB_FILES:
        flname = fl.split("jupyter/")[-1]
        #Check for Sphinx Version Specific Excludes
        SKIP = False
        if SPHINX_VERSION[0] in SPHINX_VERSION_EXCLUDE.keys():
            exclude_patterns = SPHINX_VERSION_EXCLUDE[SPHINX_VERSION[0]]
            for pattern in exclude_patterns:
                pattern = re.compile(pattern)
                if pattern.search(flname):
                    print("Excluding: {} (due to SPHINX_VERSION_EXCLUDE)".format(fl))
                    SKIP = True
        if SKIP:
            continue
        else:
            print("Testing {} ...".format(fl))
            if flname not in REFERENCE_IPYNB_FILES:
                print("[FAIL] Notebook {} has no matching test case in ipynb/".format(flname))
                failed += 1
                continue
            nb1 = nbformat.read(fl, NB_VERSION)
            nb2 = nbformat.read(os.path.join(PATH+"/ipynb", flname), NB_VERSION)
            diff = diff_notebooks(nb1, nb2)
            if len(diff) != 0:
                print("[FAIL] {} and {} are different:".format(
                    fl, os.path.join("ipynb", flname)))
                print(diff)
                failed += 1
    return failed

#-Main-#
for configset in CONFIGSETS:
    print("Testing Configuration Set: {}".format(configset))
    failed = check_set(configset)
    if failed != 0:
        exit(failed)
