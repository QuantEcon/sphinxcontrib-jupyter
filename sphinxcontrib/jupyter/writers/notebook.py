"""
An Object Representing a Jupyter Notebook
"""

import nbformat.v4 as nbformat
from jupyter_client.kernelspec import get_kernel_spec, find_kernel_specs

class JupyterKernelNotFound(Exception):
    pass

class JupyterNotebook:

    def __init__(self):
        self.notebook = nbformat.new_notebook()

    def add_code_cell(self, source, metadata=None):
        code_cell = nbformat.new_code_cell(source)
        if metadata:
            for k,v in metadata.items():
                code_cell.metadata[k] = v
        self.notebook["cells"].append(code_cell)

    def add_markdown_cell(self, formatted_text):
        markdown_cell = nbformat.new_markdown_cell(formatted_text)
        self.notebook["cells"].append(markdown_cell)

    def add_kernelspec(self, language):
        self.kernelspec = get_kernel_spec(language)
        # if language not in self.available_kernelspecs.keys():
        #     msg = "Requested kernel: {} is not among the available kernels\n{}".format(language, self.available_kernels)
        #     raise JupyterKernelNotFound(msg)
        kernel = {
            "kernelspec": {
                "display_name": self.kernelspec.display_name,
                "language": language,
                }
            }
        self.notebook.metadata.kernelspec = kernel