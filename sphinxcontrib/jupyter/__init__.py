from .builders.jupyter import JupyterBuilder
from .transform import JupyterOnlyTransform

def setup(app):
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
    app.add_config_value("jupyter_slide", True, "jupyter")  
    app.add_transform(JupyterOnlyTransform)
    app.add_config_value("jupyter_allow_html_only", False, "jupyter")

    return {
        "version": "0.2.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
