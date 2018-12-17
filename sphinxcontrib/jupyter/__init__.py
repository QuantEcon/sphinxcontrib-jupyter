from .builders.jupyter import JupyterBuilder
from .directive.jupyter import jupyter_node
from .directive.jupyter import Jupyter as JupyterDirective
from .directive.jupyter import JupyterDependency
from .transform import JupyterOnlyTransform

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
    app.add_node(jupyter_node)              #include in html=(visit_jupyter_node, depart_jupyter_node)
    app.add_directive("jupyter", JupyterDirective)
    app.add_directive("jupyter-dependency", JupyterDependency)

   
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
