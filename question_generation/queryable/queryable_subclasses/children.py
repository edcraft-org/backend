import random
from typing import Any, Callable, Dict, List
from question_generation.queryable.queryable_class import Queryable


class DirectChildren(Queryable):
    def __init__(self):
        super().__init__()
        self.variable: str = "direct_children"
        self.direct_children: Dict[str, Any] = {
            "value": {},
            "svg": {
                "graph": "",
                "table": "",
            },
        }
        self.get_children: Callable[[Any], Any] = None
        self.values: List[Any] = []

    def query(self, state_value: Any) -> Any:
        states = super().query()
        print(state_value)
        print(self.get_children(state_value))
        try:
            return {
                "value": self.get_children(state_value),
                "svg": states["svg"],
            }
        except IndexError:
            return {
                "value": None,
                "svg": states["svg"],
            }

    def children(self, values: List[Any], get_direct_children_function: Callable[[Any], Any]):
        self.values = values
        self.get_children = get_direct_children_function

    def generate_input(self) -> Any:
        if not self.values:
            raise ValueError("No values available to select from.")
        return random.choice(self.values)