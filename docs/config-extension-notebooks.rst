.. _config_extension_notebooks:

Constructing Jupyter Notebooks
------------------------------

+--------------------------------+-----------------------------------------------------------------------+-----------------------+
| Option                         | Description                                                           | Default               |
+================================+=======================================================================+=======================+
| jupyter_conversion_mode        | **["all", "code"]** This option specifies which writer to use when    | None                  |
|                                | constructing notebooks. The "all" option produces complete notebooks  |                       |
|                                | which includes text, figures, and code. The "code" option produces    |                       |
|                                | notebooks that only contain the code blocks.                          |                       |
+--------------------------------+-----------------------------------------------------------------------+-----------------------+
| jupyter_static_file_path       | Specify path to `_static` folder                                      | []                    |
+--------------------------------+-----------------------------------------------------------------------+-----------------------+
| jupyter_header_block           | Add a header block to every generated notebook as a Path to RST file  | ""                    |
+--------------------------------+-----------------------------------------------------------------------+-----------------------+
| jupyter_default_lang           | Specify default language for collection of RST files                  | "python3"             |
+--------------------------------+-----------------------------------------------------------------------+-----------------------+
| jupyter_lang_synonyms          | Specify any language synonyms. This will be used when parsing code    | []                    |
|                                | blocks. For example, python and ipython have slightly different       |                       |
|                                | highlighting directives but contain code that can both be executed on |                       |
|                                | the same kernel                                                       |                       |
+--------------------------------+-----------------------------------------------------------------------+-----------------------+
| `jupyter_kernels`_             | specify kernel information for the jupyter notebook metadata          |                       |
+--------------------------------+-----------------------------------------------------------------------+-----------------------+

.. TODO::

    jupyter_write_metadata
    jupyter_options
    jupyter_drop_solutions
    jupyter_drop_tests
    jupyter_ignore_no_execute
    jupyter_ignore_skip_test
    jupyter_allow_html_only
    jupyter_target_html
    jupyter_images_markdown


jupyter_kernels
~~~~~~~~~~~~~~~

*Default Value:* None 

Specify kernel information for the jupyter notebook metadata. This is **required** in `conf.py`.

.. code-block:: text

    jupyter_kernels = {
        "python3": {
            "kernelspec": {
                "display_name": "Python",
                "language": "python3",
                "name": "python3"
                },
            "file_extension": ".py",
        },
    }

This information is used to connect to the desired jupyter kernel when starting the notebook.

.. TODO:: 

    See Issue `196 <https://github.com/QuantEcon/sphinxcontrib-jupyter/issues/196)>`__