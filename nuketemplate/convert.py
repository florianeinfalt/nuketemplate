import networkx as nx

from .graph import AbstractGraph
from .graph import NukeNode


class AbstractTemplateConverter(object):
    def __init__(self, template, start='>>', end='<<'):
        self.start = start
        self.end = end
        self.template = template
        self.subgraphs = []
        self.result = None

    def _convert_template_to_graph(self, template):
        subgraph = AbstractGraph(nx_graph=nx.DiGraph())
        self._add_nodes(subgraph, template[self.start], template)
        self.subgraphs.append(subgraph)

    def _add_nodes(self, subgraph, node, template):
        nuke_node = NukeNode(name=node,
                             attr=template[node]['attr'],
                             type=template[node]['type'],
                             id={})
        subgraph.nx_graph.add_node(nuke_node)
        if not subgraph.start:
            subgraph.start = nuke_node
        for input_idx, input in enumerate(template[node]['inputs']):
            if input != self.end:
                subgraph.nx_graph.add_edge(nuke_node,
                                           self._add_nodes(subgraph,
                                                           input,
                                                           template),
                                           input=input_idx)
            else:
                subgraph.end = nuke_node
                subgraph.end_slot = input_idx
        return nuke_node

    def _combine_graphs(self):
        self.subgraphs = self.subgraphs[::-1]
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
        for sub_template in self.template:
            self._convert_template_to_graph(sub_template)
        print len(self.subgraphs),\
              [sg.number_of_nodes() for sg in self.subgraphs]
        self._combine_graphs()
