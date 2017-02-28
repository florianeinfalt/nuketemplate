import attr
import networkx as nx
from nukecontexts import ctx
from nuketemplate import import_nuke, logger

from .graph import AbstractGraph
from .exceptions import AbstractGraphError

nuke = import_nuke()


@attr.s(repr=False)
class NukeGraphBuilder(object):
    """
    NukeGraphBuilder, convert an :class:`~nuketemplate.graph.AbstractGraph`
    to a Nuke compositing script

    :param abstract_graph: Abstract graph
    :type abstract_graph: :class:`~nuketemplate.graph.AbstractGraph`
    """
    abstract_graph = attr.ib(validator=attr.validators.instance_of(
        AbstractGraph))

    def _check_cycles(self, graph):
        """
        Given a NetworkX graph, check for circular dependencies within the
        graph and raise :class:`~nuketemplate.exceptions.AbstractGraphError`
        if any circles are found.

        :param graph: NetworkX graph
        :type graph: :class:`~nx.classes.graph.Graph`
        """
        if list(nx.simple_cycles(graph)):
            raise AbstractGraphError('Cycles in graph')

    def _autoplace(self, nodes):
        """
        Given a list of nodes, apply Nuke's auto placement.

        :param: nodes: Nodes
        :type nodes: list
        """
        for node in nodes:
            node.autoplace()

    def _build_node(self, node):
        """
        Given a ``node`` name, build the node in Nuke and return the Nuke node.

        :param node: Node name
        :type node: str
        :return: Node
        :rtype: :class:`~nuke.Node`
        """
        logger.info('Building node: {0}'.format(node))
        nx_graph = self.abstract_graph.nx_graph

        for selected_node in nuke.selectedNodes():
            selected_node.setSelected(False)
        parent = node.build()
        inputs = [edge for edge in nx_graph.edges(data=True)
                  if edge[0] == node]
        for input in inputs:
            child = self._build_node(input[1])
            logger.info('{0} >> {1} >> {2}'.format(
                input[1],
                input[2]['input'],
                node))
            parent.setInput(input[2]['input'], child)
        return parent

    def build(self):
        """
        Build the Nuke node graph from the object's ``abstract_graph``
        """
        logger.info('Building...')
        self._check_cycles(self.abstract_graph.nx_graph)
        with ctx.inventory('new_nodes'):
            self._build_node(self.abstract_graph.start)
        self._autoplace(new_nodes)
        logger.info('Total number of nodes built: {}'.format(len(new_nodes)))

    def __repr__(self):
        return '<NukeGraphBuilder: {0}>'.format(self.abstract_graph)
