from functools import singledispatchmethod
from typing import List, Any, Tuple
from question.processor_class import ProcessorClass
from question.queryable_class import QueryableClass
from question.queryable_subclasses.output import OutputQueryableClass
from question.queryable_subclasses.step import StepQueryableClass


class MergeSortClass(ProcessorClass):
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

        def merge_sort(arr: List[int], left: int, right: int):
            if left < right:
                mid = (left + right) // 2
                merge_sort(arr, left, mid)
                merge_sort(arr, mid + 1, right)
                merge(arr, left, mid, right)
                states.append(arr.copy())

        def merge(arr: List[int], left: int, mid: int, right: int):
            n1 = mid - left + 1
            n2 = right - mid

            L = arr[left:mid + 1]
            R = arr[mid + 1:right + 1]

            i = j = 0
            k = left

            while i < n1 and j < n2:
                if L[i] <= R[j]:
                    arr[k] = L[i]
                    i += 1
                else:
                    arr[k] = R[j]
                    j += 1
                k += 1

            while i < n1:
                arr[k] = L[i]
                i += 1
                k += 1

            while j < n2:
                arr[k] = R[j]
                j += 1
                k += 1

        merge_sort(input, 0, len(input) - 1)
        return states
