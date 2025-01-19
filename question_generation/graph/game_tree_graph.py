import string
from typing import List, Tuple, Any
from graphviz import Digraph

from question_generation.graph.diagram_output import DiagramOutput

class GameTreeGraph(DiagramOutput):
    def __init__(self):
        self.count = 0

    def to_graph(self, initial_node: Any, pruned_edges: List[Tuple[Any, Any]] = None) -> str:
        """
        Generate a Graphviz representation of the graph with optional pruned edges highlighted in red.

        Args:
            initial_node (Any): The initial node of the graph.
            pruned_edges (List[Tuple[Any, Any]]): List of pruned edges.

        Returns:
            str: The Graphviz representation in SVG format.
        """
        dot = Digraph(format='svg')
        self._add_nodes_edges(dot, initial_node, 0, pruned_edges)
        return dot.pipe().decode('utf-8')


    def _add_nodes_edges(self, graph: Digraph, node: Any, level: int, pruned_edges: List[Tuple[Any, Any]] = None):
        """
        Recursively add nodes and edges to the Graphviz graph, highlighting pruned edges in red.

        Args:
            graph (Digraph): The Graphviz graph.
            node (Any): The current node.
            level (int): The current level in the tree.
            pruned_edges (List[Tuple[Any, Any]]): List of pruned edges.
            edge_label_counter (int): Counter to generate edge labels.
        """
        if node is not None:
            if hasattr(node, 'is_terminal') and node.is_terminal():
                label = str(node.value()) if node.value() is not None else ""
                shape = 'box'
            else:
                label = ""
                shape = 'triangle' if level % 2 == 0 else 'invtriangle'

            graph.node(str(id(node)), label, shape=shape)
            for child in node.get_actions():
                edge_color = 'red' if pruned_edges and (node, child) in pruned_edges else 'black'
                edge_label = string.ascii_lowercase[self.count % 26]
                graph.edge(str(id(node)), str(id(child)), arrowhead='none', color=edge_color, label=edge_label)
                self.count += 1
                self._add_nodes_edges(graph, child, level + 1, pruned_edges)
