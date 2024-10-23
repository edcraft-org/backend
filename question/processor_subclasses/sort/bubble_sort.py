from functools import singledispatchmethod
from typing import List, Any, Tuple
from question.processor_class import ProcessorClass
from question.queryable_class import QueryableClass
from question.queryable_subclasses.output import OutputQueryableClass
from question.queryable_subclasses.step import StepQueryableClass


class BubbleSortClass(ProcessorClass):
    @singledispatchmethod
    @classmethod
    def process_method(cls, queryable: QueryableClass, input: Any) -> Any:
        return super().process_method(queryable, input)

    @process_method.register
    @classmethod
    def _(cls, queryable: StepQueryableClass, input: List[int], step: int) -> List[int]:
        states: List[Tuple[List[int], int]] = cls.algorithm(input)

        if step - 1 < len(states):
            return states[step - 1]
        return []

    @process_method.register
    @classmethod
    def _(cls, queryable: OutputQueryableClass, input: List[int]) -> List[int]:
        states: List[Tuple[List[int], int]] = cls.algorithm(input)
        return states[-1]

    @classmethod
    def algorithm(cls, input: List[int]) -> List[Tuple[List[int], int]]:
        states: List[Tuple[List[int], int]] = []
        n = len(input)
        for i in range(n):
            for j in range(0, n-i-1):
                if input[j] > input[j+1]:
                    input[j], input[j+1] = input[j+1], input[j]
                    states.append(input.copy())
        return states
