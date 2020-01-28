class HTMLSyntax:

    def __init__(self):
        pass

    def visit_attribution(self):
        return "> "

    def visit_block_quote(self):
        return "> "

    def visit_bold(self):
        return "**"
    
    def depart_bold(self):
        return "**"

    def visit_citation(self, id_text):
        return "<a id='{}'></a>\n".format(id_text)

    def visit_code_block(self, language):
        return "``` {}".format(language)
    
    def depart_code_block(self):
        return "```"

    def visit_definition(self):
        return "<dd>"               #TODO: Is there a MD equivalent?

    def depart_definition(self):
        return "</dd>"              #TODO: Is there a MD equivalent?

    def visit_definition_list(self):
        return "<dl style='margin: 20px 0;'>"

    def depart_definition_list(self):
        return "</dl>"

    def visit_horizontal_rule(self):
        return "---"

    def visit_image(self, uri, attrs):
        """
        Construct HTML Image
        """
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
        return image

    def visit_inline_code(self):
        return "`"

    def depart_inline_code(self):
        return "`"

    def visit_italic(self):
        return "*"

    def depart_italic(self):
        return "*"

    def visit_heading(self, depth):
        return "#"*depth

    def visit_label(self):
        return "\["

    def depart_label(self):
        return "\]"

    def visit_link(self, text, link):
        return "[text](link)"

    #List(Start)
    #Note: Not required as implemented as an Accumulator Object List()

    def visit_literal(self):
        return "`"

    def depart_literal(self):
        return "`"

    def visit_literal_block(self, language=None):
        if language is None:
            return "```"
        else:
            return "``` {}".format(language)

    def depart_literal_block(self):
        return "```"

    def visit_math(self, text):
        return "$ {} $".format(text)

    def visit_math_block(self, text, label=None):
        if label:
            return "$$\n{0} {1}$$".format(text, label)
        else:
            return "$$\n{0}\n$$".format(text)

    def visit_note(self):
        return ">**Note**\n>\n>"
    
    def visit_title(self, level):
        return "#" * level