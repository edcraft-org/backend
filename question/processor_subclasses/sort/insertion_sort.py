from typing import List, Tuple
from question.processor_class import Processor
from question.processor_subclasses.Sort.queryable.sort_output import SortOutputQueryable
from question.processor_subclasses.Sort.queryable.sort_step import SortStepQueryable


class InsertionSortClass(Processor, SortOutputQueryable, SortStepQueryable):
    def algo(self, input: List[int]) -> List[Tuple[List[int], int]]:
        states: List[Tuple[List[int], int]] = []

        for insert_index in range(1, len(input)):
            insert_value = input[insert_index]
            while insert_index > 0 and insert_value < input[insert_index - 1]:
                input[insert_index] = input[insert_index - 1]
                insert_index -= 1
            input[insert_index] = insert_value
            states.append((input.copy(), insert_index))
        return states
