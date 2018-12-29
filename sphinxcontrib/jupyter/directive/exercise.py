from docutils.nodes import Admonition, Element
from docutils.parsers.rst.directives.admonitions import BaseAdmonition


class exercise_node(Admonition, Element):
    pass


class ExerciseDirective(BaseAdmonition):
    node_class = exercise_node
