.. _links:

Links
-----

Links are generated as markdown references to jump between notebooks and
the sphinx link machinery is employed to track links across documents.

An external link to another `notebook (as full file) <links_target.ipynb>`_

This is a paragraph that contains `a google hyperlink`_.

.. _a google hyperlink: https://google.com.au

- An inline reference to :ref:`another document <links_target>`

Special Cases
-------------

The following link has ( and ) contained within them that doesn't render nicely in markdown. In this case the extension will substitute ( with `%28` and ) with `%29`

Thinking back to the mathematical motivation, a `Field <https://en.wikipedia.org/wiki/Field_\(mathematics\)>`_ is an `Ring` with a few additional properties