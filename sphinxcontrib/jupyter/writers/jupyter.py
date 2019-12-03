from docutils.writers import Writer

import nbformat

from .translate_code import JupyterCodeTranslator, JupyterCodeBlockTranslator
from .translate_ipynb import JupyterTranslator
from .translate_html import JupyterHTMLTranslator
from .translate_pdf import JupyterPDFTranslator

class JupyterWriter(Writer):
    
    builder_translator = {
        #Code Translators
        'jupytercode' : JupyterCodeBlockTranslator,  #JupyterCodeTranslator
        "execute" : JupyterCodeBlockTranslator,
        #RST + Code Translators
        'jupyter' : JupyterTranslator,
        'jupyterhtml' : JupyterHTMLTranslator,
        'jupyterpdf' : JupyterPDFTranslator
    }

    def __init__(self, builder):
        super().__init__()           #init docutils.writers.Writer
        self.builder = builder
        self.output = None
        try:
            self.translator = self.builder_translator[builder.name]
        except:
            msg = "Builder ({}) does not have a valid Translator".format(builder.name)
            raise InvalidTranslator(msg)

    def translate(self):
        self.settings = self.document.settings

        #TODO: Investigate the need for these settings here
        self.document.settings.newlines = True
        self.document.settings.indents = True

        visitor = self.translator(self.document, self.builder)
        self.document.walkabout(visitor)   #TODO: What is this doing?
        self.output = visitor.output.notebook_as_string   #writers/notebook -> JupyterNotebook

    def _set_ref_urlpath(self, urlpath=None):
        """
        Set a urlpath to be used to prepend links in the notebook, so that it can be different for different targets.
        """
        self.builder.urlpath = urlpath

    def _set_jupyter_download_nb_image_urlpath(self, urlpath=None):
        """
        Set a urlpath to be used to prepend image paths in the notebook, so that it can be different for different targets.
        """
        self.builder.jupyter_download_nb_image_urlpath = urlpath

class InvalidTranslator(Exception):
    pass