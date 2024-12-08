from typing import Any, List
from copy import deepcopy
from question_generation.algo.algo import Algo
from question_generation.input.input_subclasses.composite.list_type import ListInput
from question_generation.quantifiable.quantifiable_class import Quantifiable
from question_generation.queryable.queryable_subclasses.output import Output
from question_generation.queryable.queryable_subclasses.step import Step
from question_generation.question.question import Question


class MergeSortClass(Algo, Question, Output, Step):
    def algo(self, input: ListInput[Quantifiable]):
        def merge_sort(arr: List[Any], left: int, right: int):
            if left < right:
                mid = (left + right) // 2
                merge_sort(arr, left, mid)
                merge_sort(arr, mid + 1, right)
                merge(arr, left, mid, right)
                self.step(arr)

        def merge(arr: List[Any], left: int, mid: int, right: int):
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
        self.output(input)
