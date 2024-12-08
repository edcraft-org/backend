import random
from typing import Any, Dict, Generic, List, Type, TypeVar
from question_generation.input.input_class import Input
from question_generation.input.input_subclasses.custom.traversable.traversable import Traversable
from question_generation.input.input_subclasses.primitive.int_type import IntInput
from question_generation.quantifiable.quantifiable_class import Quantifiable
from graphviz import Digraph

T = TypeVar('T', bound=Quantifiable)

class AdjacencyListInput(Input, Traversable, Generic[T]):
    def __init__(self, node_labels: List[Any] = [], element_type: Type[T] = IntInput, num_nodes: int = None, num_edges: int = None, options: Dict[str, Any] = {}):
        self.element_type = element_type
        self.num_nodes = num_nodes if num_nodes is not None else options.get('num_nodes', 7)
        self.num_edges = num_edges if num_edges is not None else options.get('num_edges', 6)
        self.node_labels = []
        self._value = self.generate_input(options)

    def get_neighbors(self, node: Any) -> List[Any]:
        return self._value.get(node, [])

    def get_start(self) -> Any:
        if self.node_labels:
            return self.node_labels[0]
        return None

    def generate_input(self, options: Dict[str, Any] = {}) -> Dict[Any, List[Any]]:
        """
        Generate input data for the Adjacency List.

        Args:
            options (Dict[str, Any]): Additional options for generating input, including:
                - num_nodes (int): The number of nodes in the Adjacency List.
                - num_edges (int): The number of edges in the Adjacency List.

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

    def generate_options(self, options: Dict[str, Any] = {}) -> 'AdjacencyListInput':

        """
        Generate options for generating input data.

        Args:
            options (Dict[str, Any]): Options for generating input, including:
                - num_options (int): The number of options to generate.

        Returns:
            List[Dict[Any, List[Any]]]: The generated options.
        """
        shuffled_labels = self.node_labels[:]
        random.shuffle(shuffled_labels)
        return self.__class__(node_labels=shuffled_labels, element_type=self.element_type, num_nodes=self.num_nodes, num_edges=self.num_edges, options=options)

    def to_graph(self) -> str:
        """
        Generate a Graphviz representation of the adjacency list.

        Returns:
            str: The Graphviz representation in SVG format.
        """
        dot = Digraph(format='svg')
        for node, neighbors in self._value.items():
            dot.node(str(id(node)), str(node))
            for neighbor in neighbors:
                dot.edge(str(id(node)), str(id(neighbor)))
        return dot.pipe().decode('utf-8')

    def __str__(self) -> str:
        return f"{self._value}"
