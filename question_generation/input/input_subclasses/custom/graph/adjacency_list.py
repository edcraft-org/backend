import random
from typing import Any, Dict, Generic, List, Type, TypeVar
from question_generation.input.input_class import Input
from question_generation.input.input_subclasses.custom.graph.graph_env import GraphEnv
from question_generation.input.input_subclasses.primitive.int_type import IntInput
from question_generation.quantifiable.quantifiable_class import Quantifiable
from graphviz import Digraph

from utils.conversion_helper import convert_keys

T = TypeVar('T', bound=Quantifiable)

class AdjacencyListInput(GraphEnv, Input, Generic[T]):
    _exposed_args = ['num_nodes', 'num_edges']

    def __init__(self, node_labels: List[Any] = [], element_type: Type[T] = IntInput, num_nodes: int = 7, num_edges: int = 6, value: Dict[Any, List[Any]] = None):
        self.element_type = element_type
        self.num_nodes = num_nodes
        self.num_edges = num_edges
        self.node_labels = node_labels
        self.value = convert_keys(value) if value is not None else self.generate_input()
        super().__init__(self.value, self.initial(), None)

    def initial(self) -> Any:
        return self.node_labels[0] if self.node_labels else None

    def generate_input(self) -> Dict[Any, List[Any]]:
        """
        Generate input data for the Adjacency List.

        Returns:
            Dict[Any, List[Any]]: The generated adjacency list representing the Adjacency List.
        """
        if not self.node_labels:
            unique_labels = set()
            while len(unique_labels) < self.num_nodes:
                label = self.element_type()
                unique_labels.add(label)
            self.node_labels = list(unique_labels)

        adjacency_list = {label: [] for label in self.node_labels}

        for new_node_index in range(1, self.num_nodes):
            new_node = self.node_labels[new_node_index]
            while True:
                parent_node_index = random.randint(0, new_node_index - 1)
                parent_node = self.node_labels[parent_node_index]
                if len(adjacency_list[parent_node]) < 2:
                    adjacency_list[parent_node].append(new_node)
                    break
        return adjacency_list

    def generate_options(self) -> 'AdjacencyListInput':
        """
        Generate options for generating input data.
        """
        shuffled_labels = self.node_labels[:]
        random.shuffle(shuffled_labels)
        return self.__class__(node_labels=shuffled_labels, element_type=self.element_type, num_nodes=self.num_nodes, num_edges=self.num_edges)

    def to_graph(self) -> str:
        """
        Generate a Graphviz representation of the adjacency list.

        Returns:
            str: The Graphviz representation in SVG format.
        """
        dot = Digraph(format='svg')
        for node, neighbors in self.value.items():
            dot.node(str(id(node)), str(node))
            for neighbor in neighbors:
                dot.edge(str(id(node)), str(id(neighbor)))
        return dot.pipe().decode('utf-8')

    def __str__(self) -> str:
        return f"{self.value}"
