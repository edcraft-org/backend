from copy import copy
from typing import Any
from question_generation.queryable.queryable_class import Queryable


class Step(Queryable):
    def __init__(self):
        super().__init__()
        self.variable: str = "history"
        self.history: list = []

    def query(self, step: int) -> Any:
        states = super().query()
        try:
            return states[step - 1]
        except IndexError:
            return None

    def step(self, state: Any):
        self.history.append(copy(state))
