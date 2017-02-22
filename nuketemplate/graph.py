import attr
import networkx as nx

from .exceptions import AbstractGraphError


def is_node_in_nx_graph(instance, attribute, value):
    """
    Input validator for :class:`~nuketemplate.graph.AbstractGraph`.
    Check whether start and end node inputs are part of the graph.

    :param instance: :class:`~nuketemplate.graph.AbstractGraph` instance
    :type instance: :class:`~nuketemplate.graph.AbstractGraph`
    :param _type: Attribute
    :type _type: :class:`~attr.Attribute`
    :param _attr: Input node
    :type _attr: :class:`~nuketemplate.graph.GenericNode` or
                 :class:`~nuketemplate.graph.NukeNode`
    """
    if value not in instance.nx_graph.nodes():
        raise AbstractGraphError('{0} node must be in nx_graph'.format(
            attribute.name.title()))


@attr.s(repr=False)
class GenericNode(object):
    """
    Generic Node, used with :class:`~nuketemplate.graph.AbstractGraph`

    :param name: Node name
    :type name: str
    """
    name = attr.ib()

    def __repr__(self):
        return '<GenericNode: {0}>'.format(self.name)


@attr.s(repr=False)
class NukeNode(GenericNode):
    """
    Nuke Node, used with :class:`~nuketemplate.graph.AbstractGraph`,
    inherits from :class:`~nuketemplate.graph.GenericNode`

    :param name: Node name
    :type name: str
    :param _type: Nuke node type
    :type _type: str
    :param _attr: Nuke node attributes
    :type _attr: dict
    :param _id: Node UUIDs
    :type _id: dict
    """
    _type = attr.ib(repr=False)
    _attr = attr.ib(repr=False, hash=False)
    _id = attr.ib(repr=False, hash=False)

    def __repr__(self):
        return '<NukeNode: {0}>'.format(self.name)


@attr.s
class AbstractGraph(object):
    """
    Abstraction of a NetworkX Directed Graph, adds ``start``, ``end``
    attributes for simplified graph combination.

    :param nx_graph: NetworkX directed graph
    :type nx_graph: :class:`~nx.classes.graph.Graph`
    :param start: Start node
    :type start: :class:`~nuketemplate.graph.GenericNode` or
                 :class:`~nuketemplate.graph.NukeNode`
    :param end: :class:`~nuketemplate.graph.GenericNode` or
                :class:`~nuketemplate.graph.NukeNode`
    :type end: str
    :param end_slot: End node input slot, for nodes with multiple inputs
    :type end_slot: int
    """
    nx_graph = attr.ib(validator=attr.validators.instance_of(
        nx.classes.graph.Graph))
    start = attr.ib(default=None)
    end = attr.ib(default=None)
    end_slot = attr.ib(default=0)

    def __getattribute__(self, name):
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            try:
                return object.__getattribute__(self.nx_graph, name)
            except AttributeError:
                raise AttributeError()
