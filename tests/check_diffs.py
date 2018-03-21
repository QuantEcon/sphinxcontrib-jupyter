"""
Check diffs for each test file
"""

import nbformat
from nbdime.diffing.notebooks import diff_notebooks

fl1 = nbformat.read(
    "_build/jupyter/simple_notebook.ipynb", 4)
fl2 = nbformat.read(
    "ipynb/simple_notebook.ipynb", 4)

results = diff_notebooks(fl1, fl2)

if len(results) == 0:
    exit(0)
else:
    exit(1)