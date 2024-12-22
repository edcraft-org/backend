import random
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar

from graphviz import Digraph
from question_generation.input.input_class import Input
from question_generation.input.input_subclasses.custom.adversarial_problem.adversarial_problem import AdversarialProblem
from question_generation.input.input_subclasses.custom.graph.node_type import Node
from question_generation.input.input_subclasses.primitive.int_type import IntInput
from question_generation.quantifiable.quantifiable_class import Quantifiable

class GameTreeInput(Input, AdversarialProblem):
    _exposed_args = ['num_children', 'depth']

    def __init__(self, element_type: Type = IntInput, leaves: List[Node] = None, num_children: int = 2, depth: int = 3):
        self._element_type = element_type
        self._num_children = num_children
        self._depth = depth
        self.input_leaves = leaves
        self.leaves = []
        self._leaf_index = 0
        self._root = self.generate_input()

    def generate_input(self) -> Node:
        """
        Generate input data for the Game Tree.
        """
        return self.create_game_tree(self._depth, self._num_children, 0)

    def create_game_tree(self, depth: int, num_children: int, current_depth: int = 0) -> Node:
        """
        Recursively create a game tree with specified depth and branching factor.
        """
        if current_depth == depth:
            # Terminal node with a value from leaves if provided, otherwise a random value
            if self.input_leaves:
                leaf_value = self.input_leaves.pop(0)
                leaf = Node(self._element_type, value=leaf_value)
                self.leaves.append(leaf_value)
            else:
                leaf = Node(self._element_type)
                self.leaves.append(leaf.value())
            return leaf

        # Internal node with children
        children = [self.create_game_tree(depth, num_children, current_depth + 1) for _ in range(num_children)]
        return Node(children=children)

    def get_state(self) -> Node:
        """
        Return the root of the game tree.
        """
        return self._root

    def get_legal_actions(self, state: Node) -> List[Node]:
        """
        Return the children of the current node as legal actions.
        """
        return state.get_children()

    def apply_action(self, state: Node, action: Node, maximising: bool) -> Node:
        """
        Return the child node as the result of applying the action.
        """
        return action

    def is_terminal(self, state: Node) -> bool:
        """
        Check if the node is a terminal state (i.e., has no children).
        """
        return state.is_terminal()

    def evaluate(self, state: Node, maximising: bool) -> float:
        """
        Evaluate the value of a terminal node.
        For non-terminal nodes, evaluation should not occur but can return a placeholder value.
        """
        if state.is_terminal():
            return state.value()
        raise ValueError("Evaluation called on a non-terminal node.")

    def to_graph(self) -> str:
        """
        Generate a Graphviz representation of the game tree.

        Returns:
            str: The Graphviz representation in SVG format.
        """
        dot = Digraph(format='svg')
        self._add_nodes_edges(dot, self._root, 0)
        return dot.pipe().decode('utf-8')

    def _add_nodes_edges(self, graph: Digraph, node: Node, level: int):
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
            for child in node.get_children():
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
        return self.__class__(element_type=self._element_type, leaves=shuffled_leaves, num_children=self._num_children, depth=self._depth)

    def __str__(self):
        """
        String representation of the leaves for debugging purposes.
        """
        return str(self.leaves)
