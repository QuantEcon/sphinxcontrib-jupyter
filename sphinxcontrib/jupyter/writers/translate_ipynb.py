"""
Translator for RST to IPYNB Conversion
"""

from __future__ import unicode_literals
import re
import nbformat.v4
from docutils import nodes, writers
from shutil import copyfile
import copy
import os

from sphinx.util import logging
from sphinx.util.docutils import SphinxTranslator

from .translate_code import JupyterCodeBlockTranslator
from .utils import JupyterOutputCellGenerators, get_source_file_name
from .notebook import JupyterNotebook
from .markdown import MarkdownSyntax
from .accumulators import List, TableBuilder

logger = logging.getLogger(__name__)

class JupyterIPYNBTranslator(SphinxTranslator):
    
    #Configuration (Attribution)
    attribution = False
    #Configuration (Block Quote)
    block_quote = dict()
    block_quote['in'] = False
    block_quote['block_quote_type'] = "block-quote"      #TODO: can this be removed?
    #Configuration(Caption)
    caption = False
    #Configuration(Citation)
    citation = dict()
    citation['in'] = False
    #Configuration (Download)
    download_reference = dict()
    download_reference['in'] = False
    #Configuration (Formatting)
    sep_lines = "  \n"              #TODO: needed?
    sep_paragraph = "\n\n"          #TODO: needed?
    section_level = 0
    #Configuration (Footnote)
    footnote = dict()
    footnote['in'] = False
    footnote_reference = dict()
    footnote_reference['in'] = False
    #Configuration (File)
    default_ext = ".ipynb"
    #Configuration (Image)
    image = dict()
    #Configuration (List)
    List = None
    #Configuration (Literal Block)
    literal_block = dict()
    literal_block['in'] = False
    literal_block['no-execute'] = False
    #Configuration (Math)
    math = dict()
    math['in'] = False
    math_block = dict()
    math_block['in'] = False
    math_block['math_block_label'] = None
    #Configuration (Note)
    note = False
    #Configuration (References)
    reference_text_start = 0
    inpage_reference = False
    #Configuration (Rubric)
    rubric = False
    #Configuration (Static Assets)
    images = []
    files = []
    #Configuration (Tables)
    Table = None
    #Configuration (Titles)
    visit_first_title = True
    title = ""
    #Configuration (Toctree)
    toctree = False
    #Configuration (Topic)
    topic = False    

    #->Review Options

    remove_next_content = False  #TODO: what is this? PDF
    target = dict()              #TODO: needed?

    # Slideshow option
    metadata_slide = False    #TODO: move to JupyterSlideTranslator
    slide = "slide"           #TODO: move to JupyterSlideTranslator

    cached_state = dict()   #A dictionary to cache states to support nested blocks
    URI_SPACE_REPLACE_FROM = re.compile(r"\s")
    URI_SPACE_REPLACE_TO = "-"

    def __init__(self, document, builder):
        """
        A Jupyter Notebook Translator

        This translator supports the construction of Jupyter notebooks
        with an emphasis on readability. It uses markdown structures
        wherever possible. 
        
        Notebooks geared towards HTML or PDF are available:
          1. JupyterHTMLTranslator, 
          2. JupyterPDFTranslator

        Notes
        -----
        1. A capitalised variable name (i.e. List, Table) are attributes that
           use an accumulator object to assist with constructing the object
        """
        super().__init__(document, builder)
        #-Jupyter Settings-#
        self.language = self.config["jupyter_language"]   #self.language = self.config['highlight_language'] (https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-highlight_language)
        self.language_synonyms = self.config['jupyter_language_synonyms']
        src_dir = self.settings.env.srcdir
        self.source_file_name = self.settings._source.replace(src_dir+"/", "")
        #-Syntax-#
        self.syntax = MarkdownSyntax()

    #-Document-#

    def visit_document(self, node):
        self.output = JupyterNotebook(language=self.language)
        self.new_cell()

    def depart_document(self, node):
        self.output.add_metadata_notebook({"filename": self.source_file_name.split("/")[-1], "title": self.title})
        self.cell_to_notebook()
        #TODO: Should this be in the `builder` (otherwise helper function should be used)
        if len(self.files) > 0:
            for fl in self.files:
                src_fl = os.path.join(self.builder.srcdir, fl)
                out_fl = os.path.join(self.builder.outdir, os.path.basename(fl))   #copy file to same location as notebook (remove dir structure)
                #Check if output directory exists
                out_dir = os.path.dirname(out_fl)
                if not os.path.exists(out_dir):
                    os.makedirs(out_dir)
                print("Copying {} to {}".format(src_fl, out_fl))
                copyfile(src_fl, out_fl)

    #-Nodes-#

    def visit_attribution(self, node):
        self.attribution = True
        self.cell.append(self.syntax.visit_attribution())

    def depart_attribution(self, node):
        self.attribution = False
        self.add_newline()

    def visit_block_quote(self, node):
        self.block_quote['in'] = True
        if "epigraph" in node.attributes["classes"]:
            self.block_quote['block_quote_type'] = "epigraph"
        if self.List:
            self.add_newline()
            return
        self.cell.append(self.syntax.visit_block_quote())

    def depart_block_quote(self, node):
        if "epigraph" in node.attributes["classes"]:
            self.block_quote['block_quote_type'] = "block-quote"
        self.block_quote['in'] = False
        self.add_newline()

    def visit_caption(self, node):
        self.caption = True

    def depart_caption(self, node):
        self.caption = False
        if self.toctree:
            self.cell.append("\n")

    def visit_citation(self, node):
        self.citation['in'] = True
        if "ids" in node.attributes:
            id_text = ""
            for id_ in node.attributes["ids"]:
                id_text += "{} ".format(id_)
            else:
                id_text = id_text[:-1]
        self.cell.append(self.syntax.visit_citation(id_text))

    def depart_citation(self, node):
        self.citation['in'] = False

    def visit_comment(self, node):
        raise nodes.SkipNode

    def visit_compact_paragraph(self, node):
        try:
            if node.attributes['toctree']:
                self.toctree = True
        except:
            pass  #Should this execute visit_compact_paragragh in BaseTranslator?

    def depart_compact_paragraph(self, node):
        try:
            if node.attributes['toctree']:
                self.toctree = False
        except:
            pass

    def visit_compound(self, node):
        pass

    def depart_compound(self, node):
        pass

    def visit_definition(self, node):
        self.cell.append(self.syntax.visit_definition())
        self.add_newline()

    def depart_definition(self, node):
        self.cell.append(self.syntax.depart_definition())
        self.add_newline()

    def visit_definition_list(self, node):
        self.add_newline()
        self.cell.append(self.syntax.visit_definition_list())
        self.add_newline()

    def depart_definition_list(self, node):
        self.add_newline()
        self.cell.append(self.syntax.depart_definition_list())  
        self.add_newparagraph()

    def visit_definition_list_item(self, node):
        pass

    def depart_definition_list_item(self, node):
        pass

    def visit_doctest_block(self, node):
        pass

    def depart_doctest_block(self, node):
        pass

    def visit_figure(self, node):
        pass

    def depart_figure(self, node):
        self.add_newline()

    def visit_field_body(self, node):
        self.visit_definition(node)

    def depart_field_body(self, node):
        self.depart_definition(node)

    def visit_field_list(self, node):
        self.visit_definition_list(node)

    def depart_field_list(self, node):
        self.depart_definition_list(node)
    
    def visit_footnote(self, node):
        self.footnote['in'] = True

    def depart_footnote(self, node):
        self.footnote['in'] = False

    def visit_image(self, node):
        """
        Image Directive

        Notes
        -----
            1. Should this use .has_attrs()?
            2. the scale, height and width properties are not combined in this
            implementation as is done in http://docutils.sourceforge.net/docs/ref/rst/directives.html#image
            3. HTML images are available in HTMLTranslator (TODO: Should this be an available option here?)
        """
        uri = node.attributes["uri"]
        self.images.append(uri)
        self.cell.append(self.syntax.visit_image(uri))
    
    def depart_image(self, node):
        pass

    def visit_index(self, node):
        pass

    def depart_index(self, node):
        pass

    def visit_inline(self, node):
        pass

    def depart_inline(self, node):
        pass
    
    def visit_jupyter_node(self, node):
        try:
            if 'cell-break' in node.attributes:
                self.add_markdown_cell()
            if 'slide' in node.attributes:
                self.metadata_slide = node['slide'] # this activates the slideshow metadata for the notebook
            if 'slide-type' in node.attributes:
                if "fragment" in node['slide-type']:
                    self.add_markdown_cell(slide_type=node['slide-type'])   #start a new cell
                self.slide = node['slide-type'] # replace the default value
        except:
            pass
        #Parse jupyter_dependency directive (TODO: Should this be a separate node type?)
        try:
            self.files.append(node['uri'])
        except:
            pass

    def depart_jupyter_node(self, node):
        if 'cell-break' in node.attributes:
            pass
        if 'slide' in node.attributes:
            pass
        if 'slide-type' in node.attributes:
            pass

    def visit_label(self, node):
        """
        Notes: footnote requires `html` to create links within the 
        notebooks as there is no markdown equivalent 
        """
        if self.footnote['in']:
            ids = node.parent.attributes["ids"]
            id_text = ""
            for id_ in ids:
                id_text += "{} ".format(id_)
            else:
                id_text = id_text[:-1]
            self.cell.append("<a id='{}'></a>\n**[{}]** ".format(id_text, node.astext())) #TODO: can this be harmonized with HTML
            raise nodes.SkipNode

        if self.citation['in']:
            self.cell.append(self.syntax.visit_label())

    def depart_label(self, node):
        if self.citation['in']:
            self.cell.append(self.syntax.depart_label())
            self.add_space()

    def visit_line(self, node):
        pass

    def depart_line(self, node):
        pass

    def visit_line_block(self, node):
        pass

    def depart_line_block(self, node):
        pass

    #List(Start)

    def visit_bullet_list(self, node):
        if not self.List:
            self.List = List(level=0,markers=dict())
        self.List.increment_level()


    def depart_bullet_list(self, node):
        if self.List is not None:
            self.List.decrement_level()
        if self.List and self.List.level == 0:
            markdown = self.List.to_markdown()
            self.cell.append(markdown)
            self.List = None

    def visit_enumerated_list(self, node):
        if not self.List:
            self.List = List(level=0,markers=dict())
        self.List.increment_level()

    def depart_enumerated_list(self, node):
        if self.List is not None:
            self.List.decrement_level()

        if self.List.level == 0:
            markdown = self.List.to_markdown()
            self.cell.append(markdown)
            self.List = None

    def visit_list_item(self, node):
        if self.List:
            self.List.set_marker(node)

    #List(End)

    def visit_literal(self, node):
        if self.download_reference['in']:
            return            #TODO: can we just raise Skipnode?
        if self.List:
            self.List.add_item(self.syntax.visit_literal())
        else:
            self.cell.append(self.syntax.visit_literal())

    def depart_literal(self, node):
        if self.download_reference['in']:
            return
        if self.List:
            self.List.add_item(self.syntax.depart_literal())
        else:
            self.cell.append(self.syntax.depart_literal())

    def visit_literal_block(self, node):
        "Parse Literal Blocks (Code Blocks)"
        self.literal_block['in'] = True

        # Check if inside a list.
        # if in list append the contents till here to the cell, 
        # and make a new cell for code block
        if self.List:
            markdown = self.List.to_markdown()
            self.cell.append(markdown)
            self.cached_state['list_level'] = self.List.getlevel()
            self.cached_state['list_marker'] = self.List.get_marker()
            self.cached_state['list_item_no'] = self.List.get_item_no()
            self.List = None

        #Start new cell and add add current cell to notebook
        self.cell_to_notebook()
        self.new_cell(cell_type = "code")

        #Check Code Language
        if "language" in node.attributes:
            self.nodelang = node.attributes["language"].strip()
        else:
            self.cell_type = "markdown"
        if self.nodelang == 'default':
            self.nodelang = self.language   #use notebook language

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
            self.cell.append(self.syntax.visit_literal_block(self.nodelang))
            self.add_newline()
            self.cell_type = "markdown"


    def depart_literal_block(self, node):
        if (self.nodelang != self.language and self.nodelang not in self.language_synonyms) or self.literal_block['no-execute']:
            self.cell.append(self.syntax.depart_literal_block())
        self.cell_to_notebook()
        #Initialise new cell
        self.new_cell()
        self.literal_block['in'] = False

        ## If this code block was inside a list, then resume the list again just in case there are more items in the list.
        if "list_level" in self.cached_state:
            self.List = List(self.cached_state["list_level"], self.cached_state["list_marker"], self.cached_state["list_item_no"])
            del self.cached_state["list_level"]
            del self.cached_state["list_marker"]
            del self.cached_state["list_item_no"]

    def visit_math(self, node):
        """
        Inline Math
        
        Notes
        -----
        With sphinx < 1.8, a math node has a 'latex' attribute, from which the
        formula can be obtained and added to the text.

        With sphinx >= 1.8, a math node has no 'latex' attribute, which mean
        that a flag has to be raised, so that the in visit_Text() we know that
        we are dealing with a formula.

        TODO:
            1. Deprecate support for sphinx < 1.8
        """
        self.math['in'] = True
        try: # sphinx < 1.8
            math_text = node.attributes["latex"].strip()
        except KeyError:
            # sphinx >= 1.8
            # the flag is raised, the function can be exited.
            return                                              #TODO: raise nodes.SkipNode?

        formatted_text = self.syntax.visit_math(math_text)

        if self.Table:
            self.Table.add_item(formatted_text)
        else:
            self.cell.append(formatted_text)

    def depart_math(self, node):
        self.math['in'] = False

    def visit_math_block(self, node):
        """
        Math from Directives

        Notes:
        ------
        visit_math_block is called only with sphinx >= 1.8
        """
        self.math_block['in'] = True
        #check for labelled math
        if node["label"]:
            #Use \tags in the embedded LaTeX environment
            #Haven't included this in self.syntax.MardownSyntax as it should be general across HTML (mathjax), PDF (latex)
            self.math_block['math_block_label'] = "\\tag{" + str(node["number"]) + "}\n"

    def depart_math_block(self, node):
        self.math_block['in'] = False

    def visit_note(self, node):
        self.note = True
        self.cell.append(self.syntax.visit_note())

    def depart_note(self, node):
        self.note = False

    def visit_only(self, node):
        pass

    def depart_only(self, node):
        pass

    def visit_paragraph(self, node):
        pass

    def depart_paragraph(self, node):
        if self.List:
            pass
        else:
            if self.List and self.List.getlevel() > 0:           #TODO: is this ever reach given above if statement?
                self.add_newline()
            elif self.Table:
                pass
            elif self.block_quote['block_quote_type'] == "epigraph":
                try:
                    attribution = node.parent.children[1]
                    self.cell.append("\n>\n")   #Continue block for attribution
                except:
                    self.add_newparagraph()
            else:
                self.add_newparagraph()

    def visit_raw(self, node):
        pass
    
    def depart_raw(self, node):
        self.add_newparagraph()

    def visit_rubric(self, node):
        self.rubric = True
        self.cell_to_notebook()
        self.new_cell(cell_type="markdown")
        if len(node.children) == 1 and node.children[0].astext() in ['Footnotes']:
            self.cell.append('**{}**\n\n'.format(node.children[0].astext()))            #TODO: add to MarkdownSyntax?
            raise nodes.SkipNode

    def depart_rubric(self, node):
        self.cell_to_notebook()
        self.new_cell(cell_type="markdown")
        self.rubric = False

    def visit_section(self, node):
        self.section_level += 1

    def depart_section(self, node):
        self.section_level -= 1

    #Table(Start)

    def visit_colspec(self, node):
        self.Table.add_column_width(node['colwidth'])

    def visit_entry(self, node):
        pass

    def depart_entry(self, node):
        pass
    
    def visit_row(self, node):
        self.Table.start_row()

    def depart_row(self, node):
        self.Table.end_row()

    def visit_table(self, node):
        self.Table = TableBuilder(node)

    def depart_table(self, node):
        markdown = self.Table.to_markdown()
        self.cell.append(markdown)
        self.Table = None
        self.add_newline()

    def visit_thead(self, node):
        """ Table Header """
        pass

    def depart_thead(self, node):
        """ create the header line which contains the alignment for each column """
        self.Table.add_header_line("|")

    def visit_tgroup(self, node):
        pass

    def depart_tgroup(self, node):
        pass

    def visit_tbody(self, node):
        pass

    def depart_tbody(self, node):
        pass

    #Table(End)

    def visit_target(self, node):
        if "refid" in node.attributes:
            self.cell.append("\n<a id='{}'></a>\n".format(node.attributes["refid"]))

    def depart_target(self, node):
        pass

    #Text(Start)

    def visit_emphasis(self, node):
        self.cell.append(self.syntax.visit_italic())

    def depart_emphasis(self, node):
        self.cell.append(self.syntax.depart_italic())

    def visit_strong(self, node):
        self.cell.append(self.syntax.visit_bold())

    def depart_strong(self, node):
        self.cell.append(self.syntax.depart_bold())

    def visit_Text(self, node):
        text = node.astext()

        #Escape Special markdown chars except in code block
        if self.literal_block['in'] == False:
            text = text.replace("$", "\$")
        #Inline Math
        if self.math['in']:
            text = self.syntax.visit_math(text.strip())
        #Math Blocks
        elif self.math_block['in'] and self.math_block['math_block_label']:
            text = self.syntax.visit_math_block(text.strip(), self.math_block['math_block_label'])
            self.math_block['math_block_label'] = None
        elif self.math_block['in']:
            text = self.syntax.visit_math_block(text.strip())

        #List and Table objects should be updated first. 
        #TODO: Append Text to Cell (Should this be moved to depart_Text?)
        if self.List:
            self.List.add_item(text)
        elif self.Table:
            self.Table.add_item(text)
        elif self.math_block['in']:
            self.cell.append(text)
            self.add_newparagraph()
        elif self.literal_block['in']:
            self.cell.append(text)
        elif self.block_quote['in'] or self.note:
            if self.block_quote['block_quote_type'] == "epigraph":
                self.cell.append(text.replace("\n", "\n> ")) #Ensure all lines are prepended (TODO: should this be in MarkdownSyntax)
            else:
                self.cell.append(text)
        elif self.caption and self.toctree:         #TODO: Check this condition
            self.cell.append("# {}".format(text))
        else:
            self.cell.append(text)

    def depart_Text(self, node):
        pass

    #Text(End)

    def visit_title(self, node):
        if self.visit_first_title:
            self.title = node.astext()
        self.visit_first_title = False
        if self.topic:
            # this prevents from making it a subsection from section
            self.cell.append(self.syntax.visit_title(self.section_level + 1))
            self.add_space()
        elif self.Table:
            self.Table.add_title(node)
        else:
            self.cell.append(self.syntax.visit_title(self.section_level))
            self.add_space()

    def depart_title(self, node):
        if not self.Table:
            self.add_newparagraph()

    def visit_topic(self, node):
        self.topic = True

    def depart_topic(self, node):
        self.topic = False

    #References(Start)

    #TODO: Revisit References to Simplify using Sphinx Internals
    #TODO: add too MarkdownSyntax()

    def visit_reference(self, node):
        self.in_reference = dict()

        if self.List:
            self.List.add_item("[")
            self.reference_text_start = len(self.cell)
        else:
            self.cell.append("[")
            self.reference_text_start = len(self.cell)

    def depart_reference(self, node):
        subdirectory = False
        formatted_text = ""

        if self.topic:
            # Jupyter Notebook uses the target text as its id
            uri_text = node.astext().replace(" ","-")
            formatted_text = "](#{})".format(uri_text)
            #self.cell.append(formatted_text)
        else:
            # if refuri exists, then it includes id reference
            if "refuri" in node.attributes:
                refuri = node["refuri"]
                # add default extension(.ipynb)
                if "internal" in node.attributes and node.attributes["internal"] == True:
                    refuri = self.add_extension_to_inline_link(refuri, self.default_ext)
            else:
                # in-page link
                if "refid" in node:
                    refid = node["refid"]
                    self.inpage_reference = True
                    #markdown doesn't handle closing brackets very well so will replace with %28 and %29
                    #ignore adjustment when targeting pdf as pandoc doesn't parse %28 correctly
                    refid = refid.replace("(", "%28")
                    refid = refid.replace(")", "%29")
                    #markdown target
                    refuri = "#{}".format(refid)
                # error
                else:
                    self.error("Invalid reference")
                    refuri = ""

            #TODO: review if both %28 replacements necessary in this function?
            #      Propose delete above in-link refuri
            #ignore adjustment when targeting pdf as pandoc doesn't parse %28 correctly
            refuri = refuri.replace("(", "%28")  #Special case to handle markdown issue with reading first )
            refuri = refuri.replace(")", "%29")
            formatted_text = "]({})".format(refuri)

        if self.toctree:
            formatted_text += "\n"

        ## if there is a list add to it, else add it to the cell directly
        if self.List:
            self.List.add_item(formatted_text)
        else:
            self.cell.append(formatted_text)

    def visit_title_reference(self, node):
        pass

    def depart_title_reference(self, node):
        pass

    def visit_download_reference(self, node):
        self.download_reference['in'] = True
        html = "<a href={} download>".format(node["reftarget"])
        self.cell.append(html)

    def depart_download_reference(self, node):
        self.download_reference['in'] = False
        self.cell.append("</a>")

    def visit_footnote_reference(self, node):
        self.footnote_reference['in'] = True
        refid = node.attributes['refid']
        ids = node.astext()
        self.footnote_reference['link'] = "<sup>[{}](#{})</sup>".format(ids, refid) #TODO: can this be harmonized with HTML
        self.cell.append(self.footnote_reference['link'])
        raise nodes.SkipNode

    def depart_footnote_reference(self, node):
        self.footnote_reference['in'] = False
    
    #References(End)

    def unknown_visit(self, node):
        raise NotImplementedError('Unknown node: ' + node.__class__.__name__)

    def unknown_departure(self, node):
        pass

    # Nodes (Exercise)
    #TODO: Are these needed (as they are written over by directive in __init__.py?)

    def visit_exercise_node(self, node):
        pass

    def depart_exercise_node(self, node):
        pass

    def visit_exerciselist_node(self, node):
        pass

    def depart_exerciselist_node(self, node):
        pass

    # Nodes (Review if Needed)

    def visit_field_name(self, node):
        self.visit_term(node)

    def depart_field_name(self, node):
        self.depart_term(node)

    def visit_term(self, node):
        self.cell.append("<dt>")

    def depart_term(self, node):
        self.cell.append("</dt>\n")

    #Utilities(Jupyter)

    def new_cell(self, cell_type="markdown"):
        self.cell = []
        self.cell_type = cell_type

    def cell_to_notebook(self):
        if len(self.cell) == 0:
            return
        # Default Cell type if not specified
        if not self.cell_type:
            self.cell_type = "markdown"
        source = "".join(self.cell)
        self.output.add_cell(source, self.cell_type)

    def add_space(self, n=1):
        self.cell.append(" " * n)

    def add_newline(self, n=1):
        self.cell.append("\n" * n)

    def add_newparagraph(self):
        self.cell.append("\n\n")

    #TODO: is this needed?
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
            self.new_cell()

    #Utilities(Formatting)

    @classmethod
    def split_uri_id(cls, uri):                   #TODO: required?
        regex = re.compile(r"([^\#]*)\#?(.*)")
        return re.search(regex, uri).groups()

    @classmethod
    def add_extension_to_inline_link(cls, uri, ext):
        """
        Removes an extension such as `html` and replaces with `ipynb`
        
        .. todo::

            improve implementation for references (looks hardcoded)
        """
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