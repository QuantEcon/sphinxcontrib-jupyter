import yaml
yaml.warnings({'YAMLLoadWarning': False})

from .builders.jupyter import JupyterBuilder
from .builders.jupyter_pdf import JupyterPDFBuilder
from .builders.jupyter_code import JupyterCodeBuilder
from .builders.jupyter_html import JupyterHTMLBuilder
from .directive.jupyter import jupyter_node
from .directive.jupyter import Jupyter as JupyterDirective
from .directive.jupyter import JupyterDependency
from .transform import JupyterOnlyTransform

import pkg_resources
VERSION = pkg_resources.get_distribution('pip').version

import sphinx
SPHINX_VERSION = sphinx.version_info

if SPHINX_VERSION[0] >= 2:
    from .directive import exercise

def _noop(*args, **kwargs):
    pass

def depart_exercise_node(self, node):
    return HTML.depart_admonition(self, node)
    

def setup(app):
    #Add Sphinx Version to ENV Configuration
    app.add_config_value('SPHINX_VERSION', SPHINX_VERSION, 'env')

    # Jupyter Builder and Options
    app.add_builder(JupyterBuilder)
    app.add_builder(JupyterCodeBuilder)
    app.add_builder(JupyterHTMLBuilder)
    app.add_builder(JupyterPDFBuilder)
    app.add_config_value("jupyter_language", "python3", "jupyter")
    app.add_config_value("jupyter_language_synonyms", [], "jupyter")
    #-IPYNB-#
    app.add_config_value("jupyter_images_html", True, "jupyter")
    app.add_config_value("jupyter_section_blocks", True, "jupyter")

    app.add_config_value("jupyter_static_file_path", [], "jupyter") #TODO: future deprecation
    app.add_config_value("jupyter_html_template", None, "jupyter")
    app.add_config_value("jupyter_template_coverage_file_path", None, "jupyter") #jupyter_coverage_template
    app.add_config_value("jupyter_threads_per_worker", 1, "jupyter")
    app.add_config_value("jupyter_number_workers", 1, "jupyter")
    app.add_config_value("jupyter_theme", None, "jupyter") 

    #-EXECUTE-#
    app.add_config_value("jupyter_execute_allow_errors", True, "jupyter")

    #review
    app.add_config_value("jupyter_drop_solutions", True, "jupyter") #TODO: reimplement as jupyter_solution_notebook = True
    app.add_config_value("jupyter_drop_tests", True, "jupyter") #TODO: class hide
    app.add_config_value("jupyter_dependencies", None, "jupyter") #TODO: rename
    app.add_config_value("jupyter_dependency_lists", {}, "jupyter") #TODO: rename

    app.add_config_value("jupyter_kernels", None, "jupyter") #TODO: remove
    app.add_config_value("jupyter_conversion_mode", "all", "jupyter") #TODO: remove
    app.add_config_value("jupyter_write_metadata", True, "jupyter") #TODO: deprecated
    app.add_config_value("jupyter_header_block", None, "jupyter") #TODO: deprecated
    app.add_config_value("jupyter_options", None, "jupyter") #TODO: remove (Aakash)
    app.add_config_value("jupyter_default_lang", "python3", "jupyter") #TODO: remove
    app.add_config_value("jupyter_lang_synonyms", [], "jupyter") #TODO: remove
    app.add_config_value("jupyter_generate_html", False, "jupyter") #TODO: deprecated 
    app.add_config_value("jupyter_execute_notebooks", False, "jupyter") #TODO: remove
    app.add_config_value("jupyter_make_site", False, "jupyter") #TODO: remove
    app.add_config_value("jupyter_make_coverage", False, "jupyter") #TODO: remove
    app.add_config_value("jupyter_target_pdf", False, "jupyter") #TODO: remove
    app.add_config_value("jupyter_coverage_dir", None, "jupyter") #TODO: remove 
    app.add_config_value("jupyter_theme_path", "theme", "jupyter") #TODO: remove 
    app.add_config_value("jupyter_template_path", "templates", "jupyter") #TODO: remove
    app.add_config_value("jupyter_download_nb_execute", None, "jupyter") #TODO: remove
    
    # Jupyter pdf options
    app.add_config_value("jupyter_latex_template", None, "jupyter") # jupyter_template_latex
    app.add_config_value("jupyter_latex_template_book", None, "jupyter") #jupyter_template_latexbook
    app.add_config_value("jupyter_pdf_logo", None, "jupyter")
    app.add_config_value("jupyter_bib_file", None, "jupyter")
    app.add_config_value("jupyter_pdf_author", None, "jupyter") 
    app.add_config_value("jupyter_pdf_showcontentdepth", 2, "jupyter") #TODO: remove
    app.add_config_value("jupyter_pdf_urlpath", None, "jupyter")
    app.add_config_value("jupyter_pdf_excludepatterns", [], "jupyter") 
    app.add_config_value("jupyter_pdf_book", False, "jupyter")
    app.add_config_value("jupyter_pdf_book_index", None, "jupyter")
    app.add_config_value("jupyter_pdf_book_title", None, "jupyter")
    app.add_config_value("jupyter_pdf_book_name", None, "jupyter")



    
    # Jupyter Directive
    app.add_node(jupyter_node, html=(_noop, _noop), latex=(_noop, _noop))
    app.add_directive("jupyter", JupyterDirective)
    app.add_directive("jupyter-dependency", JupyterDependency)

    # Exercise directive
    if SPHINX_VERSION[0] >= 2:
        app.add_config_value('exercise_include_exercises', True, 'html')
        app.add_config_value('exercise_inline_exercises', False, 'html')
        app.add_node(exercise.exerciselist_node)
        app.add_node(
            exercise.exercise_node,
            html=(exercise.visit_exercise_node, exercise.depart_exercise_node),
            latex=(exercise.visit_exercise_node, exercise.depart_exercise_node),
            text=(exercise.visit_exercise_node, exercise.depart_exercise_node)
        )
        app.add_directive('exercise', exercise.ExerciseDirective)
        app.add_directive('exerciselist', exercise.ExerciselistDirective)
        app.connect('doctree-resolved', exercise.process_exercise_nodes)
        app.connect('env-purge-doc', exercise.purge_exercises)

    # jupyter setup
    app.add_transform(JupyterOnlyTransform)
    app.add_config_value("jupyter_allow_html_only", False, "")
    app.add_config_value("jupyter_target_html", False, "jupyter") #TODO: remove
    app.add_config_value("jupyter_download_nb", False, "jupyter") #TODO: remove
    app.add_config_value("jupyter_download_nb_urlpath", None, "jupyter")
    app.add_config_value("jupyter_download_nb_image_urlpath", None, "jupyter")
    app.add_config_value("jupyter_images_markdown", False, "jupyter") #TODO: remove

    return {
        "version": VERSION,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
