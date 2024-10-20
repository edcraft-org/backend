from functools import singledispatchmethod
from typing import List, Any, Tuple
from question.processor_class import ProcessorClass
from question.queryable_class import QueryableClass
from question.queryable_subclasses.output import OutputQueryableClass
from question.queryable_subclasses.step import StepQueryableClass

class InsertionSortClass(ProcessorClass):
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
    def algorithm(cls, input: List[int]) -> List[Tuple[List[int], int]] :
        states: List[Tuple[List[int], int]] = []

        for insert_index in range(1, len(input)):
            insert_value = input[insert_index]
            while insert_index > 0 and insert_value < input[insert_index - 1]:
                input[insert_index] = input[insert_index - 1]
                insert_index -= 1
            input[insert_index] = insert_value
            states.append(input.copy())
        return states