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
        super().__init__(document, builder)  #add document, builder, config and settings to object
        self.warn = self.document.reporter.warning
        self.error = self.document.reporter.error
        #-Jupyter Settings-#
        self.language = builder.config["jupyter_language"]
        self.jupyter_lang_synonyms = builder.config["jupyter_language_synonyms"]

    def visit_document(self, node):
        self.output = JupyterNotebook(language=self.language)
        #Collector List for Current Cell
        self.cell = []

    def depart_document(self, node):
        pass

    def visit_literal_block(self, node):
        "Parse Literal Blocks (Code Blocks)"
        self.in_literal_block = True
        try:
            self.nodelang = node.attributes["language"].strip()
        except KeyError:
            self.nodelang = self.language
        if self.nodelang == 'default':
            self.nodelang = self.language

    def depart_literal_block(self, node):
        source = "".join(self.cell)
        self.output.add_code_cell(source)
        self.cell = []
        self.in_literal_block = False

    def visit_Text(self, node):
        text = node.astext()
        self.cell.append(text)

    def depart_Text(self, node):
        pass

