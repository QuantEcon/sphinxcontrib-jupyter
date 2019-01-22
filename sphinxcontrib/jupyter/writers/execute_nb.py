import nbformat
from sphinx.builders import Builder
import os.path
import time
from nbconvert.preprocessors import ExecutePreprocessor

JUPYTER_EXECUTED = "_build/jupyter/executed/"
JUPYTER_COVERAGE = "_build/jupyter/coverage/"
JUPYTER_REPORTS = "_build/jupyter/reports"

def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)

class ExecuteNotebookWriter():
    """
    Executes jupyter notebook written in python or julia
    """
    def execute_notebook(self, f, filename):
        execute_nb_config = self.config["jupyter_execute_nb"]
        coverage = execute_nb_config["coverage"]
        timeout = execute_nb_config["timeout"]
        nb = nbformat.reads(f, as_version=4)

        mkdir(JUPYTER_EXECUTED)
        if coverage:
            ep = ExecutePreprocessor(timeout=timeout)
        else:
            ep = ExecutePreprocessor(timeout=timeout, allow_errors=True)   #kernel_name=language_info["kernel"]
        
        starting_time = time.time()
        try:
            # Time how long it takes to process this notebook.
            out = ep.preprocess(nb, {"metadata": {"path": JUPYTER_EXECUTED}})  #Execute in target directory

        except Exception as e:
            print(e)
        finally:
            total_time = time.time() - starting_time
            # save executed notebook
            notebook_name = "{}.ipynb".format(filename)
            executed_notebook_path = os.path.join(JUPYTER_EXECUTED, notebook_name)
            #Parse Executed notebook to remove hide-output blocks
            for cell in nb['cells']:
                if cell['cell_type'] == "code":
                    if cell['metadata']['hide-output']:
                        cell['outputs'] = []
            #Write Executed Notebook as File
            with open(executed_notebook_path, "wt", encoding="UTF-8") as f:
                nbformat.write(nb, f)
