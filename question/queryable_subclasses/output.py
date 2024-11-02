from abc import abstractmethod
from typing import Any
from question.queryable_class import Queryable


class OutputQueryable(Queryable):
    def query(self, input: Any) -> Any:
        return self.output(input)

    @abstractmethod
    def algo(self, input: Any) -> Any:
        raise NotImplementedError("Method 'algo' must be implemented in subclass")

    @abstractmethod
    def output(self, input: Any) -> Any:
        raise NotImplementedError("Method 'output' must be implemented in subclass")
