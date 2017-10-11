import docutils.writers
import nbformat

from .translate_code import JupyterCodeTranslator
from .translate_all import JupyterTranslator


class JupyterWriter(docutils.writers.Writer):
    def __init__(self, builder):
        docutils.writers.Writer.__init__(self)

        self.output = None
        self.builder = builder
        self.translator_class = self._identify_translator(builder)

    def translate(self):
        self.document.settings.newlines = \
            self.document.settings.indents = \
            self.builder.env.config.xml_pretty

        visitor = self.translator_class(self.builder, self.document)

        self.document.walkabout(visitor)
        self.output = nbformat.writes(visitor.output)

    def _identify_translator(self, builder):
        """
        Determine which translator class to apply to this translation. The choices are 'code' and 'all'; all converts
        the entire sphinx RST file to a Jupyter notebook, whereas 'code' only translates the code cells, and
        skips over all other content.

        Typically, you would use 'code' when you're testing your code blocks, not for final publication of your
        notebooks.

        The default translator to use is set in conf.py, but this value can be overridden on the command line.

        :param builder: The builder object provided by the Sphinx run-time
        :return: The translator class object to instantiate.
        """
        code_only = False
        if "jupyter_conversion_mode" not in builder.config \
                or builder.config["jupyter_conversion_mode"] is None:
            self.builder(
                "jupyter_conversion_mode is not given in conf.py. "
                "Set conversion_mode as default(code)")
            code_only = True
        else:
            if builder.config["jupyter_conversion_mode"] == "code":
                code_only = True
            elif builder.config["jupyter_conversion_mode"] != "all":
                builder.warn(
                    "Invalid jupyter_conversion_mode is given({}). "
                    "Set conversion_mode as default(code)"
                    .format(builder.config["jupyter_conversion_mode"]))
                code_only = True

        return JupyterCodeTranslator if code_only else JupyterTranslator
