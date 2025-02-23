from copy import copy
import random
from typing import Any, Callable, Dict, List
from question_generation.queryable.queryable_class import Queryable


class Entropy(Queryable):
    def __init__(self):
        super().__init__()
        self.variable: str = "entropy_value"
        self.entropy_value: Dict[str, Any] = {
            "value": {},
            "svg": {
                "graph": "",
                "table": "",
            },
        }
        self.keys: List[str] = []

    def query(self, key: str) -> Any:
        states = super().query()
        try:
            return {
                "value": states["value"][key],
                "svg": states["svg"],
            }
        except IndexError:
            return {
                "value": None,
                "svg": states["svg"],
            }

    def entropy(self, data: List[Dict[str, Any]], entropy_function: Callable[[Any], Any]):
        if data:
            self.keys = list(data[0].keys())
        else:
            self.keys = []
        self.entropy_value["value"] = entropy_function(data)

    def generate_input(self) -> int:
        if not self.keys:
            raise ValueError("No keys available to select from.")
        return random.choice(self.keys)