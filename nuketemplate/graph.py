import attr
import networkx as nx

from .exceptions import AbstractGraphError


def is_node_in_nx_graph(instance, attribute, value):
    if value not in instance.nx_graph.nodes():
        raise AbstractGraphError('{0} node must be in nx_graph'.format(
            attribute.name.title()))


@attr.s
class GenericNode(object):
    name = attr.ib()


@attr.s
class NukeNode(GenericNode):
    _type = attr.ib(repr=False)
    _attr = attr.ib(repr=False, hash=False)
    _id = attr.ib(repr=False, hash=False)


@attr.s
class AbstractGraph(object):
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
