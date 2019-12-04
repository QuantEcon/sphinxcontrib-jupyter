"""
Translators for working with Code Blocks
"""

from docutils.nodes import SparseNodeVisitor
from sphinx.util.docutils import SphinxTranslator

from .notebook import JupyterNotebook

class SphinxSparseTranslator(SparseNodeVisitor):
    def __init__(self, document, builder):
        super().__init__(document)
        self.builder = builder
        self.config = builder.config
        self.settings = document.settings

class JupyterCodeBlockTranslator(SphinxSparseTranslator):
    
    in_literal_block = False

    def __init__(self, document, builder):
        """
        A translator for extracting code-blocks from RST documents 
        and generating a Jupyter Notebook
        """
        super().__init__(document, builder)  #add document, builder, config and settings to object
        self.warn = self.document.reporter.warning
        self.error = self.document.reporter.error
        #-Jupyter Settings-#
        self.language = builder.config["jupyter_language"]
        self.jupyter_lang_synonyms = builder.config["jupyter_language_synonyms"]

    def visit_document(self, node):
        self.output = JupyterNotebook(language=self.language)
        #Collector List for Current Cell
        self.new_cell()

    def depart_document(self, node):
        pass

    def visit_literal_block(self, node):
        "Parse Literal Blocks (Code Blocks)"
        self.in_literal_block = True
        self.cell_type = "code"
        if "language" in node.attributes:
            self.nodelang = node.attributes["language"].strip()
        else:
            self.nodelang = self.language    #use notebook language
        if self.nodelang == 'default':
            self.nodelang = self.language
        if self.nodelang != self.language:
            self.cell.append("``` {}".format(self.nodelang))
            self.cell_type = "markdown"

    def depart_literal_block(self, node):
        if self.nodelang != self.language:
            self.cell.append("```")
        source = "".join(self.cell)
        self.output.add_cell(source, self.cell_type)
        self.new_cell()
        self.in_literal_block = False

    def visit_Text(self, node):
        text = node.astext()
        if self.in_literal_block:
            self.cell.append(text)

    def depart_Text(self, node):
        pass

    #Utilities

    def new_cell(self):
        self.cell = []
        self.cell_type = None

