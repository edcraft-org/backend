import random
import string
from typing import List, Tuple, Type

from graphviz import Digraph
from question_generation.input.input_class import Input
from question_generation.input.input_subclasses.custom.adversarial_problem.adversarial_element import AdversarialElement
from question_generation.input.input_subclasses.custom.adversarial_problem.adversarial_env import AdversarialEnv
from question_generation.input.input_subclasses.primitive.int_type import IntInput

class GameTreeInput(AdversarialEnv, Input):
    _exposed_args = ['num_children', 'depth']

    def __init__(self, element_type: Type = IntInput, leaves: List[AdversarialElement] = None, num_children: int = 3, depth: int = 2):
        self.element_type = element_type
        self.num_children = num_children
        self.depth = depth
        self.leaves = leaves if leaves is not None else []
        self._leaf_index = 0
        self.count = 0
        self.edge_label_mapping = {}
        self.initial = self.generate_input()

    def generate_input(self) -> AdversarialElement:
        """
        Generate input data for the Game Tree.
        """
        if self.leaves:
            return self.create_game_tree_from_leaves(self.depth, self.num_children, 0)
        else:
            return self.create_game_tree_from_scratch(self.depth, self.num_children, 0)

    def create_game_tree_from_scratch(self, depth: int, num_children: int, current_depth: int = 0) -> AdversarialElement:
        """
        Recursively create a game tree with specified depth and branching factor from scratch.
        """
        if current_depth + 1 == depth:
            leaf = AdversarialElement(self.element_type)
            self.leaves.append(leaf.value())
            return leaf

        parent = AdversarialElement()
        children = []
        for i in range(num_children):
            child = self.create_game_tree_from_scratch(depth, num_children, current_depth + 1)
            children.append(child)
            edge_label = string.ascii_lowercase[len(self.edge_label_mapping) % 26]
            self.edge_label_mapping[(parent.id, child.id)] = edge_label  # Add edge to mapping
        parent.neighbours = children
        return parent

    def create_game_tree_from_leaves(self, depth: int, num_children: int, current_depth: int = 0) -> AdversarialElement:
        """
        Recursively create a game tree with specified depth and branching factor using existing leaves.
        """
        if current_depth + 1 == depth:
            leaf_value = self.leaves[self._leaf_index]
            leaf = AdversarialElement(self.element_type, value=leaf_value)
            self._leaf_index += 1
            return leaf

        parent = AdversarialElement()
        children = []
        for i in range(num_children):
            count = self.count
            self.count += 1
            child = self.create_game_tree_from_leaves(depth, num_children, current_depth + 1)
            children.append(child)
            edge_label = string.ascii_lowercase[count % 26]
            self.edge_label_mapping[(parent.id, child.id)] = edge_label
        parent.neighbours = children
        return parent

    def get_edge_label(self, state: AdversarialElement, child: AdversarialElement) -> str:
        """
        Get the edge label between two nodes.
        """
        return self.edge_label_mapping.get((state.id, child.id), "")

    def to_graph(self, label_edges: bool = False) -> str:
        """
        Generate a Graphviz representation of the game tree.

        Returns:
            str: The Graphviz representation in SVG format.
        """
        def _add_nodes_edges(graph: Digraph, node: AdversarialElement, level: int, label_edges: bool = False):
            """
            Recursively add nodes and edges to the Graphviz graph.

            Args:
                graph (Digraph): The Graphviz graph.
                node (Node): The current node.
                level (int): The current level in the tree.
            """
            nonlocal count
            if node is not None:
                if node.is_terminal():
                    label = str(node.value()) if node.value() is not None else ""
                    shape = 'box'
                else:
                    label = ""
                    shape = 'triangle' if level % 2 == 0 else 'invtriangle'

                graph.node(str(id(node)), label, shape=shape)
                for child in node.get_actions():
                    if label_edges:
                        edge_label = string.ascii_lowercase[count % 26]
                        graph.edge(str(id(node)), str(id(child)), arrowhead='none', label=edge_label)
                    else:
                        graph.edge(str(id(node)), str(id(child)), arrowhead='none')
                    count += 1
                    _add_nodes_edges(graph, child, level + 1, label_edges)

        count = 0
        dot = Digraph(format='svg')
        _add_nodes_edges(dot, self.initial, 0, label_edges)
        return dot.pipe().decode('utf-8')



    def generate_options(self) -> 'GameTreeInput':
        """
        Generate options for the game tree by shuffling the leaves.

        Returns:
            List[GameTreeInput]: The generated options.
        """
        shuffled_leaves = self.leaves[:]
        random.shuffle(shuffled_leaves)
        return self.__class__(element_type=self.element_type, leaves=shuffled_leaves, num_children=self.num_children, depth=self.depth)

    def __str__(self):
        """
        String representation of the leaves for debugging purposes.
        """
        return str(self.leaves)
