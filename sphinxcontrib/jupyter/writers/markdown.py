
class MarkdownConstructor:

    def __init__(self):
        """A collection of markdown syntax methods"""
        pass

    @classmethod
    def highlighted_code(self, code, language):
        template = textwrap.dedent(
        """``` {language}
        {code}
        ```
        """
        )
        return template % {'code' : code, 'language' : language}
    
    @classmethod
    def bold(self, text):
        template = "**{text}**"
        return template % {'text' : text}


class MarkdownSyntax:
    """
    Provides Markdown Syntax

    visit_{}:
        methods contain the begining of the markdown syntax
    depart_{}:
        methods contain the end of the markdown syntax and may not be needed

    some items are multi-part that are most easily constructed in full. But 
    may be split to use visit_reference and visit_label to mimic sphinx

    Reference
    ---------
    [1] https://commonmark.org/help/
    [2] https://spec.commonmark.org/0.29/
    """

    def __init__(self):
        pass

    def visit_bold(self):
        return "**"
    
    def end_bold(self):
        return "**"

    def visit_italic(self):
        return "*"

    def depart_italic(self):
        return "*"

    def visit_heading(self, depth):
        return "#"*depth

    def visit_link(self, text, link):
        return "[text](link)"

    def visit_code_block(self, language):
        return "``` {}".format(language)
    
    def depart_code_block(self):
        return "```"

    def visit_block_quote(self):
        return "> "

    def visit_list(self):
        return "* "

    def visit_enumerated_list(self):
        return "1. "

    def visit_horizontal_rule(self):
        return "---"

    #-Inline-#

    def visit_inline_code(self):
        return "`"

    def depart_inline_code(self):
        return "`"
    
    #-Multi Part Elements-#
    
    def image(self, label, link):
        return "![{}]({})".format(label, link)

    def visit_image(self, text, link):
        return "!"

    def visit_label(self):
        return "["

    def depart_label(self):
        return "]"


#-List Accumulators-#

class List:

    indentation = " "*2
    marker = "*"

    def __init__(self, level):
        """
        List Object

        Parameters
        ----------
        level : int
                Specify Level for List (base level=0)
        marker : str, optional(default="*")

        Example
        -------
        from markdown import List                                                                                                          
        a = List(level=0)                                                                                                                  
        a.add_item("first")                                                                                                                
        a.add_item("second")                                                                                                               
        a.to_markdown()
        """
        self.items = []
        self.level = level

    def __repr__(self):
        return self.to_markdown()

    def add_item(self, item):
        """
        Add Item to List
        
        Parameters
        ----------
        item : str or List
               add an element or a list object
        """
        self.items.append(item)

    def to_markdown(self):
        markdown = []
        indent = self.indentation * self.level
        for item in self.items:
            if issubclass(type(item), List):
                markdown.append("{}".format(item))
            else:
                markdown.append("{}{} {}".format(indent, self.marker, item))
        return "\n".join(markdown)

class EnumeratedList(List):

    def to_markdown(self):
        markdown = []
        indent = self.indentation * self.level
        for num, item in enumerate(self.items):
            if issubclass(type(item), List):
                markdown.append("{}".format(item))
            else:
                self.marker = "{}.".format(num+1)
                markdown.append("{}{} {}".format(indent, self.marker, item))
        return "\n".join(markdown)

#-> Use above in Translator and if requried develop a ListCollector

class ListCollector:
    """
    An automatic list collector object to remove the need to track levels
    """
    def __init__(self):
        pass