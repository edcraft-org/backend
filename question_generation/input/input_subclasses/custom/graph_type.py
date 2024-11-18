import random
from typing import Any, Dict, Generic, List, Type, TypeVar, Tuple
from question_generation.input.input_class import Input
from question_generation.input.input_subclasses.primitive.int_type import IntInput
from question_generation.quantifiable.quantifiable_class import Quantifiable
from utils.constants import MIN_VALUE, MAX_INT_VALUE

T = TypeVar('T', bound=Quantifiable)

class GraphInput(Input, Quantifiable, Generic[T]):
    def __init__(self, element_type: Type[T] = IntInput, num_nodes: int = None, num_edges: int = None, options: Dict[str, Any] = {}):
        self.element_type = element_type
        self.num_nodes = num_nodes if num_nodes is not None else options.get('num_nodes', 5)
        self.num_edges = num_edges if num_edges is not None else options.get('num_edges', 8)
        self._value = self.generate_input(options)

    def value(self) -> Dict[Any, List[Any]]:
        return self._value

    def generate_input(self, options: Dict[str, Any] = {}) -> Dict[Any, List[Any]]:
        """
        Generate input data for the graph.

        Args:
            options (Dict[str, Any]): Additional options for generating input, including:
                - num_nodes (int): The number of nodes in the graph.
                - num_edges (int): The number of edges in the graph.

        Returns:
            Dict[Any, List[Any]]: The generated adjacency list representing the graph.
        """
        num_nodes = options.get('num_nodes', self.num_nodes)
        num_edges = options.get('num_edges', self.num_edges)

        adjacency_list = {i: [] for i in range(num_nodes)}
        edges = set()
        while len(edges) < num_edges:
            node1 = random.randint(0, num_nodes - 1)
            node2 = random.randint(0, num_nodes - 1)
            if node1 != node2 and (node1, node2) not in edges and (node2, node1) not in edges:
                adjacency_list[node1].append(node2)
                adjacency_list[node2].append(node1)  # For undirected graph
                edges.add((node1, node2))
        return adjacency_list

    def generate_options(self, answer: Dict[Any, List[Any]] = None, options: Dict[str, Any] = {}) -> List[Dict[Any, List[Any]]]:
        """
        Generate options for generating input data.

        Args:
            answer (Dict[Any, List[Any]]): The answer for the input data.
            options (Dict[str, Any]): Options for generating input, including:
                - num_options (int): The number of options to generate.
                - use_existing (bool): Whether to shuffle the existing graph instead of creating a new graph.

        Returns:
            List[Dict[Any, List[Any]]]: The generated options.
        """
        if answer is None:
            answer = self.generate_input()

        num_options = options.get('num_options', 4)
        use_existing = options.get('use_existing', True)
        num_nodes = options.get('num_nodes', self.num_nodes)
        num_edges = options.get('num_edges', self.num_edges)

        generated_options = set()
        generated_options.add(tuple((k, tuple(v)) for k, v in answer.items()))

        if use_existing:
            while len(generated_options) < num_options:
                shuffled_answer = {k: random.sample(v, len(v)) for k, v in answer.items()}
                generated_options.add(tuple((k, tuple(v)) for k, v in shuffled_answer.items()))
        else:
            while len(generated_options) < num_options:
                option = self.generate_input({'num_nodes': num_nodes, 'num_edges': num_edges})
                generated_options.add(tuple((k, tuple(v)) for k, v in option.items()))

        return [{k: list(v) for k, v in dict(option).items()} for option in generated_options]

    def __str__(self) -> str:
        return f"GraphInput(num_nodes={self.num_nodes}, num_edges={self.num_edges}, value={self._value})"