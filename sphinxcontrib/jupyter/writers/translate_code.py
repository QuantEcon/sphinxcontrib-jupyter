"""
Translators for working with Code Blocks
"""
from docutils import nodes
from docutils.nodes import SparseNodeVisitor
from sphinx.util.docutils import SphinxTranslator
from sphinx.util import logging

from .notebook import JupyterNotebook

logger = logging.getLogger(__name__)

class SphinxSparseTranslator(SparseNodeVisitor):
    def __init__(self, document, builder):
        super().__init__(document)
        self.builder = builder
        self.config = builder.config
        self.settings = document.settings

class JupyterCodeBlockTranslator(SphinxSparseTranslator):
    
    #Configuration (Literal Block)
    literal_block = dict()
    literal_block['in'] = False
    literal_block['no-execute'] = False

    def __init__(self, document, builder):
        """
        A sparse translator for extracting code-blocks from RST documents 
        and generating a Jupyter Notebook
        """
        super().__init__(document, builder)  #add document, builder, config and settings to object
        #-Jupyter Settings-#
        self.language = self.config["jupyter_language"]   #self.language = self.config['highlight_language'] (https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-highlight_language)
        self.language_synonyms = self.config['jupyter_language_synonyms']

    def visit_document(self, node):
        self.output = JupyterNotebook(language=self.language)
        #Collector List for Current Cell
        self.new_cell()

    def depart_document(self, node):
        pass

    def visit_literal_block(self, node):
        """
        Parse Literal Blocks (Code Blocks)
        """
        #Start new cell and add add current cell to notebook
        self.literal_block['in'] = True
        self.new_cell(cell_type = "code")

        #-Determine Language of Code Block-#
        if "language" in node.attributes:
            self.nodelang = node.attributes["language"].strip()
        else:
            self.cell_type = "markdown"   
        if self.nodelang == 'default':
            self.nodelang = self.language   #use notebook programming language

        #Check for no-execute status
        if  "classes" in node.attributes and "no-execute" in node.attributes["classes"]:
            self.literal_block['no-execute'] = True
        else:
            self.literal_block['no-execute'] = False

        ## Check node language is the same as notebook language else make it markdown
        if (self.nodelang != self.language and self.nodelang not in self.language_synonyms) or self.literal_block['no-execute']:
            logger.warning("Found a code-block with different programming \
                language to the notebook language. Adding as markdown"
            )
            raise nodes.SkipNode
            
    def depart_literal_block(self, node):
        source = "".join(self.cell)
        self.output.add_cell(source, self.cell_type)
        self.new_cell()
        self.literal_block['in'] = False

    def visit_Text(self, node):
        if self.literal_block['in']:
            text = node.astext()
            self.cell.append(text)

    def depart_Text(self, node):
        pass

    #Utilities

    def new_cell(self, cell_type="markdown"):
        self.cell = []
        self.cell_type = cell_type

