import subprocess
import networkx as nx

from .graph import AbstractGraph
from .graph import NukeNode
from .exceptions import AbstractTemplateError

from nuketemplate import logger


class AbstractTemplateConverter(object):
    """
    Template to Graph Converter

    :param template: JSON Template
    :type template: list, dict
    :param start: Start characters, default: ``>>``
    :type start: str
    :param end: End characters, default: ``<<``
    :type end: str
    """
    def __init__(self, template, start='>>', end='<<'):
        self.start = start
        self.end = end
        self.template = template
        self.subgraphs = []
        self.result = None

    def _convert_template_to_graph(self, template):
        """
        Private conversion helper function, create an
        :class:`~nx.classes.graph.Graph` and start
        :func:`nuketemplate.convert.AbstractTemplateConverter._add_nodes()`.

        :param template: JSON Template
        :type template: list, dict
        """
        graph = AbstractGraph(nx_graph=nx.DiGraph())
        self._add_nodes(graph, template[self.start], template)
        self.subgraphs.append(graph)

    def _add_nodes(self, graph, node, template):
        """
        Private conversion helper function, recursively add nodes and edges to
        ``graph``.

        :param graph: NetworkX graph
        :type graph: :class:`~nx.classes.graph.Graph`
        :param node: Start node
        :type node: str
        :param template: JSON template
        :type template: list, dict
        """
        nuke_node = NukeNode(name=node,
                             attr=template[node].get('attr', {}),
                             type=template[node].get('type', {}),
                             id={})
        graph.nx_graph.add_node(nuke_node)
        if not graph.start:
            graph.start = nuke_node
        for input_idx, input in enumerate(template[node]['inputs']):
            if input != self.end:
                graph.nx_graph.add_edge(nuke_node,
                                        self._add_nodes(graph,
                                                        input,
                                                        template),
                                        input=input_idx)
            else:
                graph.end = nuke_node
                graph.end_slot = input_idx
        return nuke_node

    def _combine_graphs(self):
        """
        Combine graphs if the template consists of multiple sub graphs.
        """
        self.subgraphs.reverse()
        self.result = self.subgraphs.pop()
        while self.subgraphs:
            subgraph = self.subgraphs.pop()
            composed_graphs = nx.compose(self.result.nx_graph,
                                         subgraph.nx_graph)
            composed_graphs.add_edge(self.result.end,
                                     subgraph.start,
                                     input=subgraph.end_slot)
            self.result = AbstractGraph(nx_graph=composed_graphs,
                                        start=self.result.start,
                                        end=subgraph.end)

    def convert(self):
        """
        Convert the JSON template into an
        :class:`~nuketemplate.graph.AbstractGraph`, if the template consists
        of multiple sub graphs, convert and combine otherwise convert in one
        pass.
        """
        if isinstance(self.template, list):
            for sub_template in self.template:
                self._convert_template_to_graph(sub_template)
        elif isinstance(self.template, dict):
            self._convert_template_to_graph(self.template)
        else:
            AbstractTemplateError('Template must be either list or dict')
        num_nodes_p_subgraph = [sg.number_of_nodes() for sg in self.subgraphs]
        logger.info('Number of sub graphs: {}'.format(len(self.subgraphs)))
        logger.info('Number of nodes per sub graph: {}'.format(num_nodes_p_subgraph))
        logger.info('Total number of nodes: {}'.format(
            sum(num_nodes_p_subgraph)))
        self._combine_graphs()

    def to_dot(self, filename='graph.dot'):
        """
        Save the converted graph to a dot file at location ``filename``

        :param filename: Filename
        :type filename: str
        """
        nx.drawing.nx_pydot.write_dot(self.result.nx_graph, filename)

    def to_png(self, filename='graph.png'):
        """
        Save the converted graph to a png file at location ``filename``

        :param filename: Filename
        :type filename: str
        """
        self.to_dot()
        subprocess.call(['dot', '-Tpng', 'graph.dot', '-o', 'graph.png'])
