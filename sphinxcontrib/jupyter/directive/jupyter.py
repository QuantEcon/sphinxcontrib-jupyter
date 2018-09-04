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
                   'slide': directives.flag,
                   'path': directives.unchanged,
                   'type': directives.unchanged}
    has_content = True
    add_index = False
 
    def run(self):
        env = self.state.document.settings.env  
        # gives you access to the parameter stored
        # in the main configuration file (conf.py)
        config = env.config
         
        # we create a cell
        idb = nodes.make_id("new-cell")
        cell = nodes.section(ids=[idb])
         
         
        # we create the content of the blog post
        # because it contains any kind of RST
        # we parse parse it with function nested_parse
        # par = nodes.paragraph()
        # self.state.nested_parse(content, self.content_offset, par)
         
        # we create a blogpost and we add the section
        node = jupyter_node()
        if 'cell-break' in self.options:
            node['cell-break'] = True

        # if 'slide' in self.options:
        #     node['slide'] = True
        # node += cell
        # node += par
         
        # we return the result
        return [ node ]


# FUTURE SUPPORT FOR HTML, LATEX writers

# def visit_jupyter_node(self, node):
#     pass

# def depart_jupyter_node(self, node):
#     pass

