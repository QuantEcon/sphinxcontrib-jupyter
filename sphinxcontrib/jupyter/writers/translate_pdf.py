"""
Translator to Support PDF / LaTeX Files
"""

from __future__ import unicode_literals
import re
import nbformat.v4
from docutils import nodes, writers
from shutil import copyfile
import copy
import os

from .utils import JupyterOutputCellGenerators
from .translate_ipynb import JupyterIPYNBTranslator
from .pdf import PDFSyntax

class JupyterPDFTranslator(JupyterIPYNBTranslator):
    """ 
    Jupyter Translator for PDF Support

    This will generate IPYNB files emphasis on LaTeX and 
    build to work with the `nbconvert` template to support
    PDF construction
    """

    def __init__(self, document, builder):
        super().__init__(document, builder)
        
        self.in_book_index = False
        self.book_index_previous_links = []
        self.cell_trimmed = []
        self.book_index = self.config["jupyter_pdf_book_index"]
        self.urlpath = builder.urlpath
        self.skip_topic_list_content = True
        self.syntax = PDFSyntax()


    #-Document-#

    def visit_document(self, node):
        """at start
        """
        super().visit_document(node)

        ## if the source file parsed is book index file and target is pdf
        if self.book_index is not None and self.book_index in self.source_file_name:
            self.in_book_index = True

    #-Nodes-#

    def depart_image(self, node):
        self.add_newline()

    # List items

    def visit_bullet_list(self, node):
        #TODO: implement depth to skip and other pdf related things    
        super().visit_bullet_list(node)

    def depart_bullet_list(self, node):
        if self.List is not None:
            self.List.decrement_level()
        if self.List and self.List.level == 0:
            if self.in_book_index:
                markdown = self.List.to_latex()
            else:
                markdown = self.List.to_markdown()
            self.cell.append(markdown)
            self.List = None

    # math

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
            self.math_block['math_block_label'] = " \\tag{" + str(node["number"]) + "}" + "\\label{" + node["ids"][0] + "}\n"

    #Text(Start)

    def visit_Text(self, node):
        text = node.astext()

        ## removing references from index file book
        if self.in_book_index:
            return

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

        #Append Text to Cell (Should this be moved to depart_Text?)
        if self.math_block['in']:
            self.cell.append(text)
            self.add_newparagraph()
        elif self.List:
            self.List.add_item(text)
        elif self.Table:
            self.Table.add_item(text)
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

    #Text(End)

    def depart_raw(self, node):
        for attr in node.attributes:
            if attr == 'format' and node.attributes[attr] == 'html':
                self.new_cell()
                return
        self.add_newparagraph()

    #References(Start)

    #TODO: Revisit References to Simplify using Sphinx Internals
    #TODO: add too MarkdownSyntax()

    def visit_reference(self, node):

        if self.in_book_index and node.attributes['refuri'] == 'zreferences':
            return

        if self.topic and self.skip_topic_list_content:
            self.skip_topic_list_content = False
            self.List.decrement_level()
            raise nodes.SkipNode

        self.in_reference = dict()

        if self.List:
            marker = self.List.get_marker()
            if not self.in_book_index and not self.topic:
                self.List.add_item("[")
        else:
            self.cell.append("[")

    def depart_reference(self, node):
        subdirectory = False
        formatted_text = ""

        ## removing zreferences from the index file
        if self.in_book_index and node.attributes['refuri'] == 'zreferences':
            return

        if self.topic:
            # Jupyter Notebook uses the target text as its id
            uri_text = node.astext().replace(" ","-").lower()
            SPECIALCHARS = [r"!", r"@", r"#", r"$", r"%", r"^", r"&", r"*", r"(", r")", r"[", r"]", r"{", 
                            r"}", r"|", r":", r";", r",", r"?", r"'", r"’", r"–", r"`"]
            for CHAR in SPECIALCHARS:
                uri_text = uri_text.replace(CHAR,"")
                uri_text = uri_text.replace("--","-")
                uri_text = uri_text.replace(".-",".")
            formatted_text = " \\ref{" + uri_text + "}" #Use Ref and Plain Text titles
        else:
            # if refuri exists, then it includes id reference
            if "refuri" in node.attributes:
                refuri = node["refuri"]
                # add default extension(.ipynb)
                if "internal" in node.attributes and node.attributes["internal"] == True:
                    #TODO: cross check this if else condition again with translate_all
                    if 'references#' in refuri:
                        label = refuri.split("#")[-1]
                        bibtex = self.cell.pop()
                        if len(self.cell) > 1 and "hyperlink" in self.cell[-1]:
                            self.cell.pop()
                        refuri = "reference-\\cite{" + label
                        self.add_bib_to_latex(self.output, True)
                    elif 'references' not in refuri:
                        if len(self.source_file_name.split('/')) >= 2 and self.source_file_name.split('/')[-2] and 'rst' not in self.source_file_name.split('/')[-2]:
                            subdirectory = self.source_file_name.split('/')[-2]
                        if subdirectory: refuri = subdirectory + "/" + refuri
                        hashIndex = refuri.rfind("#")
                        if hashIndex > 0:
                            refuri = refuri[0:hashIndex] + ".html" + refuri[hashIndex:]
                        else:
                            refuri = refuri + ".html"
                        if self.urlpath:
                            formatted_text = "]({})".format(self.urlpath + refuri)
                        else:
                            formatted_text = "]({})".format(refuri)
                    else:
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
            #TODO: show these checks while pushing to list as well?
            if 'reference-' in refuri:
                formatted_text = refuri.replace("reference-","") + "}"
            elif "refuri" in node.attributes and "internal" in node.attributes and node.attributes["internal"] == True and "references" not in node["refuri"]:
                ##### Below code, constructs an index file for the book
                if self.in_book_index:
                    if self.List.level > 1:
                        # if it is not the top level, then probably it is a chapter
                        formatted_text = "\\chapter{{{}}}\\input{{{}}}".format(node.astext(), node["refuri"] + ".tex")
                    else:
                        formatted_text = "\\cleardoublepage\\part{{{}}}".format(node.astext())

            elif "refuri" in node.attributes and "http" in node["refuri"]:
                ### handling extrernal links
                formatted_text = "]({})".format(refuri)
            elif self.inpage_reference:
                labeltext = self.cell.pop()
                # Check for Equations as they do not need labetext
                if 'equation-' in refuri:
                    formatted_text = refuri + "}"
                else:
                    formatted_text = refuri + "}{" + labeltext + "}"

                # if self.in_toctree:
                #     #TODO: this will become an internal link when making a single unified latex file
                #     formatted_text = " \\ref{" + refuri + "}"
                #     self.cell.append(formatted_text)

        if self.toctree:
            formatted_text += "\n"

        ## if there is a list add to it, else add it to the cell directly        
        if self.List:
            marker = self.List.get_marker()
            self.List.add_item(formatted_text)
        else:
            self.cell.append(formatted_text)

    #References(End)

    def visit_target(self, node):
        if "refid" in node.attributes:
            refid = node.attributes["refid"]
            if 'equation' in refid:
                #no html targets when computing notebook to target pdf in labelled math
                pass
            else:
                #set hypertargets for non math targets
                if self.cell:
                    self.cell.append("\n\\hypertarget{" + refid + "}{}\n\n")

    def visit_title(self, node):
        ### to remove the main title from ipynb as they are already added by metadata
        if self.section_level == 1 and not self.topic:
            return

        if self.visit_first_title:
            title = node.astext()
        self.visit_first_title = False

        if self.topic:
            # this prevents from making it a subsection from section
            if self.section_level == 1:
                self.cell.append(self.syntax.visit_title(self.section_level))
            else:
                self.cell.append(self.syntax.visit_title(self.section_level + 1))
            self.add_space()
        elif self.Table:
            self.Table.add_title(node)
        else:
            # this makes all the sections go up one level to transform subsections to sections
            self.cell.append(self.syntax.visit_title(self.section_level - 1))
            self.add_space()

    def depart_title(self, node):
        if not self.Table:
            if self.section_level == 1 and not self.topic:
                self.new_cell()
                return
            self.add_newparagraph()

    @classmethod
    def add_bib_to_latex(self, nb, boolean):
        ## add bib include value to the latex metadata object
        latex_metadata = nb.get_metadata('latex_metadata', {})

        latex_metadata['bib_include'] = boolean
        nb.add_metadata_notebook(latex_metadata)



