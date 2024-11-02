from abc import abstractmethod
from typing import Any, List, Tuple
from question.queryable_subclasses.output import OutputQueryable


class SortOutputQueryable(OutputQueryable):
    def query(self, input: List[int]) -> List[int]:
        return super().query(input)

    @abstractmethod
    def algo(self, input: List[int]) -> Any:
        raise NotImplementedError("Method 'algo' must be implemented in subclass")

    def output(self, input: List[int]) -> List[int]:
        states: List[Tuple[List[int], int]] = self.algo(input)
        return states[-1][0]
