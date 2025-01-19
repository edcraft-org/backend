from copy import copy
from typing import Any, Dict, List
from question_generation.graph.diagram_output import DiagramOutput
from question_generation.queryable.queryable_class import Queryable

class Pruned(Queryable):
    def __init__(self):
        super().__init__()
        self.variable: str = "pruned_edges"
        self.pruned_edges: Dict[str, Any] = {
            "value": [],
            "svg": {
                "graph": "",
                "table": "",
            },
        }

    def prune(self, state: Any, next_state:Any):
        self.pruned_edges["value"].append((copy(state), copy(next_state)))

    def prune_graph(self, initial_state: Any, diagramClass: DiagramOutput):
        self.pruned_edges["svg"]["graph"] = diagramClass.to_graph(initial_state, self.pruned_edges["value"])