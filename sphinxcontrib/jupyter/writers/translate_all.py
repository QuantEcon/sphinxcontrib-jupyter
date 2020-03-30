from __future__ import unicode_literals
import re
import nbformat.v4
from docutils import nodes, writers
from .translate_code import JupyterCodeTranslator
from .utils import JupyterOutputCellGenerators
from shutil import copyfile
import copy
import os


class JupyterTranslator(JupyterCodeTranslator, object):
    """ Jupyter Translator for Text and Code
    """

    SPLIT_URI_ID_REGEX = re.compile(r"([^\#]*)\#?(.*)")

    def __init__(self, builder, document):
        super(JupyterTranslator, self).__init__(builder, document)

        # Settings
        self.sep_lines = "  \n"
        self.sep_paras = "\n\n"
        self.indent_char = " "
        self.indent = self.indent_char * 4
        self.default_ext = ".ipynb"
        self.html_ext = ".html"
        self.urlpath = builder.urlpath
        # Variables used in visit/depart
        self.in_code_block = False  # if False, it means in markdown_cell
        self.in_block_quote = False
        self.block_quote_type = "block-quote"
        self.in_note = False
        self.in_attribution = False
        self.in_rubric = False
        self.in_footnote = False
        self.in_footnote_reference = False
        self.in_download_reference = False
        self.in_inpage_reference = False
        self.in_caption = False
        self.in_toctree = False
        self.in_list = False
        self.in_math = False
        self.in_math_block = False

        self.code_lines = []
        self.markdown_lines = []

        self.indents = []
        self.section_level = 0
        self.bullets = []
        self.list_item_starts = []
        self.in_topic = False
        self.reference_text_start = 0
        self.in_reference = False
        self.list_level = 0
        self.skip_next_content = False
        self.content_depth = self.jupyter_pdf_showcontentdepth
        self.content_depth_to_skip = None
        self.remove_next_content = False
        self.in_citation = False
        self.math_block_label = None

        self.images = []
        self.files = []
        self.table_builder = None

        # Slideshow option
        self.metadata_slide = False  #False is the value by default for all the notebooks
        self.slide = "slide" #value by default
        
        ## pdf book options
        self.in_book_index = False
        self.book_index_previous_links = []
        self.markdown_lines_trimmed = []


    # specific visit and depart methods
    # ---------------------------------

    def visit_document(self, node):
        """at start
        """
        JupyterCodeTranslator.visit_document(self, node)

        ## if the source file parsed is book index file and target is pdf
        if self.book_index is not None and self.book_index in self.source_file_name and self.jupyter_pdf_book:
            self.in_book_index = True




    def depart_document(self, node):
        """at end
        Almost the exact same implementation as that of the superclass.


        Notes
        -----
        [1] if copyfile is not graceful should catch exception if file not found / issue warning in sphinx
        [2] should this be moved to CodeTranslator for support files when producing code only notebooks?
        """
        self.add_markdown_cell()
        #Parse .. jupyter-dependency::
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
        JupyterCodeTranslator.depart_document(self, node)
    
    # =========
    # Sections
    # =========

    def visit_only(self, node):
        pass

    def depart_only(self, node):
        pass

    def visit_topic(self, node):
        self.in_topic = True

    def depart_topic(self, node):
        self.in_topic = False

    def visit_section(self, node):
        self.section_level += 1

    def depart_section(self, node):
        self.section_level -= 1

    #=================
    # Inline elements
    #=================
    def visit_Text(self, node):

        text = node.astext()

        ## removing references from index file book
        if self.in_book_index and 'references' in text.lower():
            return

        #Escape Special markdown chars except in code block
        if self.in_code_block == False:
            text = text.replace("$", "\$")

        if self.in_math:
            if self.jupyter_target_pdf:
                text = '${}$'.format(text.strip())  #must remove spaces between $ and math for latex
            else:
                text = '$ {} $'.format(text.strip())
        elif self.in_math_block and self.math_block_label:
            text = "$$\n{0}{1}$${2}".format(
                        text.strip(), self.math_block_label, self.sep_paras
                    )
            self.math_block_label = None
        elif self.in_math_block:
            text = "$$\n{0}\n$${1}".format(text.strip(), self.sep_paras)

        if self.in_code_block:
            self.code_lines.append(text)
        elif self.table_builder:
            self.table_builder['line_pending'] += text
        elif self.in_block_quote or self.in_note:
            if self.block_quote_type == "epigraph":
                self.markdown_lines.append(text.replace("\n", "\n> ")) #Ensure all lines are indented
            else:
                self.markdown_lines.append(text)
        elif self.in_caption and self.in_toctree:
            self.markdown_lines.append("# {}".format(text))
        else:
            self.markdown_lines.append(text)

    def depart_Text(self, node):
        pass

    def visit_attribution(self, node):
        self.in_attribution = True
        self.markdown_lines.append("> ")

    def depart_attribution(self, node):
        self.in_attribution = False
        self.markdown_lines.append("\n")

    # image
    def visit_image(self, node):
        """
        Notes
        -----
        1. Should this use .has_attrs()?
        2. the scale, height and width properties are not combined in this
        implementation as is done in http://docutils.sourceforge.net/docs/ref/rst/directives.html#image

        """
        ### preventing image from the index file at the moment
        if self.in_book_index:
            return
        uri = node.attributes["uri"]
        self.images.append(uri)             #TODO: list of image files
        if self.jupyter_download_nb_image_urlpath:
            for file_path in self.jupyter_static_file_path:
                if file_path in uri:
                    uri = uri.replace(file_path +"/", self.jupyter_download_nb_image_urlpath)
                    break  #don't need to check other matches
        attrs = node.attributes
        if self.jupyter_images_markdown:
            #-Construct MD image
            image = "![{0}]({0})".format(uri)
        else:
            # Construct HTML image
            image = '<img src="{}" '.format(uri)
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
        self.markdown_lines.append(image)
    
    def depart_image(self, node):
        if self.jupyter_target_pdf:
            self.markdown_lines.append("\n")

    # math
    def visit_math(self, node):
        """inline math"""

        # With sphinx < 1.8, a math node has a 'latex' attribute, from which the
        # formula can be obtained and added to the text.

        # With sphinx >= 1.8, a math node has no 'latex' attribute, which mean
        # that a flag has to be raised, so that the in visit_Text() we know that
        # we are dealing with a formula.

        try: # sphinx < 1.8
            math_text = node.attributes["latex"].strip()
        except KeyError:
            # sphinx >= 1.8
            self.in_math = True

            # the flag is raised, the function can be exited.
            return

        if self.jupyter_target_pdf:
            formatted_text = "${}$".format(math_text) #must remove spaces between $ and math for latex
        else:
            formatted_text = "$ {} $".format(math_text)

        if self.table_builder:
            self.table_builder['line_pending'] += formatted_text
        else:
            self.markdown_lines.append(formatted_text)

    def depart_math(self, node):
        self.in_math = False

    def visit_displaymath(self, node):
        """directive math"""
        # displaymath is called with sphinx < 1.8 only

        math_text = node.attributes["latex"].strip()

        if self.in_list and node["label"]:
            self.markdown_lines.pop()  #remove entry \n from table builder

        if self.list_level == 0:
            formatted_text = "$$\n{0}\n$${1}".format(
                math_text, self.sep_paras)
        else:
            formatted_text = "$$\n{0}\n$${1}".format(
                math_text, self.sep_paras)

        #check for labelled math
        if node["label"]:
            #Use \tags in the LaTeX environment
            if self.jupyter_target_pdf:
                if "ids" in node and len(node["ids"]):
                    #pdf should have label following tag and removed html id tags in visit_target
                    referenceBuilder = " \\tag{" + str(node["number"]) + "}" + "\\label{" + node["ids"][0] + "}\n"
            else:
                referenceBuilder = " \\tag{" + str(node["number"]) + "}\n"                  #node["ids"] should always exist for labelled displaymath
            formatted_text = formatted_text.rstrip("$$\n") + referenceBuilder + "$${}".format(self.sep_paras)

        self.markdown_lines.append(formatted_text)

    def depart_displaymath(self, node):
        if self.in_list:
            self.markdown_lines[-1] = self.markdown_lines[-1][:-1]  #remove excess \n

    def visit_math_block(self, node):
        """directive math"""
        # visit_math_block is called only with sphinx >= 1.8

        self.in_math_block = True

        if self.in_list and node["label"]:
            self.markdown_lines.pop()  #remove entry \n from table builder

        #check for labelled math
        if node["label"]:
            #Use \tags in the LaTeX environment
            if self.jupyter_target_pdf:
                if "ids" in node and len(node["ids"]):
                    #pdf should have label following tag and removed html id tags in visit_target
                    referenceBuilder = " \\tag{" + str(node["number"]) + "}" + "\\label{" + node["ids"][0] + "}\n"
            else:
                referenceBuilder = " \\tag{" + str(node["number"]) + "}\n"
            #node["ids"] should always exist for labelled displaymath
            self.math_block_label = referenceBuilder

    def depart_math_block(self, node):
        if self.in_list:
            self.markdown_lines[-1] = self.markdown_lines[-1][:-1]  #remove excess \n

        self.in_math_block = False

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
        table_lines = "".join(self.table_builder['lines'])
        self.markdown_lines.append(table_lines)
        self.table_builder = None

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

    def generate_alignment_line(self, line_length, alignment):
        left = ":" if alignment != "right" else "-"
        right = ":" if alignment != "left" else "-"
        return left + "-" * (line_length - 2) + right

    def visit_colspec(self, node):
        self.table_builder['column_widths'].append(node['colwidth'])

    def visit_row(self, node):
        self.table_builder['line_pending'] = "|"

    def depart_row(self, node):
        finished_line = self.table_builder['line_pending'] + "\n"
        self.table_builder['lines'].append(finished_line)

    def visit_entry(self, node):
        pass

    def depart_entry(self, node):
        self.table_builder['line_pending'] += "|"

    def visit_raw(self, node):
        pass


    def visit_rubric(self, node):
        self.in_rubric = True
        self.add_markdown_cell()
        if len(node.children) == 1 and node.children[0].astext() in ['Footnotes']:
            self.markdown_lines.append('**{}**\n\n'.format(node.children[0].astext()))
            raise nodes.SkipNode

    def depart_rubric(self, node):
        self.add_markdown_cell()
        self.in_rubric = False

    def visit_footnote_reference(self, node):
        self.in_footnote_reference = True
        refid = node.attributes['refid']
        ids = node.astext()
        if self.jupyter_target_html:
            link = "<sup><a href=#{} id={}-link>[{}]</a></sup>".format(refid, refid, ids)
        else:
            link = "<sup>[{}](#{})</sup>".format(ids, refid)
        self.markdown_lines.append(link)
        raise nodes.SkipNode

    def depart_footnote_reference(self, node):
        self.in_footnote_reference = False

    def visit_footnote(self, node):
        self.in_footnote = True

    def depart_footnote(self, node):
        self.in_footnote = False

    def visit_download_reference(self, node):
        self.in_download_reference = True
        html = "<a href={} download>".format(node["reftarget"])
        self.markdown_lines.append(html)

    def depart_download_reference(self, node):
        self.markdown_lines.append("</a>")
        self.in_download_reference = False

    #================
    # markdown cells
    #================

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

    # title(section)
    def visit_title(self, node):
        JupyterCodeTranslator.visit_title(self, node)

        ### to remove the main title from ipynb as they are already added by metadata
        if self.jupyter_target_pdf and self.section_level == 1 and not self.in_topic:
            return
        else:
            self.add_markdown_cell()
        if self.in_topic:
            ### this prevents from making it a subsection from section
            if self.jupyter_target_pdf and self.section_level == 1:
                self.markdown_lines.append(
                    "{} ".format("#" * (self.section_level)))
            else:
                self.markdown_lines.append(
                    "{} ".format("#" * (self.section_level + 1)))
        elif self.table_builder:
            self.markdown_lines.append(
                "### {}\n".format(node.astext()))
        else:
            ### this makes all the sections go up one level to transform subsections to sections
            if self.jupyter_target_pdf:
                self.markdown_lines.append(
                "{} ".format("#" * (self.section_level -1)))
            else:
                self.markdown_lines.append(
                    "{} ".format("#" * self.section_level))

    def depart_title(self, node):
        if not self.table_builder:

            ### to remove the main title from ipynb as they are already added by metadata
            if self.jupyter_target_pdf and self.section_level == 1 and not self.in_topic:
                self.markdown_lines = []
                return
            self.markdown_lines.append(self.sep_paras)

    # emphasis(italic)
    def visit_emphasis(self, node):
        self.markdown_lines.append("*")

    def depart_emphasis(self, node):
        self.markdown_lines.append("*")

    # strong(bold)
    def visit_strong(self, node):
        self.markdown_lines.append("**")

    def depart_strong(self, node):
        self.markdown_lines.append("**")

    def visit_literal(self, node):
        if self.in_download_reference:
            return
        self.markdown_lines.append("`")

    def depart_literal(self, node):
        if self.in_download_reference:
            return
        self.markdown_lines.append("`")

    # figures
    def visit_figure(self, node):
        pass

    def depart_figure(self, node):
        self.markdown_lines.append(self.sep_lines)

    # reference
    def visit_reference(self, node):
        """anchor link"""
        ## removing zreferences from the index file
        if self.in_book_index and node.attributes['refuri'] == 'zreferences':
            return

        self.in_reference = True
        if self.jupyter_target_pdf:
            if "refuri" in node and "http" in node["refuri"]:
                self.markdown_lines.append("[")
            elif "refid" in node:
                if 'equation-' in node['refid']:
                    self.markdown_lines.append("\eqref{")
                elif self.in_topic:
                    pass
                else:
                    self.markdown_lines.append("\hyperlink{")
            elif "refuri" in node and 'references#' not in node["refuri"]:
                self.markdown_lines.append("[")
            else:
                self.markdown_lines.append("\hyperlink{")
        else:
            self.markdown_lines.append("[")
        self.reference_text_start = len(self.markdown_lines)

    def depart_reference(self, node):
        subdirectory = False

        ## removing zreferences from the index file
        if self.in_book_index and node.attributes['refuri'] == 'zreferences':
            return

        if self.in_topic:
            # Jupyter Notebook uses the target text as its id
            uri_text = "".join(
                self.markdown_lines[self.reference_text_start:]).strip()
            uri_text = re.sub(
                self.URI_SPACE_REPLACE_FROM, self.URI_SPACE_REPLACE_TO, uri_text)
            if self.jupyter_target_html:
                #Adjust contents (toc) text when targetting html to prevent nbconvert from breaking html on )
                uri_text = uri_text.replace("(", "%28")
                uri_text = uri_text.replace(")", "%29")
            #Format end of reference in topic
            if self.jupyter_target_pdf:
                uri_text = uri_text.lower()
                SPECIALCHARS = [r"!", r"@", r"#", r"$", r"%", r"^", r"&", r"*", r"(", r")", r"[", r"]", r"{", 
                                r"}", r"|", r":", r";", r",", r"?", r"'", r"’", r"–", r"`"]
                for CHAR in SPECIALCHARS:
                    uri_text = uri_text.replace(CHAR,"")
                    uri_text = uri_text.replace("--","-")
                    uri_text = uri_text.replace(".-",".")
                formatted_text = " \\ref{" + uri_text + "}" #Use Ref and Plain Text titles
            else:
                formatted_text = "](#{})".format(uri_text)
            self.markdown_lines.append(formatted_text)
        else:
            # if refuri exists, then it includes id reference(#hoge)
            if "refuri" in node.attributes:
                refuri = node["refuri"]
                # add default extension(.ipynb)
                if "internal" in node.attributes and node.attributes["internal"] == True:
                    if self.jupyter_target_html:
                        refuri = self.add_extension_to_inline_link(refuri, self.html_ext)
                        ## add url path if it is set
                        if self.urlpath is not None:
                            refuri = self.urlpath + refuri
                    elif self.jupyter_target_pdf and 'references#' in refuri:
                        label = refuri.split("#")[-1]
                        bibtex = self.markdown_lines.pop()
                        if "hyperlink" in self.markdown_lines[-1]:
                            self.markdown_lines.pop()
                        refuri = "reference-\\cite{" + label
                        self.add_bib_to_latex(self.output, True)
                    elif self.jupyter_target_pdf and 'references' not in refuri:
                        if self.source_file_name.split('/')[-2] and 'rst' not in self.source_file_name.split('/')[-2]:
                            subdirectory = self.source_file_name.split('/')[-2]
                        if subdirectory: refuri = subdirectory + "/" + refuri
                        hashIndex = refuri.rfind("#")
                        if hashIndex > 0:
                            refuri = refuri[0:hashIndex] + ".html" + refuri[hashIndex:]
                        else:
                            refuri = refuri + ".html"
                        if self.urlpath:
                            self.markdown_lines.append("]({})".format(self.urlpath + refuri))
                        else:
                            self.markdown_lines.append("]({})".format(refuri))
                    else:
                        refuri = self.add_extension_to_inline_link(refuri, self.default_ext)
            else:
                # in-page link
                if "refid" in node:
                    refid = node["refid"]
                    self.in_inpage_reference = True
                    if not self.jupyter_target_pdf:
                        #markdown doesn't handle closing brackets very well so will replace with %28 and %29
                        #ignore adjustment when targeting pdf as pandoc doesn't parse %28 correctly
                        refid = refid.replace("(", "%28")
                        refid = refid.replace(")", "%29")
                    if self.jupyter_target_pdf:
                        refuri = refid
                    else:
                        #markdown target
                        refuri = "#{}".format(refid)
                # error
                else:
                    self.error("Invalid reference")
                    refuri = ""

            #TODO: review if both %28 replacements necessary in this function?
            #      Propose delete above in-link refuri
            if not self.jupyter_target_pdf:
                #ignore adjustment when targeting pdf as pandoc doesn't parse %28 correctly
                refuri = refuri.replace("(", "%28")  #Special case to handle markdown issue with reading first )
                refuri = refuri.replace(")", "%29")
            if self.jupyter_target_pdf and 'reference-' in refuri:
                self.markdown_lines.append(refuri.replace("reference-","") + "}")
            elif "refuri" in node.attributes and self.jupyter_target_pdf and "internal" in node.attributes and node.attributes["internal"] == True and "references" not in node["refuri"]:
                ##### Below code, constructs an index file for the book
                if self.in_book_index:
                    if self.markdown_lines_trimmed != [] and (all(x in self.markdown_lines for x in self.markdown_lines_trimmed)): 
                        ### when the list is not empty and when the list contains chapters or heading from the topic already
                        self.markdown_lines_trimmed = self.markdown_lines[len(self.book_index_previous_links) + 2:] ### +2 to preserve '/n's
                        if '- ' in self.markdown_lines[len(self.book_index_previous_links) + 1:]:
                            text = "\\chapter{{{}}}\\input{{{}}}".format(node.astext(), node["refuri"] + ".tex")
                        else:
                            text = "\\cleardoublepage\\part{{{}}}".format(node.astext())
                        self.markdown_lines = self.markdown_lines[:len(self.markdown_lines) - len(self.markdown_lines_trimmed)]
                        self.markdown_lines.append(text)
                        self.markdown_lines_trimmed = []
                        self.markdown_lines_trimmed.append(text)
                    else:
                        ### when the list is empty the first entry is the topic
                        text = "\\cleardoublepage\\part{{{}}}".format(node.astext())
                        self.markdown_lines = []
                        self.markdown_lines.append(text)
                        self.markdown_lines_trimmed = copy.deepcopy(self.markdown_lines)
                    self.book_index_previous_links = copy.deepcopy(self.markdown_lines)

                    ## check to remove any '- ' left behind during the above operation
                    if "- " in self.markdown_lines:
                        self.markdown_lines.remove("- ")

            elif "refuri" in node.attributes and self.jupyter_target_pdf and "http" in node["refuri"]:
                ### handling extrernal links
                self.markdown_lines.append("]({})".format(refuri))
                #label = self.markdown_lines.pop()
                # if "\href{" == label:  #no label just a url
                #     self.markdown_lines.append(label + "{" + refuri + "}")
                # else:
                #     self.markdown_lines.append(refuri + "}" + "{" + label + "}")
            elif self.jupyter_target_pdf and self.in_inpage_reference:
                labeltext = self.markdown_lines.pop()
                # Check for Equations as they do not need labetext
                if 'equation-' in refuri:
                    self.markdown_lines.append(refuri + "}")
                else:
                    self.markdown_lines.append(refuri + "}{" + labeltext + "}")
            # if self.jupyter_target_pdf and self.in_toctree:
            #     #TODO: this will become an internal link when making a single unified latex file
            #     formatted_text = " \\ref{" + refuri + "}"
            #     self.markdown_lines.append(formatted_text)
            else:
                self.markdown_lines.append("]({})".format(refuri))

        if self.in_toctree:
            self.markdown_lines.append("\n")

        self.in_reference = False

    # target: make anchor
    def visit_target(self, node):
        if "refid" in node.attributes:
            refid = node.attributes["refid"]
            if self.jupyter_target_pdf:
                if 'equation' in refid:
                    #no html targets when computing notebook to target pdf in labelled math
                    pass
                else:
                    #set hypertargets for non math targets
                    if self.markdown_lines:
                        self.markdown_lines.append("\n\\hypertarget{" + refid + "}{}\n\n")
            else:
                self.markdown_lines.append("\n<a id='{}'></a>\n".format(refid))

    # list items
    def visit_bullet_list(self, node):
        ## trying to return if it is in the topmost depth and it is more than 1
        if self.jupyter_target_pdf and (self.content_depth == self.jupyter_pdf_showcontentdepth) and self.content_depth > 1:
            self.content_depth_to_skip = self.content_depth
            self.initial_lines = []
            return

        self.list_level += 1

        # markdown does not have option changing bullet chars
        self.bullets.append("-")
        self.indents.append(len(self.bullets[-1] * 2))  #add two per level

    def depart_bullet_list(self, node):
        self.list_level -= 1
        if self.list_level == 0:
            self.markdown_lines.append(self.sep_paras)
            if self.in_topic:
                self.add_markdown_cell()
        if len(self.bullets):
            self.bullets.pop()
            self.indents.pop()
        

    def visit_enumerated_list(self, node):
        self.list_level += 1
        # markdown does not have option changing bullet chars
        self.bullets.append("1.")
        self.indents.append(len(self.bullets[-1]))

    def depart_enumerated_list(self, node):
        self.list_level -= 1
        if self.list_level == 0:
            self.markdown_lines.append(self.sep_paras)
        if len(self.bullets):
            self.bullets.pop()
            self.indents.pop()

    def visit_list_item(self, node):

        ## do not add this list item to the list
        if self.skip_next_content is True:
           self.markdown_lines = copy.deepcopy(self.initial_lines)
           self.skip_next_content = False
        
        ## if we do not want to add the items in this depth to the list
        if self.content_depth == self.content_depth_to_skip:
           self.initial_lines = copy.deepcopy(self.markdown_lines)
           self.skip_next_content = True
           self.content_depth_to_skip = None

           ## only one item in this content depth to remove 
           self.content_depth -= 1
           return

        ## check if there is a list level
        if not len(self.bullets):
            return
        self.in_list = True
        head = "{} ".format(self.bullets[-1])
        self.markdown_lines.append(head)
        self.list_item_starts.append(len(self.markdown_lines))

    def depart_list_item(self, node):
        ## check if there is a list level
        if not len(self.list_item_starts):
            return
        self.in_list = False
        list_item_start = self.list_item_starts.pop()
        indent = self.indent_char * self.indents[-1]
        br_removed_flag = False

        # remove last breakline
        if self.markdown_lines and self.markdown_lines[-1][-1] == "\n":
            br_removed_flag = True
            self.markdown_lines[-1] = self.markdown_lines[-1][:-1]

        for i in range(list_item_start, len(self.markdown_lines)):
            self.markdown_lines[i] = self.markdown_lines[i].replace(
                "\n", "\n{}".format(indent))

        # add breakline
        if br_removed_flag:
            self.markdown_lines.append("\n")

    # definition list
    def visit_definition_list(self, node):
        self.markdown_lines.append("\n<dl style='margin: 20px 0;'>\n")

    def depart_definition_list(self, node):
        self.markdown_lines.append("\n</dl>{}".format(self.sep_paras))

    def visit_term(self, node):
        self.markdown_lines.append("<dt>")

    def depart_term(self, node):
        self.markdown_lines.append("</dt>\n")

    def visit_definition(self, node):
        self.markdown_lines.append("<dd>\n")

    def depart_definition(self, node):
        self.markdown_lines.append("</dd>\n")

    # field list
    def visit_field_list(self, node):
        self.visit_definition_list(node)

    def depart_field_list(self, node):
        self.depart_definition_list(node)

    def visit_field_name(self, node):
        self.visit_term(node)

    def depart_field_name(self, node):
        self.depart_term(node)

    def visit_field_body(self, node):
        self.visit_definition(node)

    def depart_field_body(self, node):
        self.depart_definition(node)

    # citation
    def visit_citation(self, node):
        self.in_citation = True
        if "ids" in node.attributes:
            ids = node.attributes["ids"]
            id_text = ""
            for id_ in ids:
                id_text += "{} ".format(id_)
            else:
                id_text = id_text[:-1]

            self.markdown_lines.append(
                "<a id='{}'></a>\n".format(id_text))

    def depart_citation(self, node):
        self.in_citation = False

    # label
    def visit_label(self, node):
        if self.in_footnote:
            ids = node.parent.attributes["ids"]
            id_text = ""
            for id_ in ids:
                id_text += "{} ".format(id_)
            else:
                id_text = id_text[:-1]
            if self.jupyter_target_html:
                self.markdown_lines.append("<p><a id={} href=#{}-link><strong>[{}]</strong></a> ".format(id_text, id_text, node.astext()))
            else:
                self.markdown_lines.append("<a id='{}'></a>\n**[{}]** ".format(id_text, node.astext()))
            raise nodes.SkipNode
        if self.in_citation:
            self.markdown_lines.append("\[")

    def depart_label(self, node):
        if self.in_citation:
            self.markdown_lines.append("\] ")

    # ===============================================
    #  code blocks are implemented in the superclass
    # ===============================================

    def visit_block_quote(self, node):
        if self.in_list:               #allow for 4 spaces interpreted as block_quote
            self.markdown_lines.append("\n")
            return
        self.in_block_quote = True
        if "epigraph" in node.attributes["classes"]:
            self.block_quote_type = "epigraph"
        self.markdown_lines.append("> ")

    def depart_block_quote(self, node):
        if "epigraph" in node.attributes["classes"]:
            self.block_quote_type = "block-quote"
        self.markdown_lines.append("\n")
        self.in_block_quote = False

    def visit_literal_block(self, node):
        JupyterCodeTranslator.visit_literal_block(self, node)
        if self.in_code_block:
            self.add_markdown_cell()

    def depart_literal_block(self, node):
        JupyterCodeTranslator.depart_literal_block(self, node)
    def visit_note(self, node):
        self.in_note = True
        self.markdown_lines.append(">**Note**\n>\n>")

    def depart_note(self, node):
        self.in_note = False

    def depart_raw(self, node):
        if self.jupyter_target_pdf:
            for attr in node.attributes:
                if attr == 'format' and node.attributes[attr] == 'html':
                    self.markdown_lines = []
                    return
        self.markdown_lines.append("\n\n")
        

    # =============
    # Jupyter Nodes
    # =============

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

    def visit_comment(self, node):
        raise nodes.SkipNode

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

    def visit_caption(self, node):
        self.in_caption = True

    def depart_caption(self, node):
        self.in_caption = False
        if self.in_toctree:
            self.markdown_lines.append("\n")

    # ================
    # general methods
    # ================
    def add_markdown_cell(self, slide_type="slide", title=False):
        """split a markdown cell here

        * add the slideshow metadata
        * append `markdown_lines` to notebook
        * reset `markdown_lines`
        """
        line_text = "".join(self.markdown_lines)
        formatted_line_text = self.strip_blank_lines_in_end_of_block(line_text)
        slide_info = {'slide_type': self.slide}

        if len(formatted_line_text.strip()) > 0:
            new_md_cell = nbformat.v4.new_markdown_cell(formatted_line_text)
            if self.metadata_slide:  # modify the slide metadata on each cell
                new_md_cell.metadata["slideshow"] = slide_info
                self.slide = slide_type
            if title:
                new_md_cell.metadata["hide-input"] = True
            self.output["cells"].append(new_md_cell)
            self.markdown_lines = []

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
