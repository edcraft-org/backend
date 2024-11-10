from typing import Any
from question_generation.queryable.queryable_class import Queryable


class Step(Queryable):
    variable: str = "history"
    history: list = []

    def query(self, step: int) -> Any:
        states = getattr(self, self.variable)
        if step - 1 < len(states):
            return states[step - 1]
        return None

    def step(self, state: Any):
        self.history.append(state)
