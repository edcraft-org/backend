import random
import string
from typing import Any, Dict, List, Type

from graphviz import Digraph
from question_generation.input.input_class import Input
from question_generation.input.input_subclasses.custom.adversarial_problem.adversarial_element import AdversarialElement
from question_generation.input.input_subclasses.custom.adversarial_problem.adversarial_env import AdversarialEnv
from question_generation.input.input_subclasses.primitive.int_type import IntInput


class GoldCoinGameEnv(AdversarialEnv, Input):
    _exposed_args = ['initial_value', 'move_spaces', 'take_leftmost']

    # move_spaces index 0: left, index 1: right; values -1 indicates any number of moves [1, 0]
    # leftmost indicates whether coin can be taken from leftmost or rightmost position True
    def __init__(self, element_type: Type = IntInput, initial_value: Any = None, move_spaces: List[str] = [-1, 0], take_leftmost: bool = True):
        self.element_type = element_type
        self.values = []
        self._index = 0
        self.initial_value = initial_value
        self.move_spaces = move_spaces
        self.take_leftmost = take_leftmost
        self.initial = self.generate_input()

    def terminal(self, state: AdversarialElement) -> bool:
        return "G" not in state.value()

    def evaluate(self, state: AdversarialElement, turn: bool) -> int:
        if state.is_terminal():
            return -1 if turn else 1
        return 0

    def get_moves(self, state: AdversarialElement) -> List[AdversarialElement]:
        children = []
        if self.terminal(state):
            return children
        state_list = state.value()

        removal_position = 0 if self.take_leftmost else -1
        if state_list[removal_position] in {"C", "G"}:
            new_state = state_list[:]
            new_state[removal_position] = "_"
            children.append(AdversarialElement(value=new_state))

        if self.move_spaces[0] != 0:
            for i in range(1, len(self.initial_value)):
                if state_list[i] in {"C", "G"}:
                    max_left_moves = self.move_spaces[0] if self.move_spaces[0] != -1 else i
                    for j in range(i - 1, max(-1, i - max_left_moves - 1), -1):
                        if state_list[j] == "_":
                            new_state = state_list[:]
                            new_state[j] = new_state[i]
                            new_state[i] = "_"
                            children.append(AdversarialElement(value=new_state))
                        else:
                            break

        if self.move_spaces[1] != 0:
            for i in range(len(self.initial_value) - 2, -1, -1):
                if state_list[i] in {"C", "G"}:
                    max_right_moves = self.move_spaces[1] if self.move_spaces[1] != -1 else len(self.initial_value) - i - 1
                    for j in range(i + 1, min(len(self.initial_value), i + max_right_moves + 1)):
                        if state_list[j] == "_":
                            new_state = state_list[:]
                            new_state[j] = new_state[i]
                            new_state[i] = "_"
                            children.append(AdversarialElement(value=new_state))
                        else:
                            break

        return children

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

    def generate_options(self) -> 'GoldCoinGameEnv':
        """
        Generate options for the game tree by shuffling the leaves.

        Returns:
            List[GameTreeInput]: The generated options.
        """
        shuffled_values = self.initial_value[:]
        random.shuffle(shuffled_values)
        return self.__class__(element_type=self.element_type, initial_value=shuffled_values, move_spaces=self.move_spaces, take_leftmost=self.take_leftmost)

    def __str__(self):
        """
        String representation of the values for debugging purposes.
        """
        return str(self.values)
