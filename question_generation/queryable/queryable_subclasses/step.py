from typing import Any
from question_generation.queryable.queryable_class import Queryable


class Step(Queryable):
    def __init__(self):
        super().__init__()
        self.variable: str = "history"
        self.history: list = []

    def query(self, step: int) -> Any:
        states = getattr(self, self.variable)
        print(states)
        if step - 1 < len(states):
            return states[step - 1]
        return None

    def step(self, state: Any):
        self.history.append(state)
