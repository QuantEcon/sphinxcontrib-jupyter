"""
Contains Markdown Syntax and Object Accumulators
"""
from docutils import nodes

class MarkdownSyntax:
    """
    Provides Markdown Syntax

    visit_{}:
        methods contain the begining of the markdown syntax
    depart_{}:
        methods contain the end of the markdown syntax and may not be needed

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
    
    def visit_image(self, text, link):
        return "!"

    def visit_label(self):
        return "["

    def depart_label(self):
        return "]"

    def visit_reference(self):
        #TODO: consider context for different reference types in markdown
        return "("
    
    def depart_reference(self):
        #TODO: consider context for different reference types in markdown
        return ")"

#-Accumulator Objects-#
# List, Enumerated List
# TODO: TableBuilder, Image(?)

class List:

    indentation = " "*2
    marker = "*"
    markers = dict()

    def __init__(self, level, markers):
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
        self.markers = markers

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
        self.items.append((item[0], self.level, item[1]))

    def append_to_last_item(self, lines):
        item = self.items.pop()
        content = item[2].astext() + lines
        self.items.append((item[0], item[1], content))

    def to_markdown(self):
        markdown = []
        for item in self.items:
            indent = self.indentation * item[1]
            marker = item[0]
            if isinstance(item[0], int):
                marker = str(item[0]) + "."

            ### handling inline math list items
            content = ""
            for children in item[2]:
                if isinstance(children, nodes.math):
                    content += "${}$".format(children.astext())
                else:
                    if isinstance(children, str) or isinstance(children, int):
                        content +=  children
                    else:
                        content +=  children.astext()
            markdown.append("{}{} {}".format(indent, marker, content))
        
        ## need a new line at the end
        markdown.append("\n")
        return "\n".join(markdown)

    def increment_level(self):
        self.level += 1

    def decrement_level(self):
        self.level -= 1

    def get_marker(self):
        return self.markers[self.level]

    def set_marker(self, node):
        if isinstance(node.parent, nodes.enumerated_list):
            if self.level in self.markers:
                count = self.markers[self.level]
                self.markers[self.level] = count + 1
            else:
                self.markers[self.level] = 1
        else:
            self.markers[self.level] = "*"

    def itemlist(self):
        return self.items 

    def getlevel(self):
        return self.level

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

#-Table Builder-#

class TableBuilder:

    def __init__(self):
        self.table = []

    def add_row(self, row):
        pass
