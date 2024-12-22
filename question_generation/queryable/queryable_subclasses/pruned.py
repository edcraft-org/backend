from copy import copy
from typing import Any, List
from question_generation.queryable.queryable_class import Queryable

class Pruned(Queryable):
    def __init__(self):
        super().__init__()
        self.variable: str = "pruned_nodes"
        self.pruned_nodes: List[Any] = []

    def prune(self, node: Any):
        self.pruned_nodes.append(copy(node))
