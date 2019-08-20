import re
from docutils import nodes
from docutils.parsers.rst import directives, Directive

from sphinx.locale import _
from sphinx.util.docutils import SphinxDirective

RE_EXERCISE_NUM = re.compile(r"^Exercise \d+$")

class exercise_node(nodes.General, nodes.Element):
    pass


class exerciselist_node(nodes.General, nodes.Element):
    pass


def visit_exercise_node(self, node):
    self.visit_para(node)


def depart_exercise_node(self, node):
    self.depart_para(node)
    self.visit_para(node)


class ExerciselistDirective(SphinxDirective):
    required_arguments = 0
    optional_arguments = 0
    option_spec = {
        "scope": lambda x: directives.choice(x, ("file", "section", "all")),
        "from": directives.unchanged,
        "labels": directives.unchanged,
        "force": directives.flag,
    }
    def run(self):
        list_number = self.env.new_serialno('exerciselist')
        target_id = f"exerciselist-{list_number:d}"
        _path = self.env.docname.replace("/", "-")
        node_id = f"exerciselist-{_path}-{list_number}"

        # create node and add some properties for later use
        node = exerciselist_node('')
        node["scope"] = self.options.get("scope", "file")
        node["force"] = self.options.get("force", False) != False
        node["from"] = self.options.get("from", None)
        _labels = self.options.get("labels", None)
        if _labels is not None:
            node["labels"] = [x.strip() for x in _labels.split(",")]
        else:
            node["labels"] = None

        if node["scope"] != "file" and node["from"] is not None:
            raise ValueError("Cannot set scope to be anything other than file AND set from")
        node["_id"] = node_id
        node["_target_id"] = target_id

        # create a target node for this exercise list
        targetnode = nodes.target("", "", ids=[target_id])

        if not hasattr(self.env, 'exercise_all_exercise_lists'):
            self.env.exercise_all_exercise_lists = {}

        self.env.exercise_all_exercise_lists[node_id] = {
            'docname': self.env.docname,
            'lineno': self.lineno,
            'exercise': node.deepcopy(),
            'target': targetnode,
            "number": list_number,
        }

        return [targetnode, node]


class ExerciseDirective(SphinxDirective):
    node_class = exercise_node
    required_arguments = 0
    option_spec = {"class": lambda x: directives.choice(x, ("cfu", ))}
    has_content = True
    option_spec = {
        "label": directives.unchanged,
        "title": directives.unchanged
    }
    node_class_str = "exercise"
    title_root = "Exercise"
    env_attr = 'exercise_all_exercises'

    def run(self):
        self.assert_has_content()

        num = self.env.new_serialno(self.node_class_str)
        target_id = f"{self.node_class_str}-{num:d}"
        targetnode = nodes.target('', '', ids=[target_id])
        _path = self.env.docname.replace("/", "-")
        node_id = f"{_path}-{num}"

        node = self.node_class("\n".join(self.content))
        node["_id"] = node_id
        node["classes"] = [self.options.get("class", None)]
        node["label"] = self.options.get("label", None)
        title_root = self.options.get("title", self.title_root)
        node["title_root"] = title_root

        title = _(f"{title_root} {num + 1}")

        para = nodes.paragraph()
        para += nodes.strong(title, title)
        node += para

        self.state.nested_parse(self.content, self.content_offset, node)

        if not hasattr(self.env, self.env_attr):
            setattr(self.env, self.env_attr, dict())

        getattr(self.env, self.env_attr)[node_id] = {
            'docname': self.env.docname,
            'lineno': self.lineno,
            'node_copy': node.deepcopy(),
            'target': targetnode,
            "number": num,
            "label": node["label"],
            "title_root": title_root,
        }
        return [targetnode, node]


def purge_exercises(app, env, docname):
    """
    This is run whenever `docname` processing begins

    This is our opportunity to clear a potentially stale cache of exercises
    for docname
    """
    for attr in ["exercise_all_exercises", "exercise_all_exercise_lists"]:
        if not hasattr(env, attr):
            # no exercises to deal with
            continue
        mydict = getattr(env, attr)
        for k in list(mydict.keys()):
            if mydict[k]["docname"] == docname:
                mydict.pop(k)


