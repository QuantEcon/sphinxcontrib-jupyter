import nbformat
from sphinx.util.osutil import ensuredir
import os.path
import time
import json
from nbconvert.preprocessors import ExecutePreprocessor

from dask.distributed import as_completed

JUPYTER_EXECUTED = "_build/jupyter/executed/{}"
JUPYTER_COVERAGE = "_build/jupyter/coverage/{}"
JUPYTER_REPORTS = "_build/jupyter/reports/"
JUPYTER_ERROR = "_build_coverage/reports/{}"
JUPYTER_COVERAGE = "_build_coverage/{}/jupyter"


class ExecuteNotebookWriter():
    
    """
    Executes jupyter notebook written in python or julia
    """

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
            ep = ExecutePreprocessor(timeout=-1, allow_errors=True)
        starting_time = time.time()

        future = self.client.submit(ep.preprocess, nb, {"metadata": {"path": self.executed_notebook_dir, "filename": filename, "start_time" : starting_time}})
        self.futures.append(future)

        
    def save_executed_notebook(self):
        error_results = []

        self.dask_log['scheduler_info'] = self.client.scheduler_info()
        self.dask_log['futures'] = []

        # this for loop gathers results in the background
        for future, nb in as_completed(self.futures, with_results=True):
            error_result = []
            self.dask_log['futures'].append(str(future))
            # store the exceptions in an error result array
            if future.status == 'error':
                error_result.append(future.exception())
                future.close()
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

        print(json_filename)
        try:
            with open(json_filename, "w") as json_file:
                json.dump(json_data, json_file)
        except IOError:
            self.logger.warning("Unable to save lecture status JSON file. Does the {} directory exist?".format(JUPYTER_REPORTS))

    def produce_dask_processing_report(self, fln= "dask-reports.json"):
        """
            produces a report of dask execution
        """
        ensuredir(JUPYTER_REPORTS)
        json_filename = JUPYTER_REPORTS + fln

        try:
            with open(json_filename, "w") as json_file:
                json.dump(self.dask_log, json_file)
                print(json_filename)
        except IOError:
            self.logger.warning("Unable to save dask reports JSON file. Does the {} directory exist?".format(JUPYTER_REPORTS))

    def create_coverage_report(self, error_results):
        """
            Creates a coverage report of the errors in notebook
        """
        errors = []
        error_results = []
        errors_by_language = dict()
        produce_text_reports = self.config["jupyter_execute_nb"]["text_reports"]
        
        #Parse Error Set
        for full_error_set in error_results:
            error_result = full_error_set['errors']
            filename = full_error_set['filename']
            current_language = full_error_set['language']
            language_name = current_language['extension']

            if error_result:
                if language_name not in errors_by_language:
                    errors_by_language[language_name] = dict()
                    errors_by_language[language_name]['display_name'] = current_language['display_name']
                    errors_by_language[language_name]['language'] = current_language['language']
                    errors_by_language[language_name]['files'] = dict()

                errors += error_result
                error_files.append(filename)

                errors_by_language[language_name]['files'][filename] = error_result

        # Create the error report from the HTML template, if it exists.
        error_report_template_file = self.config["jupyter_template_coverage_file_path"]

        error_report_template = []
        if not os.path.isfile(error_report_template_file):
            print("Unable to generate error report - template not found.")
        else:
            with open(error_report_template_file) as inputFile:
                error_report_template = inputFile.readlines()

        lang_summary = ""
        notebook_looper = ""
        for lang_ext in errors_by_language:
            language_display_name = errors_by_language[lang_ext]['display_name']
            language = errors_by_language[lang_ext]['language']
            errors_by_file = errors_by_language[lang_ext]['files']
            error_dir = JUPYTER_ERROR.format(lang_ext)

            if produce_text_reports:
                # set specific language output file
                lang_error_dir = "{}/{}_errors".format(error_dir, lang_ext)
                # purge language results directory and recreate
                shutil.rmtree(path=lang_error_dir, ignore_errors=True)
                os.makedirs(lang_error_dir)

            if errors_by_file:
                # errors dictionary
                error_count_dict = dict()
                error_files_dict = dict()

                # create the HTML for the notebook filenames
                notebook_list_HTML = ""

                # write to results file
                # overview output file
                if produce_text_reports:
                    results_file = open("{}/{}_overview.txt".format(error_dir, lang_ext), 'w')
                    results_file.write(language_display_name + " execution errors occurred in the notebooks below:\n")

                logger.error(language_display_name + " execution errors occurred in the notebooks below")

                error_number = 1
                for filename in errors_by_file:
                    logger.error(filename)

                    number_of_errors = str(len(errors_by_file[filename]))
                    if produce_text_reports:
                        results_file.write("\t{} - {} errors.\n".format(filename, number_of_errors))

                    notebook_list_HTML += "<li><a href=\"#{}\">{}</a></li>".format(lang_ext + "_" + filename, filename)
                    notebook_looper += "<h3 id=\"{}\">{} - {} {} errors</h3>\n".format(
                        lang_ext + "_" + filename, filename, number_of_errors, language_display_name)

                    if produce_text_reports:
                        error_file = open("{}/{}_errors.txt".format(lang_error_dir, filename), "w")

                    for error in errors_by_file[filename]:
                        # Some errors don't provide a traceback. Make sure that some useful information is provided
                        # to the report - if nothing else, the type of error that was caught.
                        traceback = getattr(error, "traceback", None)
                        if traceback is None:
                            error.traceback = str(error)

                        last_line = error.traceback.splitlines()[-1]
                        if last_line not in error_files_dict:
                            error_files_dict[last_line] = []
                        error_files_dict[last_line].append(error_number)

                        if last_line not in error_count_dict:
                            error_count_dict[last_line] = 0
                        error_count_dict[last_line] += 1

                        notebook_looper += "<pre><code class=\""\
                                        + language\
                                        + "\">{}</code></pre>\n".format(error.traceback)

                        error_number += 1

                        if produce_text_reports:
                            error_file.write(error.traceback + "\n")

                    if produce_text_reports:
                        error_file.close()

                if notebook_list_HTML != "":
                    lang_summary += "<p>" + language_display_name \
                                    + " execution errors occured in the following notebooks:</p><ul>"\
                                    + notebook_list_HTML + " </ul>"

                # write error count and errors to overview.txt
                if produce_text_reports:
                    results_file.write("\n----------------------\nError count details: [count] error\n\n")
                    for key, value in error_count_dict.items():
                        results_file.write("[{}] {}\n".format(value, key))
                        results_file.write('\n')

                    results_file.write("\nFor specifics, including the cell block, refer to [notebook name]_errors.txt\n")
                    results_file.close()

            else:
                # no errors. Update overview to show that
                if produce_text_reports:
                    results_file = open("{}/{}_overview.txt".format(error_dir, lang_ext), 'w')
                    results_file.write("No errors occurred!\n")
                    results_file.close()

            # create the dictionary of variables to inject into the HTML template
            variables = dict()
            variables['ERROR_SUMMARY'] = lang_summary
            variables['NOTEBOOK_LOOP'] = notebook_looper
            variables['DATETIME'] = time.strftime("%c")

            # Save the error report.
            filename = "errors-" + time.strftime("%d%m%Y") + ".html"
            full_error_report_filename = os.path.normpath(error_dir + "/" + filename)
            with open(full_error_report_filename, "w") as error_output_file:
                for line in error_report_template:
                    for keyName in variables:
                        target_string = "{" + keyName + "}"
                        line = line.replace(target_string, variables[keyName])

                    error_output_file.write(line)


