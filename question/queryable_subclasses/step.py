from abc import abstractmethod
from typing import Any
from question.queryable_class import Queryable


class StepQueryable(Queryable):
    def query(self, input: Any, step: int) -> Any:
        return self.step(input, step)

    @abstractmethod
    def algo(self, input: Any) -> Any:
        raise NotImplementedError("Method 'algo' must be implemented in subclass")

    @abstractmethod
    def step(self, input: Any, step: int) -> Any:
        raise NotImplementedError("Method 'step' must be implemented in subclass")
