from typing import Any
from question_generation.queryable.queryable_class import Queryable


class Output(Queryable):
    def __init__(self):
        super().__init__()
        self.variable: str = "out"
        self.out: Any = None

    def output(self, output):
        self.out = output
