"""
An Object Representing a Jupyter Notebook

Example
-------

from notebook import JupyterNotebook
nb = JupyterNotebook()
nb.add_code_cell("import numpy as np", metadata={'collapse' : True})
nb.add_markdown_cell("Hi")
nb.add_raw_cell("--Bye--")
nb.add_kernelspec("python3")
nb.write("test.ipynb")

"""


import nbformat
import nbformat.v4 as nbapi
from jupyter_client.kernelspec import get_kernel_spec, find_kernel_specs

class JupyterNotebook:

    def __init__(self, language="python"):
        """
        A simple object that represents a Jupyter notebook
        """
        self.notebook = nbapi.new_notebook()
        self.add_kernelspec(language)

    def add_code_cell(self, source, metadata=None, **kwargs):
        """
        Append a Code Cell to the Notebook

        Parameters
        ----------
        source : str
        metadata : dict, optional(default=None)
                   Add metadata to the cell
        """
        code_cell = nbapi.new_code_cell(source, **kwargs)
        if metadata:
            code_cell = self.add_metadata(code_cell, metadata)
        self.notebook["cells"].append(code_cell)

    def add_markdown_cell(self, formatted_text, metadata=None, **kwargs):
        """
        Append a Markdown Cell to the Notebook

        Parameters
        ----------
        formatted_text : str
        """
        markdown_cell = nbapi.new_markdown_cell(formatted_text, **kwargs)
        if metadata:
            markdown_cell = self.add_metadata(markdown_cell, metadata)
        self.notebook["cells"].append(markdown_cell)

    def add_raw_cell(self, source, metadata=None, **kwargs):
        """        
        Append a Raw Cell to the Notebook

        Parameters
        ----------
        source : str
        """
        raw_cell = nbapi.new_raw_cell(source, **kwargs)
        if metadata:
            raw_cell = self.add_metadata(raw_cell, metadata)
        self.notebook["cells"].append(raw_cell)

    def add_kernelspec(self, language):
        """
        https://jupyter-client.readthedocs.io/en/stable/api/kernelspec.html
        """
        try:
            self.kernelspec = get_kernel_spec(language)
        except:
            msg = "Requested Jupyter Kernel for language: {language} is not found"
            raise JupyterKernelNotFound(msg)
        kernelspec = {
                "display_name": self.kernelspec.display_name,
                "language": self.kernelspec.language,
                "name" : language
            }
        self.notebook.metadata.kernelspec = kernelspec

    def write(self, fl):
        """
        https://nbformat.readthedocs.io/en/latest/api.html#nbformat.write
        """
        nbformat.write(self.notebook, fl)

    def read(self, fl):
        """
        https://nbformat.readthedocs.io/en/latest/api.html#reading-and-writing
        """
        self.notebook = nbformat.read(fl)

    def add_metadata(self, cell, metadata):
        """ Attach Metadata to a cell """   
        for k,v in metadata.items():
            cell.metadata[k] = v
        return cell

#Custom Exceptions

class JupyterKernelNotFound(Exception):
    pass