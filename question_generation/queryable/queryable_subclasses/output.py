from typing import Any
from question_generation.queryable.queryable_class import Queryable


class Output(Queryable):
    variable: str = "out"
    out: Any = None

    def output(self, output):
        self.out = output
