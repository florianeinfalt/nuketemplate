Getting Started
===============

Folder structure
----------------

``nuketemplate`` is a wrapper around the Jinja 2 templating engine. If you are
not familiar with Jinja 2 templates, read the documentation `Jinja 2`_.

Let's start with a simple template structure. Create a folder structure,
like so: ::

    /attrs
        main.j2
        attrs_write.j2
    /nodes
        main.j2
        nodes.j2

The ``main.j2`` file is the root template in which we will include all other
sub templates (``attrs_write.j2`` and ``nodes.j2``).

Defining attributes
-------------------

The final format of all attributes must be a valid JSON object so make sure the
aggregator in ``/attrs/main.j2`` is a valid JSON object ``{}``.

Add the following code snippet to ``/attrs/main.j2``. This code will parse
every file in the same folder that has a file name starting with ``attrs_`` and
include it in the final set of attributes. That means it is very easy to extend
by simply creating additional files with the same naming pattern.

.. code-block:: jinja

    {
        {% for attr_template in attr_templates %}
            {% include attr_template | basename %}
            {% if not loop.last %},{% endif %}
        {% endfor %}
    }

Add the following code snippet to  ``/attrs/attrs_write.j2``. Again, this will
be included in the JSON object in ``/attrs/main.j2``.

.. code-block:: javascript

    "output": {
        "flat": {
            "channels": "rgb",
            "file_type": "jpg",
            "_jpeg_quality": 1.0,
            "_jpeg_sub_sampling": "4:4:4",
            "colorspace": "sRGB"
        },
        "layered": {
            "channels": "rgba",
            "file_type": "png",
            "datatype": "8 bit",
            "colorspace": "sRGB"
        }
    }

Defining Node Graphs in Templates
---------------------------------

Add the following code snippet to ``/nodes/main.j2``. This will reference the
sub template ``nodes.j2`` and include it in the list of sub templates.

.. code-block:: jinja

    [
        {% include "nodes.j2" %}
    ]

.. note::

    The final format of all nodes must be a valid JSON object so make sure the
    aggregator in ``/nodes/main.j2`` is a valid JSON object ``[]``.

To add further sub templates simply extend the list with further ``include``
directives.

Add the following code snippet to ``/nodes/nodes.j2``.

.. code-block:: javascript

    {
        ">>": "write",
        "write": {
            "type": "Write",
            "inputs": ["cutout"],
            "attr": {{ attrs["output"]["layered"] | tojson }},
            "id": {{ id_data | tojson }}
        },
        "cutout": {
            "type": "Premult",
            "inputs": ["alpha"]
        },
        "alpha": {
            "type": "Shuffle",
            "inputs": ["<<"]
        }
    }

This is a simple sub template in the standard format. The first item is the
``start`` indicator, which tells the
:class:`~nuketemplate.convert.AbstractTemplateConverter` which node to start
with. The standard key to indicate the ``start`` value is ``>>`` but this can
be freely defined in the
:class:`~nuketemplate.convert.AbstractTemplateConverter` constructor.

One node in the template will have to have the ``end`` indicator as one of its
inputs (the default is ``<<`` but this can be redefined in the
:class:`~nuketemplate.convert.AbstractTemplateConverter` constructor).
This indicates where the sub graph will be connected to the next sub graph in
the list.

Conceptually it is best to think about this node graph as a Nuke graph
"upside-down", the ``start`` node being the last node in the graph.

A node in the template format must implement the following format:

.. code-block:: javascript

    node name: {
        type: Nuke node type,
        inputs: List of inputs from the same subgraph,
        attr: {
            Nuke attribute: value
        },
        id: {
            UUID type: UUID
        }
    }

.. note::

    The ``attr`` and ``id`` keys are optional and will be ignored if not
    specified.

All values can be substituted using Jinja 2 templating, like in the example.

.. note::

    Use the ``tojson`` filter to ensure values are converted to valid JSON

Building the Nuke Node Graph
----------------------------

With the templates in place, start Nuke and import the following
``nuketemplate`` classes:

.. code-block:: python

    from nuketemplate.template import AbstractTemplate
    from nuketemplate.convert import AbstractTemplateConverter
    from nuketemplate.build import NukeGraphBuilder

Initialise an :class:`~nuketemplate.template.AbstractTemplate` like so:

.. code-block:: python

    template = AbstractTemplate(root='/path/to/template/folder')

Since we have specified the variable ``id_data`` in our template, we will
have to supply this data.

.. code-block:: python

    data = {'id_data': {'uuid': '3a5c2055-e288-4bc2-90cb-dc0fb9ae462e'}}

Now, pass the data to the
:func:`~nuketemplate.template.AbstractTemplate.render()` function, like so:

.. code-block:: python

    template.render(**data)

After template rendering, initialise a
:class:`~nuketemplate.convert.AbstractTemplateConverter` and run the
:class:`~nuketemplate.convert.AbstractTemplateConverter.convert()` function,
like so:

.. code-block:: python

    converter = AbstractTemplateConverter(template.template)
    converter.convert()

To build the Nuke node graph, initialise a
:class:`~nuketemplate.build.NukeGraphBuilder` and run the
:class:`~nuketemplate.build.NukeGraphBuilder.build()` function,
like so:

.. code-block:: python

    builder = NukeGraphBuilder(converter.result)
    builder.build()

.. _Jinja 2: http://jinja.pocoo.org/docs
