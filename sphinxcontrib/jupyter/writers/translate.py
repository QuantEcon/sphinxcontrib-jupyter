"""
Base Jupyter Translator
"""

import re
import nbformat.v4
import os.path
import datetime
import docutils

from docutils.nodes import SparseNodeVisitor, GenericNodeVisitor   #https://github.com/docutils-mirror/docutils/blob/e88c5fb08d5cdfa8b4ac1020dd6f7177778d5990/docutils/nodes.py#L1922
from sphinx.util import logging
from sphinx.util.docutils import SphinxTranslator

from .utils import LanguageTranslator, JupyterOutputCellGenerators, get_source_file_name
from .notebook import JupyterNotebook

logger = logging.getLogger(__name__)

from .markdown import MarkdownSyntax

class JupyterBaseTranslator(SphinxTranslator):

    #Configuration (Formatting)
    sep_lines = "  \n"              #TODO: needed?
    sep_paragraph = "\n\n"          #TODO: needed?
    indent_char = " "               #TODO: needed?
    indent = indent_char * 4        #TODO: needed?
    indents = []                    #TODO: needed?
    section_level = 0
    #-Configuration (Formatting Lists)
    list_level = 0
    bullets = []
    list_item_starts = []
    #-Configuration (References)
    in_reference = False
    reference_text_start = 0
    #Configuration (File)
    default_ext = ".ipynb"
    #Configuration (Math)
    math_block_label = None
    #Configuration (Static Assets)
    images = []
    files = []
    #Configuration (Tables)
    table_builder = None    #TODO: table builder object
    #Configuration (visit/depart)
    in_block_quote = False
    in_note = False
    in_attribution = False
    in_rubric = False
    in_footnote = False
    in_footnote_reference = False
    in_download_reference = False
    in_inpage_reference = False
    in_citation = False
    in_caption = False
    in_toctree = False
    in_list = False
    in_math = False
    in_math_block = False
    in_topic = False
    in_literal_block = False
    in_code_block = False
    
    def __init__(self, document, builder):
        """
        Base Class for JupyterIPYNBTranslator, JupyterHTMLTranslator, JupyterPDFTranslator
        
        Handles common nodes and code-blocks for the suite of Jupyter Translators
        
        1. `SphinxTranslator <https://github.com/sphinx-doc/sphinx/blob/master/sphinx/util/docutils.py>`__
        """
        super().__init__(document, builder)
        #-Jupyter Settings-#
        self.language = self.config["jupyter_language"]   #self.language = self.config['highlight_language'] (https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-highlight_language)
        self.language_synonyms = self.config['jupyter_language_synonyms']
        self.md = MarkdownSyntax()

    #Document

    def visit_document(self, node):
        self.output = JupyterNotebook(language=self.language)
        self.new_cell()     #Initialise Cell

    def depart_document(self, node):
        pass

    def visit_section(self, node):
        self.section_level += 1

    def depart_section(self, node):
        self.section_level -= 1

    def visit_topic(self, node):
        self.in_topic = True

    def depart_topic(self, node):
        self.in_topic = False

    def visit_comment(self, node):
        raise nodes.SkipNode
    
    ### TODO: figure out if this literal_block definitions should be kept in codeblock translator or her in base translator
    def visit_literal_block(self, node):
        "Parse Literal Blocks (Code Blocks)"
        self.in_literal_block = True
        self.cell_type = "code"
        if "language" in node.attributes:
            self.nodelang = node.attributes["language"].strip()
        else:
            self.cell_type = "markdown"   
        if self.nodelang == 'default':
            self.nodelang = self.language   #use notebook language
        #Check node language is the same as notebook language
        if self.nodelang != self.language:
            logger.warning("Found a code-block with different programming \
                language to the notebook language. Adding as markdown"
            )
            self.cell.append("``` {}".format(self.nodelang))
            self.cell_type = "markdown"

    def depart_literal_block(self, node):
        if self.nodelang != self.language:
            self.cell.append("```")
        source = "".join(self.cell)
        self.output.add_cell(source, self.cell_type)
        self.new_cell()
        self.in_literal_block = False

    ### NOTE: special case to be handled for pdf in pdf only translators, check other translators for reference
    def visit_math_block(self, node):
        """directive math"""
        # visit_math_block is called only with sphinx >= 1.8

        self.in_math_block = True

        if self.in_list and node["label"]:
            self.markdown_lines.pop()  #remove entry \n from table builder

        #check for labelled math
        if node["label"]:
            #Use \tags in the LaTeX environment
            referenceBuilder = " \\tag{" + str(node["number"]) + "}\n"
            #node["ids"] should always exist for labelled displaymath
            self.math_block_label = referenceBuilder

    def depart_math_block(self, node):
        if self.in_list:
            self.markdown_lines[-1] = self.markdown_lines[-1][:-1]  #remove excess \n

        self.in_math_block = False

    # general paragraph
    def visit_paragraph(self, node):
        pass

    def depart_paragraph(self, node):
        if self.list_level > 0:
            self.markdown_lines.append(self.sep_lines)
        elif self.table_builder:
            pass
        elif self.block_quote_type == "epigraph":
            try:
                attribution = node.parent.children[1]
                self.markdown_lines.append("\n>\n")   #Continue block for attribution
            except:
                self.markdown_lines.append(self.sep_paras)
        else:
            self.markdown_lines.append(self.sep_paras)

    #Document.Nodes

    def visit_literal_block(self, node):
        """
        Parse Literal Blocks (Code Blocks)
        
        .. notes::

            1. node.attributes["highlight_args"] is used to identify code-blocks from raw text
               literal includes
        """
        #-Identify Type of Literal Block between :: and .. highlight:: or .. code-block-#
        if "highlight_args" in node.attributes:
            self.in_code_block = True       #literal text (with highlighting)
            self.cell_type = "code"
            if "language" in node.attributes:
                self.nodelang = node.attributes["language"].strip() 
            if self.nodelang == 'default':
                self.nodelang = self.language  #use notebook language
            #Check node language is the same as notebook language
            if self.nodelang != self.language:
                logger.warning("Found a code-block with different programming \
                    language to the notebook kernel. Adding as markdown"
                )
                self.cell.append(self.md.visit_code_block(self.nodelang))
                self.cell_type = "markdown"
        else:
            self.in_literal_block = True    #literal text (without highlighting)
            self.cell_type = "markdown"

    def depart_literal_block(self, node):
        if self.in_code_block and self.cell_type == "markdown":
            self.cell.append(self.md.depart_code_block())
        self.cell_to_notebook()
        self.in_literal_block = False
        self.in_code_block = False

    def visit_Text(self, node):
        text = node.astext()
        if self.in_literal_block or self.in_code_block:
            self.cell.append(text)

    def depart_Text(self, node):
        pass

    def unknown_visit(self, node):
        pass
        # raise NotImplementedError('Unknown node: ' + node.__class__.__name__)

    def unknown_departure(self, node):
        pass

    #Utilities

    def new_cell(self):
        self.cell = []
        self.cell_type = None

    def cell_to_notebook(self):
        source = "".join(self.cell)
        self.output.add_cell(source, self.cell_type)
        self.new_cell()


#-> REFACTORING <-#

class JupyterCodeTranslator(GenericNodeVisitor):  #-> OLD

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