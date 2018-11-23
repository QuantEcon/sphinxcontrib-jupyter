from docutils import nodes
from docutils.parsers.rst import directives, Directive

class jupyter_node(nodes.Structural, nodes.Element): 
    pass

class Jupyter(Directive):
    # defines the parameter the directive expects
    # directives.unchanged means you get the raw value from RST
    # directives.flag doesn't expect an extra argument, hence if it's there
    # it means that we want a cell-break or a slide

    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {'cell-break': directives.flag,
                   'slide': directives.unchanged,
                   'slide-type': directives.unchanged}
    has_content = True
    add_index = False
 
    def run(self):
        # we create a new cell and we add it to the node tree
        node = jupyter_node()
        if 'cell-break' in self.options:
            node['cell-break'] = True
        if 'slide' in self.options:
            if self.options['slide'] == 'enable':
                node['slide'] = True 
            else:
                node['slide'] = False     
        if 'slide-type' in self.options:
            #node.parent.append(nodes.literal(self.content.data))
            node['slide-type'] = self.options['slide-type']
        
    
 
        # we return the result
        return [ node ]


class JupyterDependency(Directive):
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {}
    has_content = False
    add_index = False

    def run(self):
        # we create a new cell and add uri reference to specified file and we add it to the node tree
        node = jupyter_node()
        node['uri'] = directives.uri(self.arguments[0])
        # we return the result
        return [node]