def process_exercise_nodes(app, doctree, fromdocname):
    """
    This will be run after all parsing is finished and AST is constructed

    We now have the opportunity to see all collected exercises and exercise
    lists and replace them with approrpriate content.

    Behavior depends on two config values that should be defined in conf.py

    1. exercise_include_exercises (bool): if this is False then all exercises
       are purged from the text. If true, they will remain
    2. exercise_inline_exercises (bool): if true, exercises are left intact
       where they are found in the document. If False, they are collected
       in an exercise list and removed from source. The inline content will
       be replaced by a link to the new position in the exercise list
    """
    # extract config values
    include_exercises = app.config.exercise_include_exercises
    inline_exercises = app.config.exercise_inline_exercises

    # if we don't want exercises, remove them all from the doctree
    if not include_exercises:
        for node in doctree.traverse(exercise_node):
            node.parent.remove(node)

        for node in doctree.traverse(exerciselist_node):
            node.parent.remove(node)

        return

    # if we don't want inline exercises, replace the exercise with a link back
    # to the exercise in an exercise list
    if not inline_exercises:
        all_exercises = {}
        for node in doctree.traverse(exercise_node):
            all_exercises[node["_id"]] = node

    # Replace all todolist nodes with a list of the collected todos.
    # Augment each todo with a backlink to the original location.
    env = app.builder.env

    def should_include_exercise(listnode, exercise_info):
        """
        given an exerciselist_node and an exercise_info, check to see if
        the exercise belongs in the list

        Logic as follows:

        - First check labels. if listnode specified labels,
          ensure exercise_info["label"] is selected in the lists labels
        - If that passes, then check listnode's from option. If specified
          exercise_info["docname"] must match listnode["from"]
        - If that passes then check scopes.
            - If scope is file, check if  exercise_info["docname"] matches
              fromdocname (closed over)
            - If scope is section, check if exercise_info["docname"] comes
              from same section as fromdocname
        - If that passes, include everything

        """
        # unpack args
        from_file = listnode["from"]
        scope = listnode["scope"]
        labels = listnode["labels"]
        if labels is not None:
            # we just check label now
            return exercise_info["label"] in labels

        ex_src_doc = exercise_info["docname"]
        if from_file is not None:
            return ex_src_doc == from_file
        if scope == "file":
            return ex_src_doc == fromdocname
        elif scope == "section":
            # check if not inside section
            if ("/" not in ex_src_doc) and ("/" not in fromdocname):
                return True
            elif "/" not in fromdocname:
                # ex_src_doc is in a section, but the exerciselist is not
                return False
            return ex_src_doc.rsplit('/', 1)[0] == fromdocname.rsplit('/', 1)[0]

        return True

    for node in doctree.traverse(exerciselist_node):
        listinfo = env.exercise_all_exercise_lists[node["_id"]]
        content = []

        if inline_exercises and not node["force"]:
            node.parent.remove(node)
            continue

        for ex_id, ex_info in env.exercise_all_exercises.items():
            if not should_include_exercise(node, ex_info):
                continue

            # make link from location in exercise list back to site where exercise appeared
            # in document
            back_to_text_para = _make_backlink(
                app, "(", "back to text", ")",
                ex_info["docname"], fromdocname, ex_info["target"]["refid"]
            )

            # Make link from body of text back down to here in exercise list only if we
            # don't want inline exercises AND the exercise list is in the same file as
            # the exercise
            if not inline_exercises and (listinfo["docname"] == ex_info["docname"]):

                # make a link from site where exercise appeared in document, back
                # to new location in exercise list
                _ex_title = ex_info["title_root"].lower()
                inline_para = _make_backlink(
                    app, "See {} {} in the ".format(_ex_title, ex_info["number"] + 1),
                    "exercise list", "",
                    fromdocname, ex_info["docname"], listinfo["target"]["refid"]
                )

                # replace this exercise with the link
                bq = nodes.block_quote()
                bq += inline_para
                if ex_info.get("removed", False) is not True:
                    all_exercises[ex_id].replace_self([bq])
                    ex_info["removed"] = True

            ex_to_add = ex_info['node_copy'].deepcopy()
            if ex_info["docname"] != listinfo["docname"]:
                # If the exercise comes from a different file make the heading be
                # `Exercise \d (path)`, e.g. `Exercise 4 (pandas/groupby)` only here in
                # the task list... not inline
                for text_node in ex_to_add.traverse(nodes.Text):
                    if RE_EXERCISE_NUM.match(text_node):
                        parent = text_node.parent
                        assert isinstance(parent, nodes.strong)  # make sure we have what we think we do
                        _src_path = app.builder.get_relative_uri(
                            fromdocname, ex_info["docname"]
                        )
                        _title_root = ex_to_add["title_root"]
                        new_title = "{} {} ({})".format(_title_root, ex_info["number"] + 1, _src_path)
                        parent.replace_self([nodes.strong(_(new_title), _(new_title))])
            content.append(ex_to_add)
            content.append(back_to_text_para)

        if len(content) > 0:
            node.replace_self(content)


def _make_backlink(app, pre, link_text, post, to_docname, from_docname, target_id):
    """
    Create a paragraph node that links back to text

    This will include:

    1. text node for opening paren (nodes.Text)
    2. Reference to the target from exercise_info (nodes.reference)
    3. Text to display with link (nodes.emphasis)
    4. text node for closing paren (nodes.Text)

    Parameters
    ----------
    app: app instance
        instance of app for creating relative uri between source and destination files

    pre: string
        Text to insert into paragraph before the link

    link_text: string
        Text to insert at the link site

    post: string
        Text to insert into paragraph after the link

    to_docname: string
        The name of the document where the link points to

    from_docname: string
        The name of the document where the link is inserted

    target_id: string
        The id of the anchor in to_docname that link should point to

    Returns: nodes.paragraph
        A paragraph node as described above

    """
    out = nodes.paragraph()
    # before link
    out += nodes.Text(_(pre), _(pre))

    # link
    link = nodes.reference('', '', internal=True)
    link["refdocname"] = to_docname
    link['refuri'] = app.builder.get_relative_uri(
        from_docname, to_docname
    ) + '#' + target_id

    # link text
    link_text = nodes.emphasis(_(link_text), _(link_text))
    link.append(link_text)
    out += link

    # after link
    out += nodes.Text(_(post), _(post))
    return out

