
class MarkdownSyntax:

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