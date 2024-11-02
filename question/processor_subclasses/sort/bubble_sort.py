from typing import List, Any, Tuple
from question.processor_class import Processor
from question.processor_subclasses.Sort.queryable.sort_output import SortOutputQueryable
from question.processor_subclasses.Sort.queryable.sort_step import SortStepQueryable

class BubbleSortClass(Processor, SortOutputQueryable, SortStepQueryable):
    def algo(self, input: List[int]) -> List[Tuple[List[int], int]]:
        states: List[Tuple[List[int], int]] = []
        n = len(input)
        step = 0

        for i in range(n):
            swapped = False

            for j in range(0, n-i-1):
                if input[j] > input[j+1]:
                    input[j], input[j+1] = input[j+1], input[j]
                    swapped = True

            states.append((input.copy(), step))
            step += 1
            if not swapped:
                break
        return states
