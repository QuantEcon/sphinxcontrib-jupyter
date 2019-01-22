import nbformat
from sphinx.util.osutil import ensuredir
import os.path
import time
from nbconvert.preprocessors import ExecutePreprocessor

JUPYTER_EXECUTED = "_build/jupyter/executed/{}"
JUPYTER_COVERAGE = "_build/jupyter/coverage/{}"
JUPYTER_REPORTS = "_build/jupyter/reports/{}"


class ExecuteNotebookWriter():
    """
    Executes jupyter notebook written in python or julia
    """
    def execute_notebook(self, f, filename):
        execute_nb_config = self.config["jupyter_execute_nb"]
        coverage = execute_nb_config["coverage"]
        timeout = execute_nb_config["timeout"]

        # get a NotebookNode object from a string
        nb = nbformat.reads(f, as_version=4)
        language = nb.metadata.kernelspec.display_name

        # - Parse Directories - #
        if coverage:
            executed_notebook_dir = JUPYTER_COVERAGE.format(language)
        else:
            executed_notebook_dir = JUPYTER_EXECUTED.format(language)
        ensuredir(executed_notebook_dir)

        if coverage:
            ep = ExecutePreprocessor(timeout=timeout)
        else:
            ep = ExecutePreprocessor(timeout=timeout, allow_errors=True)
        
        starting_time = time.time()
        try:
            # Time how long it takes to process this notebook.
            future = self.client.submit(ep.preprocess, nb, {"metadata": {"path": executed_notebook_dir}})  #Execute in target directory
            self.futures.append(future)
        except Exception as e:
            print(e)
        finally:
            total_time = time.time() - starting_time
            # save executed notebook
            notebook_name = "{}.ipynb".format(filename)
            executed_notebook_path = os.path.join(executed_notebook_dir, notebook_name)
            #Parse Executed notebook to remove hide-output blocks
            for cell in nb['cells']:
                if cell['cell_type'] == "code":
                    if cell['metadata']['hide-output']:
                        cell['outputs'] = []
            #Write Executed Notebook as File
            with open(executed_notebook_path, "wt", encoding="UTF-8") as f:
                nbformat.write(nb, f)
        
        results = dict()
        results['runtime'] = total_time
        results['filename'] = filename
        #results['errors'] = error_result
        results['language'] = language

        return results
