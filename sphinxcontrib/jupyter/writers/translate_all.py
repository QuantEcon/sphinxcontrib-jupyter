import re
import nbformat.v4
from .translate_code import JupyterCodeTranslator

class JupyterTranslator(JupyterCodeTranslator):
    """ Jupyter Translator for Text and Code
    """

    SPLIT_URI_ID_REGEX = re.compile(r"([^\#]*)\#?(.*)")

    def __init__(self, builder, document):
        super().__init__(builder, document)

        # Settings
        self.sep_lines = "  \n"
        self.sep_paras = "\n\n"
        self.indent_char = " "
        self.indent = self.indent_char * 4
        self.default_ext = ".ipynb"

        # Variables used in visit/depart
        self.in_code_block = False  # if False, it means in markdown_cell
        self.in_block_quote = False
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
        self.in_citation = False

        self.table_builder = None

    # specific visit and depart methods
    # ---------------------------------

    # =========
    # Sections
    # =========
    def visit_document(self, node):
        """at start
        """
        JupyterCodeTranslator.visit_document(self, node)

    def depart_document(self, node):
        """at end

        Almost the exact same implementation as that of the superclass.
        """
        self.add_markdown_cell()
        JupyterCodeTranslator.depart_document(self, node)

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

        if self.in_code_block:
            self.code_lines.append(text)
        elif self.table_builder:
            self.table_builder['line_pending'] += text
        elif self.in_block_quote:
            pass
        else:
            self.markdown_lines.append(text)

    def depart_Text(self, node):
        pass

    # image
    def visit_image(self, node):
        """
        Notes
        -----
        1. Should this use .has_attrs()?
        2. the scale, height and width properties are not combined in this
        implementation as is done in http://docutils.sourceforge.net/docs/ref/rst/directives.html#image 
        
        """
        return_markdown = False             #TODO: enable return markdown option
        uri = node.attributes["uri"]
        attrs = node.attributes
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
        #-Construct MD image
        if return_markdown:
            image = "![{0}]({0})".format(uri)
        self.markdown_lines.append(image)

    # math
    def visit_math(self, node):
        """inline math"""
        math_text = node.attributes["latex"].strip()
        formatted_text = "$ {} $".format(math_text)

        if self.table_builder:
            self.table_builder['line_pending'] += formatted_text
        else:
            self.markdown_lines.append(formatted_text)

    def visit_displaymath(self, node):
        """directive math"""
        math_text = node.attributes["latex"].strip()

        if self.list_level == 0:
            formatted_text = "$$\n{0}\n$${1}".format(
                math_text, self.sep_paras)
        else:
            formatted_text = "$$\n{0}\n$${1}".format(
                math_text, self.sep_paras)

        #check for labelled math
        if node["label"]:
            print(node.attributes["label"])
            formatted_text = "<table width=100%><tr style='background-color: #FFFFFF !important;'>\n"\
                             + "<td width=10%></td>\n"\
                             + "<td width=80%>\n"\
                             + formatted_text.rstrip("\n")\
                             + "\n</td>"\
                             + "<td width=10% style='text-align:center !important;'>\n"

        self.markdown_lines.append(formatted_text)

        # Add the line number reference.
        if node["ids"]:
            referenceBuilder = "(" + str(node["number"]) + ")"
            self.markdown_lines.append(referenceBuilder)

        if node["label"]:
            self.markdown_lines.append("\n</td></tr></table>\n\n")

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
        else:
            self.markdown_lines.append(self.sep_paras)

    # title(section)
    def visit_title(self, node):
        self.add_markdown_cell()

        if self.in_topic:
            self.markdown_lines.append(
                "{} ".format("#" * (self.section_level + 1)))
        elif self.table_builder:
            self.markdown_lines.append(
                "### {}\n".format(node.astext()))
        else:
            self.markdown_lines.append(
                "{} ".format("#" * self.section_level))

    def depart_title(self, node):
        if not self.table_builder:
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

    # figures
    def visit_figure(self, node):
        pass

    def depart_figure(self, node):
        self.markdown_lines.append(self.sep_lines)

    # reference
    def visit_reference(self, node):
        """anchor link"""
        self.in_reference = True
        self.markdown_lines.append("[")
        self.reference_text_start = len(self.markdown_lines)

    def depart_reference(self, node):
        if self.in_topic:
            # Jupyter Notebook uses the target text as its id
            uri_text = "".join(
                self.markdown_lines[self.reference_text_start:]).strip()
            uri_text = re.sub(
                self.URI_SPACE_REPLACE_FROM, self.URI_SPACE_REPLACE_TO, uri_text)
            formatted_text = "](#{})".format(uri_text)
            self.markdown_lines.append(formatted_text)

        else:
            # if refuri exists, then it includes id reference(#hoge)
            if "refuri" in node.attributes:
                refuri = node["refuri"]

                # add default extension(.ipynb)
                if "internal" in node.attributes and node.attributes["internal"] == True:
                    refuri = self.add_extension_to_inline_link(
                        refuri, self.default_ext)
            else:
                # in-page link
                if "refid" in node:
                    refid = node["refid"]
                    refuri = "#{}".format(refid)
                # error
                else:
                    self.error("Invalid reference")
                    refuri = ""

            self.markdown_lines.append("]({})".format(refuri))

        self.in_reference = False

    # target: make anchor
    def visit_target(self, node):
        if "refid" in node.attributes:
            refid = node.attributes["refid"]
            self.markdown_lines.append(
                "\n<a id='{}'></a>\n".format(refid))

    # list items
    def visit_bullet_list(self, node):
        self.list_level += 1
        # markdown does not have option changing bullet chars
        self.bullets.append("-")
        self.indents.append(len(self.bullets[-1]) + 1)

    def depart_bullet_list(self, node):
        self.list_level -= 1
        if self.list_level == 0:
            self.markdown_lines.append(self.sep_paras)
            if self.in_topic:
                self.add_markdown_cell()

        self.bullets.pop()
        self.indents.pop()

    def visit_enumerated_list(self, node):
        self.list_level += 1
        # markdown does not have option changing bullet chars
        self.bullets.append("1.")
        self.indents.append(len(self.bullets[-1]) + 1)

    def depart_enumerated_list(self, node):
        self.list_level -= 1
        if self.list_level == 0:
            self.markdown_lines.append(self.sep_paras)

        self.bullets.pop()
        self.indents.pop()

    def visit_list_item(self, node):
        # self.first_line_in_list_item = True
        head = "{} ".format(self.bullets[-1])
        self.markdown_lines.append(head)
        self.list_item_starts.append(len(self.markdown_lines))

    def depart_list_item(self, node):
        # self.first_line_in_list_item = False

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
        if self.in_citation:
            self.markdown_lines.append("\[")

    def depart_label(self, node):
        if self.in_citation:
            self.markdown_lines.append("\] ")

    # ===============================================
    #  code blocks are implemented in the superclass
    # ===============================================

    def visit_block_quote(self, node):
        self.in_block_quote = True
        block_quote = "\n    {}".format(node.astext())
        self.markdown_lines.append(block_quote)

    def depart_block_quote(self, node): 
        self.in_block_quote = False

    def visit_literal_block(self, node):
        JupyterCodeTranslator.visit_literal_block(self, node)

        if self.in_code_block:
            self.add_markdown_cell()

    # ================
    # general methods
    # ================
    def add_markdown_cell(self):
        """split a markdown cell here

        * append `markdown_lines` to notebook
        * reset `markdown_lines`
        """
        line_text = "".join(self.markdown_lines)
        formatted_line_text = self.strip_blank_lines_in_end_of_block(line_text)

        if len(formatted_line_text.strip()) > 0:
            new_md_cell = nbformat.v4.new_markdown_cell(formatted_line_text)
            self.output["cells"].append(new_md_cell)
            self.markdown_lines = []

    @classmethod
    def split_uri_id(cls, uri):
        return re.search(cls.SPLIT_URI_ID_REGEX, uri).groups()

    @classmethod
    def add_extension_to_inline_link(cls, uri, ext):
        if "." not in uri:
            uri, id_ = cls.split_uri_id(uri)
            return "{}{}#{}".format(uri, ext, id_)

        return uri

