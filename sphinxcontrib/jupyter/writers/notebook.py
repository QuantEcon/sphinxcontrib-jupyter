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
import nbformat.v4 as nbf
from jupyter_client.kernelspec import get_kernel_spec, find_kernel_specs

class JupyterNotebook:

    def __init__(self, language="python"):
        """
        A simple object that represents a Jupyter notebook
        """
        self.nb = nbf.new_notebook()
        self.add_kernelspec(language)

    @property
    def notebook(self):
        return self.nb

    @property
    def notebook_as_string(self):
        return self.writes()

    def add_cell(self, source, cell_type, **kwargs):
        if cell_type == "markdown":
            self.add_markdown_cell(source, **kwargs)
        elif cell_type == "code":
            self.add_code_cell(source, **kwargs)
        elif cell_type == "raw":
            self.add_raw_cell(source, **kwargs)
        else:
            raise InvalidJupyterCell("{} is not a valid Jupyter Cell type".format(cell_type))

    def add_code_cell(self, source, metadata=None, **kwargs):
        """
        Append a Code Cell to the Notebook

        Parameters
        ----------
        source : str
        metadata : dict, optional(default=None)
                   Add metadata to the cell
        """
        code_cell = nbf.new_code_cell(source, **kwargs)
        if metadata:
            code_cell = self.add_metadata(code_cell, metadata)
        self.nb["cells"].append(code_cell)

    def add_markdown_cell(self, formatted_text, metadata=None, **kwargs):
        """
        Append a Markdown Cell to the Notebook

        Parameters
        ----------
        formatted_text : str
        """
        markdown_cell = nbf.new_markdown_cell(formatted_text, **kwargs)
        if metadata:
            markdown_cell = self.add_metadata(markdown_cell, metadata)
        self.nb["cells"].append(markdown_cell)

    def add_raw_cell(self, source, metadata=None, **kwargs):
        """        
        Append a Raw Cell to the Notebook

        Parameters
        ----------
        source : str
        """
        raw_cell = nbf.new_raw_cell(source, **kwargs)
        if metadata:
            raw_cell = self.add_metadata(raw_cell, metadata)
        self.nb["cells"].append(raw_cell)

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
        self.nb.metadata.kernelspec = kernelspec

    def write(self, fl):
        """
        https://nbformat.readthedocs.io/en/latest/api.html#nbformat.write
        """
        nbformat.write(self.nb, fl)

    def writes(self):
        """
        https://nbformat.readthedocs.io/en/latest/api.html#nbformat.writes
        """
        return nbformat.writes(self.nb)

    def read(self, fl):
        """
        https://nbformat.readthedocs.io/en/latest/api.html#reading-and-writing
        """
        self.nb = nbformat.read(fl)

    def add_metadata(self, cell, metadata):
        """ Attach Metadata to a cell """   
        for k,v in metadata.items():
            cell.metadata[k] = v
        return cell

    def add_metadata_notebook(self, metadata):
        """ Attach Metadata to a notebook """
        for k,v in metadata.items():
            self.nb.metadata[k] = v



#Custom Exceptions

class JupyterKernelNotFound(Exception):
    pass

class InvalidJupyterCell(Exception):
    pass



#-Experimental Ideas-#

import textwrap

class JupyterCell:
    """
    Example
    -------
    from notebook import JupyterCell
    c = JupyterCell()
    c.add_text("Hi there")
    c.add_highlighted_markdown("import numpy as np", "python")
    c.content
    """

    def __init__(self):
        """
        [Test] Concept Class -> May not be used
        Add inline and blocks
        """
        self.content = []
        self.type = None

    def __repr__(self):
        print("{type}:\n{content}".format(self.type, self.content))

    #Direct Entry

    def add_text(self, text):
        self.content.append(text)

    #Accumulated Elements

    @property
    def start_block(self):
        """ Accumulator for constructing blocks """
        self.block = []

    @property
    def finish_block(self):
        del self.block
    
    def add_highlighted_markdown(self, language):
        template = textwrap.dedent(
        """``` {language}
        {code}
        ```
        """
        )
        self.element.append(template.format(language, self.element))
    
    def add_bold(self, text):
        template = "**{text}**"
        self.content.append(template)


class BlockAccumulator:

    def __init__(self):
        self.__block = []
        self.__element = None
    
    @property
    def block(self):
        return "".join(self.__block)

    def add(self, val):
        self.__block.append(val)
    
    @property
    def element(self):
        return self.__element
    
    @element.setter
    def element(self, val):
        self.__element = val

    @property
    def add_element(self):
        self.__block.append(self.element)
        self.__element = None