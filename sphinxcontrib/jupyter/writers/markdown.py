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

    def visit_attribution(self):
        return "> "

    def visit_block_quote(self):
        return "> "

    def visit_bold(self):
        return "**"
    
    def end_bold(self):
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

    def visit_image(self, uri):
        return "![{0}]({0})".format(uri)

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
        return "["

    def depart_label(self):
        return "]"

    def visit_link(self, text, link):
        return "[text](link)"

    #List(Start)
    #Note: Not required as implemented as an Accumulator Object List()

    def visit_reference(self):
        return "("
    
    def depart_reference(self):
        return ")"

#-Accumulator Objects-#

class List:

    indentation = " "*2
    marker = "*"
    markers = dict()
    item_no = 0

    def __init__(self, level, markers, item_no=0):
        """
        List Object

        Parameters
        ----------
        level : int
                Specify Level for List (base level=0)
        markers : dict
                A dictionary of markers with keys as levels and values as the current marker in that level
        item_no : stores at what count the current item came in the list, if we consider the list as a queue of items

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
        self.item_no = item_no

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
        marker = self.markers[self.level]
        itemtuple = (marker, self.item_no, self.level, item)
        if len(self.items) > 0:
            last_item = self.items.pop()
            ### checking if the new item is a child of the same list item
            if self.item_no == last_item[1] and last_item[2] == self.level:
                last_item_text = last_item[3]
                item_text = item
                if not isinstance(last_item_text, str):
                    last_item_text = last_item_text.astext()
                if not isinstance(item_text, str):
                    item_text = item_text.astext()
                content = last_item_text + item_text
                itemtuple = (marker, self.item_no, self.level, content)
            else:
                self.items.append(last_item)
        self.items.append(itemtuple)

    def to_markdown(self):
        """
        converts the list items to markdown
        """
        markdown = []
        for item in self.items:
            indent = self.indentation * item[2]
            marker = item[0]
            if isinstance(item[0], int):
                marker = str(item[0]) + "."

            content = ""
            for children in item[3]:
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
        return self.markers

    def set_marker(self, node):
        """
        sets the updated marker for the current level in the self.markers dictionary

        Parameters
        ----------
        node : the node object under whose visit/depart method this function was called
        """
        if isinstance(node.parent, nodes.enumerated_list) or isinstance(node.parent.parent, nodes.enumerated_list):
            if self.level in self.markers:
                count = self.markers[self.level]
                self.markers[self.level] = count + 1
            else:
                self.markers[self.level] = 1
        else:
            self.markers[self.level] = "*"
        self.item_no += 1

    def itemlist(self):
        return self.items 

    def getlevel(self):
        return self.level
    
    def get_item_no(self):
        return self.item_no


#-Table Builder-#

class TableBuilder:

    def __init__(self):
        self.table = []

    def add_row(self, row):
        pass
