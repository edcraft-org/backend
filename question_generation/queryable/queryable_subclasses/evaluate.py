from copy import copy
from typing import Any, Callable, Dict
from question_generation.queryable.queryable_class import Queryable


class Evaluate(Queryable):
    def __init__(self):
        super().__init__()
        self.variable: str = "evaluation_data"
        self.evaluation_data: Dict[str, Any] = {
            "value": None,
            "svg": {
                "graph": "",
                "table": "",
            },
        }
        self.evaluation_function: Callable[[Any, Any], Any] = None

    def query(self, example: Any) -> Any:
        states = super().query()
        return {
            "value": self.evaluation_function(states["value"], example),
            "svg": states["svg"],
        }

    def evaluate(self, state: Any, evaluation_function: Callable[[Any, Any], Any], generate_input: Callable[[], Any]):
        self.evaluation_data["value"] = state
        self.evaluation_function = evaluation_function
        self.generate_input_function = generate_input

    def generate_input(self) -> int:
        return self.generate_input_function() if self.generate_input_function else None
