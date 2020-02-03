"""
Provides accumulator objects to assist with building Syntax
"""


from docutils import nodes

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

    def build_syntax(self, item):
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
        return indent, marker, content

    def to_markdown(self):
        """
        converts the list items to markdown
        """
        markdown = []
        for item in self.items:
            indent, marker, content = self.build_syntax(item)
            markdown.append("{}{} {}".format(indent, marker, content))
        
        ## need a new line at the end
        markdown.append("\n")
        return "\n".join(markdown)

    def to_latex(self):
        """
        converts the list items to a latex string 
        """
        latex = []
        for item in self.items:
            indent, marker, content = self.build_syntax(item)
            latex.append("{}".format(content))

        latex.append("\n")
        return "\n".join(latex)
        
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

    align = "center"
    def __init__(self, node):
        self.table = []
        self.current_line = 0
        self.lines = []
        self.row = ""
        self.column_widths = []
        if 'align' in node:
            self.align = node['align']

    def __repr__(self):
        return self.to_markdown()

    def start_row(self):
        self.row = "|"

    def add_item(self, text):
        self.row += text + "|"

    def end_row(self):
        self.row += "\n"
        self.lines.append(self.row)
        self.row = ""

    def add_title(self, node):
        self.lines.append("### {}\n".format(node.astext()))

    def add_column_width(self, colwidth):
        self.column_widths.append(colwidth)

    def generate_alignment_line(self, line_length, alignment):
        left = ":" if alignment != "right" else "-"
        right = ":" if alignment != "left" else "-"
        return left + "-" * (line_length - 2) + right

    def add_header_line(self, header_line):
        for col_width in self.column_widths:
            header_line += self.generate_alignment_line(
                col_width, self.align)
            header_line += "|"
        self.lines.append(header_line + "\n")

    def to_markdown(self):
        """
        converts the table items to markdown
        """
        return "".join(self.lines)
