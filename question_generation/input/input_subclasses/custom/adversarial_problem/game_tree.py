import random
from typing import List, Type

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

        children = [self.create_game_tree_from_scratch(depth, num_children, current_depth + 1) for _ in range(num_children)]
        return AdversarialElement(neighbours=children)

    def create_game_tree_from_leaves(self, depth: int, num_children: int, current_depth: int = 0) -> AdversarialElement:
        """
        Recursively create a game tree with specified depth and branching factor using existing leaves.
        """
        if current_depth + 1 == depth:
            leaf_value = self.leaves[self._leaf_index]
            leaf = AdversarialElement(self.element_type, value=leaf_value)
            self._leaf_index += 1
            return leaf

        children = [self.create_game_tree_from_leaves(depth, num_children, current_depth + 1) for _ in range(num_children)]
        return AdversarialElement(neighbours=children)

    def to_graph(self) -> str:
        """
        Generate a Graphviz representation of the game tree.

        Returns:
            str: The Graphviz representation in SVG format.
        """
        dot = Digraph(format='svg')
        self._add_nodes_edges(dot, self.initial, 0)
        return dot.pipe().decode('utf-8')

    def _add_nodes_edges(self, graph: Digraph, node: AdversarialElement, level: int):
        """
        Recursively add nodes and edges to the Graphviz graph.

        Args:
            graph (Digraph): The Graphviz graph.
            node (Node): The current node.
            level (int): The current level in the tree.
        """
        if node is not None:
            if node.is_terminal():
                label = str(node.value()) if node.value() is not None else ""
                shape = 'box'
            else:
                label = ""
                shape = 'triangle' if level % 2 == 0 else 'invtriangle'

            graph.node(str(id(node)), label, shape=shape)
            for child in node.get_actions():
                graph.edge(str(id(node)), str(id(child)), arrowhead='none')
                self._add_nodes_edges(graph, child, level + 1)

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
