from copy import copy
from typing import Any, Dict
from question_generation.graph.diagram_output import DiagramOutput
from question_generation.queryable.queryable_class import Queryable


class Output(Queryable):
    def __init__(self):
        super().__init__()
        self.variable: str = "out"
        self.out: Dict[str, Any] = {
            "value": None,
            "svg": {
                "graph": "",
                "table": "",
            },
        }

    def output(self, output):
        self.out["value"] = copy(output)

    def output_graph(self, initial_state: Any, diagramClass: DiagramOutput):
        self.out["svg"]["graph"] = diagramClass.to_graph(tree=initial_state)