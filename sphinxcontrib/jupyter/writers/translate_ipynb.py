"""
Translators for RST to IPYNB Conversion
"""

from __future__ import unicode_literals
import re
import nbformat.v4
from docutils import nodes, writers
from shutil import copyfile
import copy
import os

from .translate_code import JupyterCodeBlockTranslator
from .utils import JupyterOutputCellGenerators
from .translate import JupyterCodeTranslator
from .markdown import MarkdownSyntax

class JupyterIPYNBTranslator(JupyterCodeTranslator):  #->NEW
    
    #Configuration (Slideshow)
    metadata_slide = False
    slide = "slide"         #TODO: change to slide translator object?

    def __init__(self, document, builder):
        """
        A Jupyter Notebook Translator

        This translator supports the construction of Jupyter notebooks
        with an emphasis on readability. It uses markdown structures
        wherever possible. Notebooks geared towards HTML or PDF are 
        available through JupyterHTMLTranslator, JupyterPDFTranslator
        """
        super().__init__(document, builder)
        #-Markdown-#
        self.md = MarkdownSyntax()

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

    def visit_title(self, node):
        super().visit_title(node)
        if self.in_topic:
            ### this prevents from making it a subsection from section
            self.cell.append("{} ".format("#" * (self.section_level + 1)))
        elif self.table_builder:
            self.cell.append(
                "### {}\n".format(self.title['title']))
        else:
            ### this makes all the sections go up one level to transform subsections to sections
            self.cell.append(
                    "{} ".format("#" * self.section_level))

    def depart_title(self, node):
        if not self.table_builder:
            self.cell.append(self.sep_paragraph)

    def visit_Text(self, node):
        super().visit_Text(node)
        text = node.astext()
        ## removing references from index file book
        if self.in_book_index and 'references' in text.lower():
            return

        #Escape Special markdown chars except in code block
        if self.literal_block['in'] == False:
            text = text.replace("$", "\$")

        if self.math['in']:
            text = '$ {} $'.format(text.strip())
        elif self.math_block['in'] and self.math_block['math_block_label']:
            text = "$$\n{0}{1}$${2}".format(
                        text.strip(), self.math_block['math_block_label'], self.sep_paragraph
                    )
            self.math_block['math_block_label'] = None
        elif self.math_block['in']:
            text = "$$\n{0}\n$${1}".format(text.strip(), self.sep_paragraph)

        if self.literal_block['in']:
            self.cell.append(text)
        elif self.table_builder:
            self.table_builder['line_pending'] += text
        elif self.block_quote['in_block_quote'] or self.in_note:
            if self.block_quote['block_quote_type'] == "epigraph":
                self.cell.append(text.replace("\n", "\n> ")) #Ensure all lines are indented
            else:
                self.cell.append(text)
        elif self.in_caption and self.in_toctree:
            self.cell.append("# {}".format(text))
        else:
            self.cell.append(text)

    def depart_Text(self, node):
        pass

    def visit_image(self, node):
        """
        Notes
        -----
        1. Should this use .has_attrs()?
        2. the scale, height and width properties are not combined in this
        implementation as is done in http://docutils.sourceforge.net/docs/ref/rst/directives.html#image

        """
        super().visit_image(node)
        self.images.append(self.image['uri'])
        self.cell.append(self.image['image'])
    
    def depart_image(self, node):
        pass

    def visit_math_block(self, node):
        """directive math"""
        # visit_math_block is called only with sphinx >= 1.8
        super().visit_math_block(node)

        if self.list_dict['in'] and node["label"]:
            self.cell.pop()  #remove entry \n from table builder

    def depart_math_block(self, node):
        super().depart_math_block(node)

        if self.list_dict['in']:
            self.cell[-1] = self.cell[-1][:-1]  #remove excess \n

    def depart_paragraph(self, node):
        super().depart_paragraph(node)

        if self.list_dict['list_level'] > 0:
            self.cell.append(self.sep_lines)
        elif self.table_builder:
            pass
        elif self.block_quote['block_quote_type'] == "epigraph":
            try:
                attribution = node.parent.children[1]
                self.cell.append("\n>\n")   #Continue block for attribution
            except:
                self.cell.append(self.sep_paragraph)
        else:
            self.cell.append(self.sep_paragraph)

    def visit_rubric(self, node):
        super().visit_rubric(node)

        if len(node.children) == 1 and node.children[0].astext() in ['Footnotes']:
            self.cell.append('**{}**\n\n'.format(node.children[0].astext()))
            raise nodes.SkipNode

    def visit_target(self, node):
        super().visit_target(node)
        self.cell.append("\n<a id='{}'></a>\n".format(self.target['refid']))

    def visit_attribution(self, node):
        super().visit_attribution(node)
        self.cell.append("> ")

    def depart_attribution(self, node):
        super().depart_attribution(node)
        self.cell.append("\n")

    def depart_caption(self, node):
        super().depart_caption(node)
        if self.in_toctree:
            self.cell.append("\n")

    def visit_field_name(self, node):
        self.visit_term(node)

    def depart_field_name(self, node):
        self.depart_term(node)

    def visit_term(self, node):
        self.cell.append("<dt>")

    def depart_term(self, node):
        self.cell.append("</dt>\n")

    def visit_label(self, node):
        super().visit_label(node)
        if self.footnote['in']:
            self.cell.append("<a id='{}'></a>\n**[{}]** ".format(self.footnote['id_text'], node.astext()))
            raise nodes.SkipNode

        if self.citation['in']:
            self.cell.append("\[")

    def depart_label(self, node):
        if self.citation['in']:
            self.cell.append("\] ")

    def visit_block_quote(self, node):
        super().visit_block_quote(node)
        if self.list_dict['in']:               #allow for 4 spaces interpreted as block_quote
            self.cell.append("\n")
            return
        self.cell.append("> ")

    def depart_block_quote(self, node):
        super().depart_block_quote(node)
        self.cell.append("\n")

    def visit_bullet_list(self, node):
        super().visit_bullet_list(node)
        self.list_dict['list_level'] += 1

        # markdown does not have option changing bullet chars
        self.list_dict['bullets'].append("-")
        self.list_dict['indents'].append(len(self.list_dict['bullets'][-1] * 2))  #add two per level


    def depart_bullet_list(self, node):
        super().depart_bullet_list(node)
        if self.list_dict['list_level'] == 0:
            self.cell.append(self.sep_paragraph)
            if self.in_topic:
                self.add_markdown_cell()
        if len(self.list_dict['bullets']):
            self.list_dict['bullets'].pop()
            self.list_dict['indents'].pop()

    def visit_citation(self, node):
        super().visit_citation(node)
        self.cell.append("<a id='{}'></a>\n".format(self.citation['id_text']))

    def visit_definition_list(self, node):
        self.cell.append("\n<dl style='margin: 20px 0;'>\n")

    def depart_definition_list(self, node):
        self.cell.append("\n</dl>{}".format(self.sep_paragraph))

    def visit_enumerated_list(self, node):
        super().visit_enumerated_list(node)

        # markdown does not have option changing bullet chars
        self.list_dict['bullets'].append("1.")
        self.list_dict['indents'].append(len(self.list_dict['bullets'][-1]))

    def depart_enumerated_list(self, node):
        super().depart_enumerated_list(node)
        if self.list_dict['list_level'] == 0:
            self.cell.append(self.sep_paragraph)
        self.list_dict['bullets'].pop()
        self.list_dict['indents'].pop()

    def visit_field_list(self, node):
        self.visit_definition_list(node)

    def depart_field_list(self, node):
        self.depart_definition_list(node)

    def depart_figure(self, node):
        self.cell.append(self.sep_lines)

    def visit_note(self, node):
        super().visit_note(node)
        self.cell.append(">**Note**\n>\n>")

    def visit_table(self, node):
        super().visit_table(node)

    def depart_table(self, node):
        super().depart_table(node)
        self.cell.append(self.table_builder['table_lines'])
        self.table_builder = None

    def visit_definition(self, node):
        self.cell.append("<dd>\n")

    def depart_definition(self, node):
        self.cell.append("</dd>\n")

    def visit_field_body(self, node):
        self.visit_definition(node)

    def depart_field_body(self, node):
        self.depart_definition(node)

    def visit_list_item(self, node):
        super().visit_list_item(node)
        self.cell.append(self.list_dict['head'])
        self.list_dict['list_item_starts'].append(len(self.cell))

    def depart_list_item(self, node):
        super().depart_list_item(node)
        list_item_start = self.list_dict['list_item_starts'].pop()
        br_removed_flag = False

        # remove last breakline
        if self.cell and self.cell[-1][-1] == "\n":
            br_removed_flag = True
            self.cell[-1] = self.cell[-1][:-1]

        for i in range(list_item_start, len(self.cell)):
            self.cell[i] = self.cell[i].replace(
                "\n", "\n{}".format(self.list_dict['indent']))

        # add breakline
        if br_removed_flag:
            self.cell.append("\n")

    def visit_math(self, node):
        super().visit_math(node)
        if 'exit' in self.math and self.math['exit']:
            return

        formatted_text = "$ {} $".format(self.math['math_text'])

        if self.table_builder:
            self.table_builder['line_pending'] += formatted_text
        else:
            self.cell.append(formatted_text)

    def visit_reference(self, node):
        super().visit_reference(node)

        self.cell.append("[")
        self.in_reference['reference_text_start'] = len(self.cell)

    def depart_reference(self, node):
        super().depart_reference(node)

        if self.in_topic:
            formatted_text = "](#{})".format(self.reference['uri_text'])
            self.cell.append(formatted_text)
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
                    self.in_inpage_reference = True
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
            self.cell.append("]({})".format(refuri))

        if self.in_toctree:
            self.cell.append("\n")

    def visit_strong(self, node):
        self.cell.append("**")

    def depart_strong(self, node):
        self.cell.append("**")

    def visit_download_reference(self, node):
        super().visit_download_reference(node)
        self.cell.append(self.download_reference['html'])

    def depart_download_reference(self, node):
        super().depart_download_reference(node)
        self.cell.append("</a>")