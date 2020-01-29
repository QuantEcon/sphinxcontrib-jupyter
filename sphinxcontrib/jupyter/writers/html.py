
from .markdown import MarkdownSyntax

class HTMLSyntax(MarkdownSyntax):

    def __init__(self):
        """
        Provides syntax for IPYNB(HTML) notebooks

        HTML notebooks still make use of Markdown Syntax
        but require alternative implementations for some
        `visit` and `depart` methods to support additional
        features. For example, images included as html have 
        access to more scale properties.
        """
        pass

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