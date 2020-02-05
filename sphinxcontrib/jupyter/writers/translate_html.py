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
        self.urlpath = builder.urlpath
        self.jupyter_download_nb_image_urlpath = builder.jupyter_download_nb_image_urlpath

    #-Nodes-#

    def visit_image(self, node):
        """
        Image Directive
        Include Images as HTML including attributes that  
        are available from the directive
        """
        uri = node.attributes["uri"]
        self.images.append(uri)
        if self.jupyter_download_nb_image_urlpath:
            for file_path in self.jupyter_static_file_path:
                if file_path in uri:
                    uri = uri.replace(file_path +"/", self.jupyter_download_nb_image_urlpath)
                    break  #don't need to check other matches
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

    #References(Start)

    def depart_reference(self, node):
        subdirectory = False

        if self.topic:
            # Jupyter Notebook uses the target text as its id
            uri_text = node.astext().replace(" ","-")
            uri_text = uri_text.replace("(", "%28").replace(")", "%29")
            formatted_text = "](#{})".format(uri_text)
        else:
            # if refuri exists, then it includes id reference
            if "refuri" in node.attributes:
                refuri = node["refuri"]
                # add default extension(.ipynb)
                if "internal" in node.attributes and node.attributes["internal"] == True:
                    refuri = self.add_extension_to_inline_link(refuri, self.html_ext)
                    if self.urlpath is not None:
                        refuri = self.urlpath + refuri
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
            if self.urlpath:
                formatted_text = "]({})".format(self.urlpath + refuri)
            else:
                formatted_text = "]({})".format(refuri)

        if self.toctree:
            formatted_text += "\n"

        ## if there is a list add to it, else add it to the cell directl
        if self.List:
            self.List.add_item(formatted_text)    
        else:
            self.cell.append(formatted_text)

        

    def visit_footnote_reference(self, node):
        self.footnote_reference['in'] = True
        refid = node.attributes['refid']
        ids = node.astext()
        self.footnote_reference['link'] = "<sup><a href=#{} id={}-link>[{}]</a></sup>".format(refid, refid, ids)
        self.cell.append(self.footnote_reference['link'])
        raise nodes.SkipNode

    #References(End)
