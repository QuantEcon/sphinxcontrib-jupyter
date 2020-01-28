"""
Translator to Support IPYNB(HTML) and Website Support
"""

from __future__ import unicode_literals
import re
import nbformat.v4
from docutils import nodes, writers
from shutil import copyfile
import copy
import os

from .translate_ipynb import JupyterIPYNBTranslator
from .utils import JupyterOutputCellGenerators
from .notebook import JupyterNotebook
from .html import HTMLSyntax

class JupyterHTMLTranslator(JupyterIPYNBTranslator):


    def __init__(self, document, builder):
        """ 
        Jupyter Translator for HTML End Target Support

        This will generate IPYNB files emphasis on HTML that are 
        built to work with the `nbconvert` template to support website 
        construction
        """
        super().__init__(document, builder)
        # HTML Settings
        self.html_ext = ".html"
        self.syntax = HTMLSyntax()

    #-Nodes-#

    def visit_attribution(self, node):
        super().visit_attribution(node)

    def visit_block_quote(self, node):
        super().visit_block_quote(node)

    def visit_citation(self, node):
        super().visit_citation(node)

    def depart_citation(self, node):
        self.citation = False

    def visit_definition(self, node):
        self.cell.append(self.syntax.visit_definition())
        self.add_newline()

    def depart_definition(self, node):
        self.cell.append(self.syntax.depart_definition())
        self.add_newline()

    def visit_definition_list(self, node):
        super().visit_definition_list(node)

    def depart_definition_list(self, node):
        super().depart_definition_list(node)

    def visit_image(self, node):
        """
        Notes
        -----
        1. Should this use .has_attrs()?
        2. the scale, height and width properties are not combined in this
        implementation as is done in http://docutils.sourceforge.net/docs/ref/rst/directives.html#image

        """
        uri = node.attributes["uri"]
        self.images.append(uri)
        attrs = node.attributes
        self.cell.append(self.syntax.visit_image(uri, attrs))

    def visit_label(self, node):
        if self.footnote['in']:
            ids = node.parent.attributes["ids"]
            id_text = ""
            for id_ in ids:
                id_text += "{} ".format(id_)
            else:
                id_text = id_text[:-1]

            self.cell.append("<p><a id={} href=#{}-link><strong>[{}]</strong></a> ".format(id_text, id_text, node.astext()))
            raise nodes.SkipNode

        if self.citation['in']:
            self.cell.append(self.syntax.visit_label())

    def depart_label(self, node):
        super().depart_label(node)

    def visit_literal(self, node):
        super().visit_literal(node)

    def depart_literal(self, node):
        super().depart_literal(node)

    def visit_note(self, node):
        super().visit_note(node)

    #References(Start)

    def depart_reference(self, node):
        subdirectory = False

        if self.topic:
            # Jupyter Notebook uses the target text as its id
            uri_text = "".join(
                self.cell[self.reference_text_start:]).strip()
            uri_text = re.sub(
                self.URI_SPACE_REPLACE_FROM, self.URI_SPACE_REPLACE_TO, uri_text)
            uri_text = uri_text.replace("(", "%28")
            uri_text = uri_text.replace(")", "%29")
            self.in_reference['uri_text'] = uri_text
            formatted_text = "](#{})".format(self.reference['uri_text'])
            self.cell.append(formatted_text)
        else:
            # if refuri exists, then it includes id reference
            if "refuri" in node.attributes:
                refuri = node["refuri"]
                # add default extension(.ipynb)
                if "internal" in node.attributes and node.attributes["internal"] == True:
                    refuri = self.add_extension_to_inline_link(refuri, self.html_ext)
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
            if self.List:
                marker = self.List.get_marker()
                text = "]({})".format(refuri)
                self.List.add_item(text)
            else:
                self.cell.append("]({})".format(refuri))

        if self.toctree:
            self.cell.append("\n")

    def visit_footnote_reference(self, node):
        self.footnote_reference['in'] = True
        refid = node.attributes['refid']
        ids = node.astext()
        self.footnote_reference['link'] = "<sup><a href=#{} id={}-link>[{}]</a></sup>".format(refid, refid, ids)
        self.cell.append(self.footnote_reference['link'])
        raise nodes.SkipNode

    #References(End)
