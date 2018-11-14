import os.path
import os 
import nbformat.v4
from xml.etree.ElementTree import ElementTree
from enum import Enum


class LanguageTranslator:
    """
    Simple extensible translator for programming language names between Sphinx
    and Jupyter.

    These two file formats accept ever-so-slightly different sets of programming
    language names; this class provides a friendly mechanism for translation between
    the two.

    The data itself is stored in an XML file within the templates directory configured
    in conf.py; deciding whether this is the most appropriate place to store that
    information is a @todo

    By default, if there is no entry in the XML file for a given language, the translator
    will return the language it was given; this decision was predicated on the fact that
    the vast majority of languages do not need any translation between Sphinx and Jupyter.

    """

    def __init__(self, template_paths):
        self.translator = dict()

        source_file = "languages.xml"
        for potentialPath in template_paths:
            full_filename = os.path.normpath(potentialPath + "/" + source_file)
            if os.path.isfile(full_filename):
                xml_parser = ElementTree()
                xml_root = xml_parser.parse(full_filename)

                languages = xml_root.findall("language")
                for language in languages:
                    sphinx_lang = None
                    jupyter_lang = None

                    for child in language:
                        if child.tag == "sphinx-name":
                            sphinx_lang = child.text
                        elif child.tag == "jupyter-name":
                            jupyter_lang = child.text

                    if sphinx_lang and jupyter_lang:
                        self.translator[sphinx_lang] = jupyter_lang
                    else:
                        # Explicit silent failure; ignore malformed data.
                        pass

    def translate(self, language_name):
        """
        Translates the provided language name, if it is found in the language dictionary.

        If the language is not found in the dictionary, return the name that was given.
        """
        return self.translator[language_name] if language_name in self.translator else language_name


class JupyterOutputCellGenerators(Enum):
    CODE = 1
    MARKDOWN = 2
    CODE_OUTPUT = 3

    @staticmethod
    def GetGeneratorFromClasses(obj, node):
        """
        Infers the type of output cell to be generated from the class attributes in the original Sphinx cell.

        Note that there is no guarantee as to the ordering or priority of output classes; a cell with the
        attribute ":class: no-execute output" is not considered to be well-defined.
        """
        res = { 
            "type" : JupyterOutputCellGenerators.CODE,
            "solution" : False,
            "test" : False 
            }
        class_list = node.attributes['classes']

        for item in class_list:
            if item == "no-execute" and not obj.jupyter_ignore_no_execute:
                res["type"] = JupyterOutputCellGenerators.MARKDOWN
            elif item == "skip-test" and not obj.jupyter_ignore_skip_test:
                res["type"] = JupyterOutputCellGenerators.MARKDOWN
            elif item == "output":
                res["type"] = JupyterOutputCellGenerators.CODE_OUTPUT
            # Check for Solution
            elif item == "solution":
                res["solution"] = True
            # Check for Test. 
            elif item == "test":
                res["test"] = True 

        return res

    def Generate(self, formatted_text, translator):
        """
        Generates the Jupyter cell object.
        """
        if self is JupyterOutputCellGenerators.CODE:
            res = nbformat.v4.new_code_cell(formatted_text)
        elif self is JupyterOutputCellGenerators.CODE_OUTPUT:
            res = nbformat.v4.new_output(output_type="stream", text=formatted_text)
        elif self is JupyterOutputCellGenerators.MARKDOWN:
            # Add triple backticks and the name of the language to the code block,
            # so that Jupyter renders the markdown correctly.
            language = translator.nodelang if translator.nodelang else ""
            if language == "none":
                raw_markdown = "```" + "text" + "\n" + formatted_text + "\n```\n"
            else:
                raw_markdown = "```" + language + "\n" + formatted_text + "\n```\n"
            res = nbformat.v4.new_markdown_cell(raw_markdown)
        else:
            raise Exception("Invalid output cell type passed to JupyterOutputCellGenerator.Generate.")

        return res


def get_source_file_name(filepath, srcdir):
    delimiter = os.sep 
    file_path_list = filepath.split(delimiter)
    srcdir_path_list = srcdir.split(delimiter)

    for i in range(len(srcdir_path_list)):
        if srcdir_path_list[i] != file_path_list[i]:
            raise ValueError("File path does not exist in the source directory")

    file_name_list = file_path_list[len(srcdir_path_list) - 1:]
    return "/".join(file_name_list) # Does this also need to be changed? 

