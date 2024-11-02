from abc import abstractmethod
from typing import List, Tuple

from question.queryable_subclasses.step import StepQueryable


class SortStepQueryable(StepQueryable):
    def query(self, input: List[int], step: int) -> List[int]:
        return super().query(input, step)

    @abstractmethod
    def algo(self, input: List[int]) -> List[Tuple[List[int], int]]:
        raise NotImplementedError("Method 'algo' must be implemented in subclass")

    def step(self, input: List[int], step: int) -> List[int]:
        states: List[Tuple[List[int], int]] = self.algo(input)
        answer = []
        if step - 1 < len(states):
            answer = states[step - 1][0]
        return answer
