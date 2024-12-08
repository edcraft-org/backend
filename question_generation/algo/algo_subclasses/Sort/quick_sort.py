from typing import Any, List
from copy import deepcopy
from question_generation.algo.algo import Algo
from question_generation.input.input_subclasses.composite.list_type import ListInput
from question_generation.quantifiable.quantifiable_class import Quantifiable
from question_generation.queryable.queryable_subclasses.output import Output
from question_generation.queryable.queryable_subclasses.step import Step
from question_generation.question.question import Question


class QuickSortClass(Algo, Question, Output, Step):
    def algo(self, input: ListInput[Quantifiable]):
        def quick_sort(arr: List[Any], low: int, high: int):
            if low < high:
                pi = partition(arr, low, high)
                quick_sort(arr, low, pi - 1)
                quick_sort(arr, pi + 1, high)
                self.step(arr)

        def partition(arr: List[Any], low: int, high: int) -> int:
            pivot = arr[high]
            i = low - 1
            for j in range(low, high):
                if arr[j] < pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            return i + 1

        quick_sort(input, 0, len(input) - 1)
        self.output(input)
