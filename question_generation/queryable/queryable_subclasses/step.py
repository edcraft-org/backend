from copy import copy
from typing import Any, Dict
from question_generation.queryable.queryable_class import Queryable


class Step(Queryable):
    def __init__(self):
        super().__init__()
        self.variable: str = "history"
        self.history: Dict[str, Any] = {
            "value": [],
            "svg": {
                "graph": "",
                "table": "",
            },
        }

    def query(self, step: int) -> Any:
        states = super().query()
        try:
            return {
                "value": states["value"][step - 1],
                "svg": states["svg"],
            }
        except IndexError:
            return {
                "value": None,
                "svg": states["svg"],
            }

    def step(self, state: Any):
        self.history["value"].append(copy(state))
