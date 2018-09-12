"""
Add sphinxcontrib-jupyter transforms
"""

from docutils import nodes
from sphinx.transforms import SphinxTransform
from sphinx import addnodes
from sphinx.util import logging

logger = logging.getLogger(__name__)

def process_only_nodes(config, document, tags):
    # type: (nodes.Node, Tags) -> None
    """Filter ``only`` nodes which does not match *tags* or html (through config)"""
    ret_html_cell = config['jupyter_allow_html_only'] 
    for node in document.traverse(addnodes.only):
        try:
            ret = tags.eval_condition(node['expr'])  #check for jupyter only
            if ret_html_cell and node['expr'] == 'html':  #allow html only cells if option is specified
                ret = True
        except Exception as err:
            logger.warning(__('exception while evaluating only directive expression: %s'), err,
                           location=node)
            node.replace_self(node.children or nodes.comment())
        else:
            if ret:
                node.replace_self(node.children or nodes.comment())
            else:
                # A comment on the comment() nodes being inserted: replacing by [] would
                # result in a "Losing ids" exception if there is a target node before
                # the only node, so we make sure docutils can transfer the id to
                # something, even if it's just a comment and will lose the id anyway...
                node.replace_self(nodes.comment())


class JupyterOnlyTransform(SphinxTransform):

    default_priority = 50

    def apply(self):
        process_only_nodes(self.config, self.document, self.app.builder.tags)

