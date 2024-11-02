from typing import List, Tuple
from question.processor_class import Processor
from question.processor_subclasses.Sort.queryable.sort_output import SortOutputQueryable
from question.processor_subclasses.Sort.queryable.sort_step import SortStepQueryable

class MergeSortClass(Processor, SortOutputQueryable, SortStepQueryable):
    def algo(self, input: List[int]) -> List[Tuple[List[int], int]]:
        states: List[Tuple[List[int], int]] = []
        step = 0

        def merge_sort(arr: List[int], left: int, right: int):
            nonlocal step
            if left < right:
                mid = (left + right) // 2
                merge_sort(arr, left, mid)
                merge_sort(arr, mid + 1, right)
                merge(arr, left, mid, right)
                step += 1
                states.append((arr.copy(), step))

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
