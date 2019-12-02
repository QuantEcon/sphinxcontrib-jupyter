import re
import nbformat.v4
import os.path
import datetime
import docutils

from docutils.nodes import SparseNodeVisitor, GenericNodeVisitor   #https://github.com/docutils-mirror/docutils/blob/e88c5fb08d5cdfa8b4ac1020dd6f7177778d5990/docutils/nodes.py#L1922
from .utils import LanguageTranslator, JupyterOutputCellGenerators, get_source_file_name

from sphinx.util.docutils import SphinxTranslator

from .notebook import JupyterNotebook

class JupyterCodeBlockTranslator(SphinxTranslator):
    """
    .. TODO: 
    
        1. setup new builder to call this translator
        2. replace JupyterCodeTranslator once working
    """

    def __init__(self, builder, document):
        super().__init__(builder, document)  #add document, builder, config and settings to object
        self.warn = self.document.reporter.warning
        self.error = self.document.reporter.error
        #-Jupyter Settings-#
        self.language = builder.config["jupyter_default_lang"]
        self.jupyter_lang_synonyms = builder.config["jupyter_lang_synonyms"]

    def visit_document(self, node):
        self.notebook = JupyterNotebook(language=self.language)
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
            self.nodelang = self.lang
        if self.nodelang == 'default':
            self.nodelang = self.lang

    def depart_literal_block(self, node):
        source = "".join(self.cell)
        self.notebook.add_code_cell(source)
        self.in_literal_block = False

    def visit_Text(self, node):
        text = node.astext()
        if self.in_literal_block:
            self.cell.append(text)

    def depart_Text(self, node):
        pass


#-Code for Refactoring-#

