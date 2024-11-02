from typing import List, Tuple
from question.processor_class import Processor
from question.processor_subclasses.Sort.queryable.sort_output import SortOutputQueryable
from question.processor_subclasses.Sort.queryable.sort_step import SortStepQueryable

class QuickSortClass(Processor, SortOutputQueryable, SortStepQueryable):
    def algo(self, input: List[int]) -> List[Tuple[List[int], int]]:
        states: List[Tuple[List[int], int]] = []
        step = 0

        def quick_sort(arr: List[int], low: int, high: int):
            nonlocal step
            if low < high:
                pi = partition(arr, low, high)
                quick_sort(arr, low, pi - 1)
                quick_sort(arr, pi + 1, high)
                step += 1
                states.append((arr.copy(), step))

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
