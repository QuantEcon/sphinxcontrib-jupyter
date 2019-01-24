from .builders.jupyter import JupyterBuilder
from .directive.jupyter import jupyter_node
from .directive.jupyter import Jupyter as JupyterDirective
from .directive.jupyter import JupyterDependency
from .directive.exercise import ExerciseDirective, exercise_node
from .transform import JupyterOnlyTransform
from sphinx.writers.html import HTMLTranslator as HTML
from sphinx.locale import admonitionlabels
admonitionlabels["exercise"] = "Exercise"
admonitionlabels["exercise_cfu"] = "Check for understanding"


def _noop(*args, **kwargs):
    pass


def visit_exercise_node(self, node):
    iscfu = "cfu" in node.attributes["classes"]
    name = "exercise_cfu" if iscfu else "exercise"
    return HTML.visit_admonition(self, node, name)

def depart_exercise_node(self, node):
    return HTML.depart_admonition(self, node)

def setup(app):
    # Jupyter Builder and Options
    app.add_builder(JupyterBuilder)
    app.add_config_value("jupyter_kernels", None, "jupyter")
    app.add_config_value("jupyter_conversion_mode", None, "jupyter")
    app.add_config_value("jupyter_write_metadata", True, "jupyter")
    app.add_config_value("jupyter_static_file_path", [], "jupyter")
    app.add_config_value("jupyter_header_block", "", "jupyter")
    app.add_config_value("jupyter_options", None, "jupyter")
    app.add_config_value("jupyter_default_lang", "python3", "jupyter")
    app.add_config_value("jupyter_lang_synonyms", [], "jupyter")
    app.add_config_value("jupyter_drop_solutions", True, "jupyter")
    app.add_config_value("jupyter_drop_tests", True, "jupyter")
    app.add_config_value("jupyter_ignore_no_execute", False, "jupyter")
    app.add_config_value("jupyter_ignore_skip_test", False, "jupyter")

    # Jupyter Directive
    app.add_node(jupyter_node, html=(_noop, _noop), latex=(_noop, _noop))
    app.add_directive("jupyter", JupyterDirective)
    app.add_directive("jupyter-dependency", JupyterDependency)

    # exercise directive
    app.add_directive("exercise", ExerciseDirective)
    app.add_node(
        exercise_node,
        html=(visit_exercise_node, depart_exercise_node)
    )

    app.add_transform(JupyterOnlyTransform)
    app.add_config_value("jupyter_allow_html_only", False, "jupyter")
    app.add_config_value("jupyter_target_html", False, "jupyter")
    app.add_config_value("jupyter_target_html_urlpath", None, "jupyter")
    app.add_config_value("jupyter_images_urlpath", False, "jupyter")

    return {
        "version": "0.2.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