class JupyterCodeTranslator(GenericNodeVisitor):
    """
    Jupyter Code Translator
    
    Provides infrastructure for extracting code-blocks from RST files
    and serves as the BASE class for all other Translators
    """

    URI_SPACE_REPLACE_FROM = re.compile(r"\s")
    URI_SPACE_REPLACE_TO = "-"

    def __init__(self, builder, document):
        super(GenericNodeVisitor, self).__init__(document)

        self.lang = None
        self.nodelang = None
        self.visit_first_title = True

        self.lang_translator = LanguageTranslator(builder.config["templates_path"])

        # Reporter
        self.warn = self.document.reporter.warning
        self.error = self.document.reporter.error

        # Settings
        self.settings = document.settings
        self.builder = builder
        self.source_file_name = get_source_file_name(
            self.settings._source,
            self.settings.env.srcdir)
        self.default_lang = builder.config["jupyter_default_lang"]

        # Create output notebook
        self.output = nbformat.v4.new_notebook()

        # Variables defined in conf.py
        self.jupyter_kernels = builder.config["jupyter_kernels"]
        self.jupyter_lang_synonyms = builder.config["jupyter_lang_synonyms"]
        self.jupyter_drop_tests = builder.config["jupyter_drop_tests"]
        self.jupyter_write_metadata = builder.config["jupyter_write_metadata"]
        self.jupyter_drop_solutions = builder.config["jupyter_drop_solutions"]         #solutions = code-block solutions
        
        self.jupyter_ignore_no_execute = builder.config["jupyter_ignore_no_execute"]   #not used in current class? However relate to execution
        self.jupyter_ignore_skip_test = builder.config["jupyter_ignore_skip_test"]     #not used in current class? However relate to execution

        # Header Block
        template_paths = builder.config["templates_path"]
        header_block_filename = builder.config["jupyter_header_block"]

        full_path_to_header_block = None
        for template_path in template_paths:
            if header_block_filename:
                if os.path.isfile(template_path + "/" + header_block_filename):
                   full_path_to_header_block = os.path.normpath( template_path + "/" + header_block_filename)

        if full_path_to_header_block:
            with open(full_path_to_header_block) as input_file:
                lines = input_file.readlines()

            line_text = "".join(lines)
            formatted_line_text = self.strip_blank_lines_in_end_of_block(
                line_text)
            nb_header_block = nbformat.v4.new_markdown_cell(
                formatted_line_text)

            # Add the header block to the output stream straight away
            self.output["cells"].append(nb_header_block)

        # Write metadata
        if self.jupyter_write_metadata:
            meta_text = \
                "Notebook created: {:%Y-%m-%d %H:%M:%S}  \n"\
                "Generated from: {}  "

            metadata = meta_text.format(
                datetime.datetime.now(),
                self.source_file_name)

            self.output["cells"].append(
                nbformat.v4.new_markdown_cell(metadata))

        # Variables used in visit/depart
        self.in_code_block = False  # if False, it means in markdown_cell
        self.output_cell_type = None
        self.code_lines = []
        
        # set the value of the cell metadata["slideshow"] to slide as the default option
        self.slide = "slide" 
        self.metadata_slide = False  #value by default for all the notebooks, we change it for those we want

    # generic visit and depart methods
    # --------------------------------
    simple_nodes = (
        docutils.nodes.TextElement,
        docutils.nodes.image,
        docutils.nodes.colspec,
        docutils.nodes.transition)  # empty elements

    def default_visit(self, node):
        pass

    def default_departure(self, node):
        pass

    # specific visit and depart methods
    # ---------------------------------

    # =========
    # Sections
    # =========
    def visit_document(self, node):
        """at start
        """
        # we need to give the translator a default language!
        # the translator needs to know what language the document is written in
        # before depart_document is called.
        self.lang = self.default_lang

    def depart_document(self, node):
        """at end
        """
        if not self.lang:
            self.warn(
                "Highlighting language is not given in .rst file. "
                "Set kernel as default(python3)")
            self.lang = self.default_lang

        # metadata for slides, this activates the option where each cell can be a slide
        if self.metadata_slide:
            self.output.metadata.celltoolbar = "Slideshow"


        # Update metadata
        if self.jupyter_kernels is not None:
            try:
                self.output.metadata.kernelspec = \
                    self.jupyter_kernels[self.lang]["kernelspec"]
                self.output.metadata["filename"] = self.source_file_name.split("/")[-1]
                self.output.metadata["title"] = self.title
            except:
                self.warn(
                    "Invalid jupyter kernels. "
                    "jupyter_kernels: {}, lang: {}"
                    .format(self.jupyter_kernels, self.lang))

    def visit_highlightlang(self, node):
        lang = node.attributes["lang"].strip()
        if lang in self.jupyter_kernels:
            self.lang = lang
        else:
            self.warn(
                "Highlighting language({}) is not defined "
                "in jupyter_kernels in conf.py. "
                "Set kernel as default({})"
                .format(lang, self.default_lang))
            self.lang = self.default_lang

    # =================
    # Inline elements
    # =================
    def visit_Text(self, node):
        text = node.astext()
        if self.in_code_block:
            self.code_lines.append(text)

    def depart_Text(self, node):
        pass

    def visit_title(self, node):
        #TODO: add support for docutils .. title::
        if self.visit_first_title:
            self.title = node.astext()
        self.visit_first_title = False
        
    # ================
    #  code blocks
    # ================
    def visit_literal_block(self, node):
        _parse_class = JupyterOutputCellGenerators.GetGeneratorFromClasses(self, node)
        self.output_cell_type = _parse_class["type"]
        self.solution = _parse_class["solution"]
        self.test = _parse_class["test"]

        try:
            self.nodelang = node.attributes["language"].strip()
        except KeyError:
            self.nodelang = self.lang
        if self.nodelang == 'default':
            self.nodelang = self.lang

        # Translate the language name across from the Sphinx to the Jupyter namespace
        self.nodelang = self.lang_translator.translate(self.nodelang)

        self.in_code_block = True
        self.code_lines = []

        # If the cell being processed contains code written in a language other than the one that
        # was specified as the default language, do not create a code block for it - turn it into
        # markup instead.
        if self.nodelang != self.lang_translator.translate(self.lang):
            if self.nodelang in self.jupyter_lang_synonyms:
                pass
            else:
                self.output_cell_type = JupyterOutputCellGenerators.MARKDOWN

    def depart_literal_block(self, node):
        if self.solution and self.jupyter_drop_solutions:    
            pass # Skip solutions if we say to. 
        elif self.test and self.jupyter_drop_tests:
            pass # Skip tests if we say to.
        else: # Don't skip otherwise. 
            line_text = "".join(self.code_lines)
            formatted_line_text = self.strip_blank_lines_in_end_of_block(line_text)
            new_code_cell = self.output_cell_type.Generate(formatted_line_text, self)

            # add slide metadata on each cell, value by default: slide
            if self.metadata_slide:   #value by default for all the notebooks, we change it for those we want
                new_code_cell.metadata["slideshow"] = { 'slide_type': self.slide}
                self.slide = "slide"
            #Save Collapse Cell Option for HTML Parser
            if "collapse" in node["classes"]:
                new_code_cell["metadata"]["html-class"] = 'collapse'
            #Save hide-output cell option for HTML Parser
            if "hide-output" in node["classes"]:
                new_code_cell["metadata"]["hide-output"] = True
            else:
                new_code_cell["metadata"]["hide-output"] = False
            #Code Output
            if self.output_cell_type is JupyterOutputCellGenerators.CODE_OUTPUT:
                # Output blocks must  be added to code cells to make any sense.
                # This script assumes that any output blocks will immediately follow a code
                # cell; a warning is raised if the cell immediately preceding this output
                # block is not a code cell.
                #
                # It is assumed that code cells may only have one output block - any more than
                # one will raise a warning and be ignored.
                mostRecentCell = self.output["cells"][-1]
                if mostRecentCell.cell_type != "code":
                    self.warn("Warning: Class: output block found after a " +
                            mostRecentCell.cell_type + " cell. Outputs may only come after code cells.")
                elif mostRecentCell.outputs:
                    self.warn(
                        "Warning: Multiple class: output blocks found after a code cell. Each code cell may only be followed by either zero or one output blocks.")
                else:
                    mostRecentCell.outputs.append(new_code_cell)
            else:
                self.output["cells"].append(new_code_cell)

        self.in_code_block = False

    # ===================
    #  general methods
    # ===================
    @staticmethod
    def strip_blank_lines_in_end_of_block(line_text):
        lines = line_text.split("\n")

        for line in range(len(lines)):
            if len(lines[-1].strip()) == 0:
                lines = lines[:-1]
            else:
                break

        return "\n".join(lines)

