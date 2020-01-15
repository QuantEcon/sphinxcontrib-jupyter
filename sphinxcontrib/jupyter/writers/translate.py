"""
Base Jupyter Translator
"""

import re
import nbformat.v4
import os.path
import datetime
import docutils

from docutils import nodes
from docutils.nodes import SparseNodeVisitor, GenericNodeVisitor   #https://github.com/docutils-mirror/docutils/blob/e88c5fb08d5cdfa8b4ac1020dd6f7177778d5990/docutils/nodes.py#L1922
from sphinx.util import logging
from sphinx.util.docutils import SphinxTranslator

from .utils import LanguageTranslator, JupyterOutputCellGenerators, get_source_file_name
from .notebook import JupyterNotebook

logger = logging.getLogger(__name__)

from .markdown import MarkdownSyntax

class JupyterBaseTranslator(SphinxTranslator):

    SPLIT_URI_ID_REGEX = re.compile(r"([^\#]*)\#?(.*)")

    #Configuration (Formatting)
    sep_lines = "  \n"              #TODO: needed?
    sep_paragraph = "\n\n"          #TODO: needed?
    section_level = 0

    ## Dictionary types are used below to store node variables to be used in specific translators  

    #-Configuration (References)
    reference_dict = dict()
    reference_dict['in'] = False
    reference_dict['reference_text_start'] = 0
    #Configuration (File)
    default_ext = ".ipynb"
    #Configuration (Math)
    math_block_dict = dict()
    math_block_dict['in'] = False
    math_block_dict['math_block_label'] = None
    #Configuration (Static Assets)
    images = []
    files = []
    #Configuration (Tables)
    table_builder = None    #TODO: table builder object
    #Configuration (visit/depart)
    title_dict = dict()
    title_dict['visit_first_title'] = True

    block_quote_dict = dict()
    block_quote_dict['in_block_quote'] = False

    footnote_dict = dict()
    footnote_dict['in'] = False

    footnote_reference = dict()
    footnote_reference['in'] = False

    download_reference_dict = dict()
    download_reference_dict['in'] = False

    citation_dict = dict()
    citation_dict['in'] = False

    literal_block_dict = dict()
    literal_block_dict['in'] = False
    literal_block_dict['no-execute'] = False

    image_dict = dict()
    target_dict = dict()

    list_dict = dict()
    list_dict['in'] = False
    list_dict['skip_next_content'] = False
    list_dict['list_item_starts'] = []
    list_dict['initial_lines'] = []
    list_dict['content_depth_to_skip'] = None
    list_dict['list_level'] = 0
    list_dict['bullets'] = []
    list_dict['indent_char'] = " "                            #TODO: needed?
    list_dict['indent'] = list_dict['indent_char'] * 4        #TODO: needed?
    list_dict['indents'] = []                                 #TODO: needed?

    math_dict = dict()
    math_dict['in'] = False

    in_note = False
    in_attribution = False
    in_rubric = False
    in_inpage_reference = False
    in_citation = False
    in_caption = False
    in_toctree = False
    in_topic = False
    remove_next_content = False

    ## options to remove?
    block_quote_dict['block_quote_type'] = "block-quote"

    # Slideshow option
    metadata_slide = False  #False is the value by default for all the notebooks
    slide = "slide" #value by default
    
    ## pdf book options
    in_book_index = False
    cell_trimmed = []
    
    def __init__(self, document, builder):
        """
        Base Class for JupyterIPYNBTranslator, JupyterHTMLTranslator, JupyterPDFTranslator
        
        Handles common nodes and code-blocks for the suite of Jupyter Translators
        
        1. `SphinxTranslator <https://github.com/sphinx-doc/sphinx/blob/master/sphinx/util/docutils.py>`__
        """
        super().__init__(document, builder)
        ### builder variables
        self.builder = builder
        self.config = builder.config
        self.settings = document.settings
        #-Jupyter Settings-#
        self.language = self.config["jupyter_language"]   #self.language = self.config['highlight_language'] (https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-highlight_language)
        self.language_synonyms = self.config['jupyter_language_synonyms']
        self.source_file_name = get_source_file_name(
            self.settings._source,
            self.settings.env.srcdir)

        self.md = MarkdownSyntax()

        self.list_dict['content_depth'] = self.config["jupyter_pdf_showcontentdepth"]


    #Document
    def visit_document(self, node):
        self.output = JupyterNotebook(language=self.language)
        self.new_cell()     #Initialise Cell

    def depart_document(self, node):
        self.cell_to_notebook()

    def visit_section(self, node):
        self.section_level += 1

    def depart_section(self, node):
        self.section_level -= 1

    def visit_topic(self, node):
        self.in_topic = True

    def depart_topic(self, node):
        self.in_topic = False

    def visit_exercise_node(self, node):
        pass

    def depart_exercise_node(self, node):
        pass

    def visit_compound(self, node):
        pass

    def depart_compound(self, node):
        pass

    def visit_inline(self, node):
        pass

    def depart_inline(self, node):
        pass

    def visit_title_reference(self, node):
        pass

    def depart_title_reference(self, node):
        pass

    def visit_title(self, node):
        if self.title_dict['visit_first_title']:
            self.title_dict['title'] = node.astext()
        self.title_dict['visit_first_title'] = False

    def depart_title(self, node):
        pass

    def visit_definition_list_item(self, node):
        pass

    def visit_doctest_block(self, node):
        pass

    def visit_comment(self, node):
        raise nodes.SkipNode
    
    def visit_image(self, node):
        """
        Notes
        -----
        1. Should this use .has_attrs()?
        2. the scale, height and width properties are not combined in this
        implementation as is done in http://docutils.sourceforge.net/docs/ref/rst/directives.html#image

        """
        self.image_dict['uri'] = node.attributes["uri"]
        attrs = node.attributes
        if self.config.jupyter_images_markdown:
            #-Construct MD image
            image = "![{0}]({0})".format(self.image_dict['uri'])
        else:
            # Construct HTML image
            image = '<img src="{}" '.format(self.image_dict['uri'])
            if "alt" in attrs.keys():
                image += 'alt="{}" '.format(attrs["alt"])
            style = ""
            if "width" in attrs.keys():
                style += "width:{};".format(attrs["width"])
            if "height" in attrs.keys():
                style += "height:{};".format(attrs["height"])
            if "scale" in attrs.keys():
                style = "width:{0}%;height:{0}%".format(attrs["scale"])
            image += 'style="{}" '.format(style)
            if "align" in attrs.keys():
                image += 'align="{}"'.format(attrs["align"])
            image = image.rstrip() + ">\n\n"  #Add double space for html
        
        self.image_dict['image'] = image
    
    def depart_image(self, node):
        pass
            


    ### TODO: figure out if this literal_block definitions should be kept in codeblock translator or here in base translator
    def visit_literal_block(self, node):
        "Parse Literal Blocks (Code Blocks)"
        self.literal_block_dict['in'] = True
        self.cell_to_notebook()
        self.cell_type = "code"

        if "language" in node.attributes:
            self.nodelang = node.attributes["language"].strip()
        else:
            self.cell_type = "markdown"
        if self.nodelang == 'default':
            self.nodelang = self.language   #use notebook language

        ## checking if no-execute flag
        if  "classes" in node.attributes and "no-execute" in node.attributes["classes"]:
            self.literal_block_dict['no-execute'] = True
        else:
            self.literal_block_dict['no-execute'] = False

        ## Check node language is the same as notebook language else make it markdown
        if (self.nodelang != self.language and self.nodelang not in self.language_synonyms) or self.literal_block_dict['no-execute']:
            logger.warning("Found a code-block with different programming \
                language to the notebook language. Adding as markdown"
            )
            self.cell.append("``` {} \n".format(self.nodelang))
            self.cell_type = "markdown"


    def depart_literal_block(self, node):
        if (self.nodelang != self.language and self.nodelang not in self.language_synonyms) or self.literal_block_dict['no-execute']:
            self.cell.append("```")
        self.cell_to_notebook()
        self.literal_block_dict['in'] = False

    ### NOTE: special case to be handled for pdf in pdf only translators, check other translators for reference
    def visit_math_block(self, node):
        """directive math"""
        # visit_math_block is called only with sphinx >= 1.8

        self.math_block_dict['in'] = True

        #check for labelled math
        if node["label"]:
            #Use \tags in the LaTeX environment
            referenceBuilder = " \\tag{" + str(node["number"]) + "}\n"
            #node["ids"] should always exist for labelled displaymath
            self.math_block_dict['math_block_label'] = referenceBuilder

    def depart_math_block(self, node):
        self.math_block_dict['in'] = False

    # general paragraph
    def visit_paragraph(self, node):
        pass

    def depart_paragraph(self, node):
        pass

    def visit_raw(self, node):
        pass

    def visit_rubric(self, node):
        self.in_rubric = True
        self.cell_to_notebook()

    def depart_rubric(self, node):
        self.cell_to_notebook()
        self.in_rubric = False

    def visit_target(self, node):
        if "refid" in node.attributes:
            self.target_dict['refid'] = node.attributes["refid"]

    def visit_attribution(self, node):
        self.in_attribution = True

    def depart_attribution(self, node):
        self.in_attribution = False

    def visit_caption(self, node):
        self.in_caption = True

    def depart_caption(self, node):
        self.in_caption = False

    def visit_colspec(self, node):
        self.table_builder['column_widths'].append(node['colwidth'])

    def visit_label(self, node):
        if self.footnote_dict['in']:
            ids = node.parent.attributes["ids"]
            id_text = ""
            for id_ in ids:
                id_text += "{} ".format(id_)
            else:
                id_text = id_text[:-1]
            self.footnote_dict['ids'] = node.parent.attributes["ids"]
            self.footnote_dict['id_text'] = id_text


    def visit_block_quote(self, node):
        self.block_quote_dict['in_block_quote'] = True
        if "epigraph" in node.attributes["classes"]:
            self.block_quote_dict['block_quote_type'] = "epigraph"

    def depart_block_quote(self, node):
        if "epigraph" in node.attributes["classes"]:
            self.block_quote_dict['block_quote_type'] = "block-quote"
        self.block_quote_dict['in_block_quote'] = False

    def visit_bullet_list(self, node):
        self.list_dict['list_level'] += 1

    def depart_bullet_list(self, node):
        self.list_dict['list_level'] -= 1

    def visit_citation(self, node):
        self.citation_dict['in'] = True
        if "ids" in node.attributes:
            self.citation_dict['ids'] = node.attributes["ids"]
            id_text = ""
            for id_ in ids:
                id_text += "{} ".format(id_)
            else:
                id_text = id_text[:-1]

            self.citation_dict['id_text'] = id_text

    def depart_citation(self, node):
        self.citation_dict['in'] = False

    def visit_enumerated_list(self, node):
        self.list_dict['list_level'] += 1

    def depart_enumerated_list(self, node):
        self.list_dict['list_level'] -= 1

    def visit_figure(self, node):
        pass
    
    def visit_footnote(self, node):
        self.footnote_dict['in'] = True

    def depart_footnote(self, node):
        self.footnote_dict['in'] = False
    
    def visit_note(self, node):
        self.in_note = True

    def depart_note(self, node):
        self.in_note = False

    def visit_table(self, node):
        self.table_builder = dict()
        self.table_builder['column_widths'] = []
        self.table_builder['lines'] = []
        self.table_builder['line_pending'] = ""

        if 'align' in node:
            self.table_builder['align'] = node['align']
        else:
            self.table_builder['align'] = "center"

    def depart_table(self, node):
        self.table_builder['table_lines'] = "".join(self.table_builder['lines'])

    def visit_entry(self, node):
        pass

    def depart_entry(self, node):
        self.table_builder['line_pending'] += "|"

    def visit_list_item(self, node):

        ## do not add this list item to the list
        if self.list_dict['skip_next_content']:
           self.cell = copy.deepcopy(self.list_dict['initial_lines'])
           self.list_dict['skip_next_content'] = False
        
        ## if we do not want to add the items in this depth to the list
        if self.list_dict['content_depth'] == self.list_dict['content_depth_to_skip']:
           self.list_dict['initial_lines'] = copy.deepcopy(self.cell)
           self.list_dict['skip_next_content'] = True
           self.list_dict['content_depth_to_skip'] = None

           ## only one item in this content depth to remove 
           self.list_dict['content_depth'] -= 1
           return

        ## check if there is a list level
        if not len(self.list_dict['bullets']):
            return
        self.list_dict['in'] = True
        self.list_dict['head'] = "{} ".format(self.list_dict['bullets'][-1])

    def depart_list_item(self, node):
        ## check if there is a list level
        if not len(self.list_dict['list_item_starts']):
            return
        self.list_dict['in'] = False
        self.list_dict['indent'] = self.list_dict['indent_char'] * self.list_dict['indents'][-1]


    def visit_row(self, node):
        self.table_builder['line_pending'] = "|"

    def depart_row(self, node):
        finished_line = self.table_builder['line_pending'] + "\n"
        self.table_builder['lines'].append(finished_line)

    def visit_thead(self, node):
        """ Table Header """
        self.table_builder['current_line'] = 0

    def depart_thead(self, node):
        """ create the header line which contains the alignment for each column """
        header_line = "|"
        for col_width in self.table_builder['column_widths']:
            header_line += self.generate_alignment_line(
                col_width, self.table_builder['align'])
            header_line += "|"

        self.table_builder['lines'].append(header_line + "\n")

    def visit_emphasis(self, node):
        self.cell.append("*")

    def depart_emphasis(self, node):
        self.cell.append("*")

    def visit_footnote_reference(self, node):
        self.footnote_reference['in'] = True
        self.footnote_reference['refid'] = node.attributes['refid']
        self.footnote_reference['ids'] = node.astext()
        if self.config.jupyter_target_pdf:
            self.footnote_reference['link'] = "<sup><a href=#{} id={}-link>[{}]</a></sup>".format(self.footnote_reference['refid'], self.footnote_reference['refid'], self.footnote_reference['ids'])
        else:
            self.footnote_reference['link'] = "<sup>[{}](#{})</sup>".format(self.footnote_reference['ids'], self.footnote_reference['refid'])
        self.cell.append(self.footnote_reference['link'])
        raise nodes.SkipNode

    def depart_footnote_reference(self, node):
        self.footnote_reference['in'] = False
    
    def visit_literal(self, node):
        if self.download_reference_dict['in']:
            return
        self.cell.append("`")

    def depart_literal(self, node):
        if self.download_reference_dict['in']:
            return
        self.cell.append("`")

    def visit_math(self, node):
        """inline math"""

        # With sphinx < 1.8, a math node has a 'latex' attribute, from which the
        # formula can be obtained and added to the text.

        # With sphinx >= 1.8, a math node has no 'latex' attribute, which mean
        # that a flag has to be raised, so that the in visit_Text() we know that
        # we are dealing with a formula.

        try: # sphinx < 1.8
            self.math_dict['math_text'] = node.attributes["latex"].strip()
        except KeyError:
            # sphinx >= 1.8
            self.math_dict['in_math'] = True
            # the flag is raised, the function can be exited.
            self.math_dict['exit'] = True

    def depart_math(self, node):
        self.math_dict['in_math'] = False

    def visit_reference(self, node):
        """anchor link"""
        self.reference_dict['in'] = True

    def depart_reference(self, node):
        subdirectory = False

        if self.in_topic:
            # Jupyter Notebook uses the target text as its id
            uri_text = "".join(
                self.cell[self.reference_dict['reference_text_start']:]).strip()
            uri_text = re.sub(
                self.URI_SPACE_REPLACE_FROM, self.URI_SPACE_REPLACE_TO, uri_text)
            self.reference_dict['uri_text'] = uri_text

        self.reference_dict['in'] = False

    def visit_compact_paragraph(self, node):
        try:
            if node.attributes['toctree']:
                self.in_toctree = True
        except:
            pass  #Should this execute visit_compact_paragragh in BaseTranslator?

    def depart_compact_paragraph(self, node):
        try:
            if node.attributes['toctree']:
                self.in_toctree = False
        except:
            pass

    def visit_download_reference(self, node):
        self.download_reference_dict['in'] = True
        self.download_reference_dict['html'] = "<a href={} download>".format(node["reftarget"])

    def depart_download_reference(self, node):
        self.download_reference_dict['in'] = False

    def visit_only(self, node):
        pass

    def depart_only(self, node):
        pass

    #Document.Nodes
    def visit_Text(self, node):
        text = node.astext()

    def depart_Text(self, node):
        pass

    def visit_exerciselist_node(self, node):
        pass

    def depart_exerciselist_node(self, node):
        pass

    def visit_tgroup(self, node):
        pass

    def depart_tgroup(self, node):
        pass

    def visit_tbody(self, node):
        pass

    def depart_tbody(self, node):
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
        ## default cell type when no cell type is specified
        if not self.cell_type:
            self.cell_type = "markdown"
        source = "".join(self.cell)
        self.output.add_cell(source, self.cell_type)
        self.new_cell()

    def generate_alignment_line(self, line_length, alignment):
        left = ":" if alignment != "right" else "-"
        right = ":" if alignment != "left" else "-"
        return left + "-" * (line_length - 2) + right

     # ================
    # general methods
    # ================
    def add_markdown_cell(self, slide_type="slide", title=False):
        """split a markdown cell here
        * add the slideshow metadata
        * append `markdown_lines` to notebook
        * reset `markdown_lines`
        """
        line_text = "".join(self.cell)
        formatted_line_text = self.strip_blank_lines_in_end_of_block(line_text)
        slide_info = {'slide_type': self.slide}

        if len(formatted_line_text.strip()) > 0:
            new_md_cell = nbformat.v4.new_markdown_cell(formatted_line_text)
            if self.metadata_slide:  # modify the slide metadata on each cell
                new_md_cell.metadata["slideshow"] = slide_info
                self.slide = slide_type
            if title:
                new_md_cell.metadata["hide-input"] = True
            self.cell_type = "markdown"
            self.output.add_cell(new_md_cell, self.cell_type)
            self.cell = []

    @classmethod
    def split_uri_id(cls, uri):
        return re.search(cls.SPLIT_URI_ID_REGEX, uri).groups()

    @classmethod
    def add_extension_to_inline_link(cls, uri, ext):
        if "." not in uri:
            if len(uri) > 0 and uri[0] == "#":
                return uri
            uri, id_ = cls.split_uri_id(uri)
            if len(id_) == 0:
                return "{}{}".format(uri, ext)
            else:
                return "{}{}#{}".format(uri, ext, id_)
        #adjust relative references
        elif "../" in uri:
            # uri = uri.replace("../", "")
            uri, id_ = cls.split_uri_id(uri)
            if len(id_) == 0:
                return "{}{}".format(uri, ext)
            else:
                return "{}{}#{}".format(uri, ext, id_)

        return uri

    @classmethod
    def get_filename(cls,path):
        if "." in path and "/" in path:
            index = path.rfind('/')
            index1 = path.rfind('.')
            return path[index + 1:index1]
        else:
            return path

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