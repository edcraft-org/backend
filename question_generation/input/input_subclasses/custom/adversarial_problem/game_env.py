import random
import string
from typing import Any, Callable, Dict, List, Tuple, Type

from graphviz import Digraph
from question_generation.input.input_class import Input
from question_generation.input.input_subclasses.custom.adversarial_problem.adversarial_element import AdversarialElement
from question_generation.input.input_subclasses.custom.adversarial_problem.adversarial_env import AdversarialEnv
from question_generation.input.input_subclasses.primitive.int_type import IntInput


class GameEnv(AdversarialEnv, Input):
    _exposed_args = ['initial_value', 'get_moves', 'terminal_function', 'evaluate_function']

    def __init__(self, element_type: Type = IntInput, initial_value: Any = None, get_moves: Callable[[Any], List[Any]] = None, terminal_function: Callable[[Any], bool] = None, evaluate_function: Callable[[Any, bool], int] = None):
        self.element_type = element_type
        self.values = []
        self._index = 0
        self.initial_value = initial_value
        self.get_moves = get_moves if get_moves is not None else self.get_possible_actions
        self.terminal_function = terminal_function if terminal_function is not None else self.terminal
        self.evaluate_function = evaluate_function if evaluate_function is not None else self.evaluate
        self.initial = self.generate_input()

    def terminal(self, state: AdversarialElement) -> bool:
        return self.terminal_function(state)

    def evaluate(self, state: AdversarialElement, turn: bool) -> int:
        return self.evaluate_function(state, turn)

    def generate_input(self) -> AdversarialElement:
        """
        Generate input data for the Game Tree.
        """
        current_state = AdversarialElement(self.element_type, value=self.initial_value)
        self.values.append(current_state.value())
        return self.create_new_game_tree(current_state)

    def create_new_game_tree(self, parent: AdversarialElement) -> AdversarialElement:
        """
        Recursively create a game tree with specified depth and branching factor from scratch.
        """

        children = self.get_moves(parent)
        if not children:
            return parent

        for child in children:
            self.values.append(child.value())
            self.create_new_game_tree(child)
        parent.neighbours = children

        return parent

    def to_graph(self, label_edges: bool = False) -> str:
        """
        Generate a Graphviz representation of the game tree.

        Returns:
            str: The Graphviz representation in SVG format.
        """
        def _add_nodes_edges(graph: Digraph, node: AdversarialElement, level: int, label_edges: bool = False, node_map: Dict[str, str] = None, edge_set: set = None):
            """
            Recursively add nodes and edges to the Graphviz graph.

            Args:
                graph (Digraph): The Graphviz graph.
                node (AdversarialElement): The current node.
                level (int): The current level in the tree.
                node_map (Dict[str, str]): A dictionary to keep track of added nodes.
                edge_set (set): A set to keep track of added edges.
            """
            nonlocal count
            if node is not None:
                node_label = str(node.value()) if node.value() is not None else ""
                node_id = f"{level}_{node_label}"

                if node_id not in node_map:
                    shape = 'box'
                    graph.node(node_id, node_label, shape=shape)
                    node_map[node_id] = node_id

                for child in node.get_actions():
                    child_label = str(child.value()) if child.value() is not None else ""
                    child_id = f"{level + 1}_{child_label}"

                    if child_id not in node_map:
                        shape = 'box'
                        graph.node(child_id, child_label, shape=shape)
                        node_map[child_id] = child_id

                    edge = (node_id, child_id)
                    if edge not in edge_set:
                        if label_edges:
                            edge_label = string.ascii_lowercase[count % 26]
                            graph.edge(node_id, child_id, arrowhead='vee', label=edge_label)
                        else:
                            graph.edge(node_id, child_id, arrowhead='vee')
                        edge_set.add(edge)

                    count += 1
                    _add_nodes_edges(graph, child, level + 1, label_edges, node_map, edge_set)

        count = 0
        node_map = {}
        edge_set = set()
        dot = Digraph(format='svg')
        _add_nodes_edges(dot, self.initial, 0, label_edges, node_map, edge_set)
        return dot.pipe().decode('utf-8')

    def generate_options(self) -> 'GameEnv':
        """
        Generate options for the game tree by shuffling the leaves.

        Returns:
            List[GameTreeInput]: The generated options.
        """
        shuffled_values = self.initial_value[:]
        random.shuffle(shuffled_values)
        return self.__class__(element_type=self.element_type, initial_value=shuffled_values, get_moves=self.get_moves, terminal_function=self.terminal_function, evaluate_function=self.evaluate_function)

    def __str__(self):
        """
        String representation of the values for debugging purposes.
        """
        return str(self.values)
