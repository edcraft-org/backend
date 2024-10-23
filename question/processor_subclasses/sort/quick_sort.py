from functools import singledispatchmethod
from typing import List, Any, Tuple
from question.processor_class import ProcessorClass
from question.queryable_class import QueryableClass
from question.queryable_subclasses.output import OutputQueryableClass
from question.queryable_subclasses.step import StepQueryableClass

class QuickSortClass(ProcessorClass):
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

        def quick_sort(arr: List[int], low: int, high: int):
            if low < high:
                pi = partition(arr, low, high)
                quick_sort(arr, low, pi - 1)
                quick_sort(arr, pi + 1, high)
                states.append(arr.copy())

        def partition(arr: List[int], low: int, high: int) -> int:
            pivot = arr[high]
            i = low - 1
            for j in range(low, high):
                if arr[j] < pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            return i + 1

        quick_sort(input, 0, len(input) - 1)
        return states