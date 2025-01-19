from typing import Type
from graphviz import Digraph

from question_generation.graph.diagram_output import DiagramOutput
from question_generation.input.input_subclasses.custom.decision_tree.tree_node import DecisionTreeNode

class DecisionTreeGraph(DiagramOutput):
    def to_graph(self, tree: Type['DecisionTreeNode'], parent=None, graph=None, node_id=0):
        """
        Generate a Graphviz representation of the graph

        Returns:
            str: The Graphviz representation in SVG format.
        """
        node_label = f"{tree.attribute}_{node_id}" if tree.attribute else f"{tree.label}_{node_id}"
        if graph is None:
            graph = Digraph(format='svg', engine='dot')
            graph.node(node_label, f"{tree.attribute}?" if tree.attribute else str(tree.label), shape='box')

        for value, child in tree.children.items():
            child_node_label = f"{child.attribute}_{node_id + 1}" if child.attribute else f"{child.label}_{node_id + 1}"
            child_node_shape = 'box' if child.attribute else 'plaintext'
            graph.node(child_node_label, f"{child.attribute}?" if child.attribute else str(child.label), shape=child_node_shape)
            graph.edge(node_label, child_node_label, label=str(value))
            self.to_graph(child, parent=child_node_label, graph=graph, node_id=node_id + 1)
        return graph.pipe().decode('utf-8')