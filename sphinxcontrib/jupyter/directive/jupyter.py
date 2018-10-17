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
                   'slide-type': directives.unchanged}
    has_content = True
    add_index = False
 
    def run(self):
        env = self.state.document.settings.env  
        # gives you access to the parameter stored
        # in the main configuration file (conf.py)
        config = env.config
         
        # we create a new cell and we add it to the node tree
        node = jupyter_node()
        if 'cell-break' in self.options:
            node['cell-break'] = True
        
        elif 'slide-type' in self.options:
            #node.parent.append(nodes.literal(self.content.data))
            node['slide-type'] = self.options['slide-type']
        
        else:
            pass
        

 
        # we return the result
        return [ node ]

