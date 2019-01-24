import nbformat
from sphinx.util.osutil import ensuredir
import os.path
import time
import json
from nbconvert.preprocessors import ExecutePreprocessor

from dask.distributed import as_completed
from sphinx.util import logging

JUPYTER_EXECUTED = "_build/jupyter/executed/{}"
JUPYTER_COVERAGE = "_build/jupyter/coverage/{}"
JUPYTER_REPORTS = "_build/jupyter/reports/"

class ExecuteNotebookWriter():
    """
    Executes jupyter notebook written in python or julia
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)


    def execute_notebook(self, f, filename):
        execute_nb_config = self.config["jupyter_execute_nb"]
        coverage = execute_nb_config["coverage"]
        timeout = execute_nb_config["timeout"]
        filename = filename

        # get a NotebookNode object from a string
        nb = nbformat.reads(f, as_version=4)
        language = nb.metadata.kernelspec.display_name

        # - Parse Directories - #
        if coverage:
            self.executed_notebook_dir = JUPYTER_COVERAGE.format(language)
        else:
            self.executed_notebook_dir = JUPYTER_EXECUTED.format(language)
        ensuredir(self.executed_notebook_dir)

        if coverage:
            ep = ExecutePreprocessor(timeout=timeout)
        else:
            ep = ExecutePreprocessor(timeout=timeout, allow_errors=True)
        starting_time = time.time()

        future = self.client.submit(ep.preprocess, nb, {"metadata": {"path": self.executed_notebook_dir, "filename": filename, "start_time" : starting_time}})
        self.futures.append(future)

        
    def save_executed_notebook(self):
        error_results = []

        # this for loop gathers results in the background
        for future, nb in as_completed(self.futures, with_results=True):
            error_result = []
            # store the exceptions in an error result array
            if future.status == 'error':
                error_result.append(future.exception())
                continue

            # using indices since nb is a tuple
            passed_metadata = nb[1]['metadata'] 
            executed_nb = nb[0]
            language_info = executed_nb['metadata']['language_info']
            total_time = time.time() - passed_metadata['start_time']
            filename = passed_metadata['filename']


            notebook_name = "{}.ipynb".format(filename)
            executed_notebook_path = os.path.join(passed_metadata['path'], notebook_name)
            #Parse Executed notebook to remove hide-output blocks
            for cell in executed_nb['cells']:
                if cell['cell_type'] == "code":
                    if cell['metadata']['hide-output']:
                        cell['outputs'] = []
            #Write Executed Notebook as File
            with open(executed_notebook_path, "wt", encoding="UTF-8") as f:
                nbformat.write(executed_nb, f)
            
            # storing error info if any execution throws an error
            results = dict()
            results['runtime']  = total_time
            results['filename'] = filename
            results['errors']   = error_result
            results['language'] = language_info
            error_results.append(results)

        return error_results


    def produce_code_execution_report(self, error_results, fln = "code-execution-results.json"):
        """
        Updates the JSON file that contains the results of the execution of each notebook.
        """
        ensuredir(JUPYTER_REPORTS)
        json_filename = JUPYTER_REPORTS + fln

        if os.path.isfile(json_filename):
            with open(json_filename) as json_file:
                json_data = json.load(json_file)

                temp_dictionary = dict()
                for item in json_data['results']:
                    name = item['filename']
                    language = item['language']
                    if name not in temp_dictionary:
                        temp_dictionary[name] = dict()
                    temp_dictionary[name][language] = item
                json_data['results'] = []

        else:
            temp_dictionary = dict()
            json_data = dict()
            json_data['results'] = []

        # Generate the data for the JSON file.
        for notebook_errors in error_results:
            runtime = int(notebook_errors['runtime'] * 10)
            name = notebook_errors['filename']
            language = notebook_errors['language']['name']
            lang_extn = notebook_errors['language']['file_extension']

            seconds = (runtime % 600) / 10
            minutes = int(runtime / 600)

            nicer_runtime = str(minutes) + ":" + ("0" + str(seconds) if seconds < 10 else str(seconds))
            new_dictionary = {
                'filename': name,
                'runtime': nicer_runtime,
                'num_errors': len(notebook_errors['errors']),
                'extension': lang_extn,
                'language': language
            }

            if name not in temp_dictionary:
                temp_dictionary[name] = dict()
            temp_dictionary[name][language] = new_dictionary

        temp_list = []
        for key in temp_dictionary:
            for second_key in temp_dictionary[key]:
                temp_list.append(temp_dictionary[key][second_key])

        for item in sorted(temp_list, key=lambda k: k['filename']):
            json_data['results'].append(item)
        json_data['run_time'] = time.strftime("%d-%m-%Y %H:%M:%S")

        try:
            with open(json_filename, "w") as json_file:
                json.dump(json_data, json_file)
        except IOError:
            self.logger.warn("Unable to save lecture status JSON file. Does the {} directory exist?".format(JUPYTER_REPORTS))
            

