from .markdown import MarkdownSyntax

class PDFSyntax(MarkdownSyntax):
    def __init__(self):
        """
        Provides syntax for IPYNB(PDF) notebooks

        PDF notebooks still make use of Markdown Syntax
        but require alternative implementations for some
        `visit` and `depart` methods to support additional
        features.
        """
        pass

    def visit_math(self, text):
        return "${}$".format(text)

    def visit_reference(self, node):
        if "refuri" in node and "http" in node["refuri"]:
            return "["
        elif "refid" in node:
            if 'equation-' in node['refid']:
                return "\eqref{"
            elif self.topic:
                return
            else:
                return "\hyperlink{"
        elif "refuri" in node and 'references#' not in node["refuri"]:
            return "["
        else:
            return "\hyperlink{"