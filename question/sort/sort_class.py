from enum import Enum
import random
from typing import Any, Dict, List, Type

from algorithm.sort.insertion_sort import InsertionSortClass
# from question.enums import DataStructureTypes, SortAlgorithms, Topics

from question.input_class import DataStructureTypes, InputClass
from question.processor_class import ProcessorClass
from question.queryable_class import QueryableClass, QueryableTypes

class SortAlgorithms(Enum):
    INSERTION_SORT = 'Insertion Sort'
    MERGE_SORT = 'Merge Sort'
    BUBBLE_SORT = 'Bubble Sort'
    QUICK_SORT = 'Quick Sort'

class SortClass(InputClass, ProcessorClass, QueryableClass):
    algorithm_class_mapping: Dict[str, Type] = {
        SortAlgorithms.INSERTION_SORT.value: InsertionSortClass,
        # SortAlgorithms.MERGE_SORT.value: MergeSortClass,
        # SortAlgorithms.BUBBLE_SORT.value: BubbleSortClass,
        # SortAlgorithms.QUICK_SORT.value: QuickSortClass,
    }

    # InputClass
    @classmethod
    def input_type(cls) -> DataStructureTypes:
        return DataStructureTypes.LIST_OF_INTEGERS

    # ProcessorClass
    @classmethod
    def subtopic(cls):
        return [
            SortAlgorithms.INSERTION_SORT.value,
            SortAlgorithms.MERGE_SORT.value,
            SortAlgorithms.BUBBLE_SORT.value,
            SortAlgorithms.QUICK_SORT.value
        ]

    @classmethod
    def process_method(cls, queryable: str, subtopic: str, variables_data: List[Any], options_data: List[Any]) -> Dict[str, Any]:
        unsorted = variables_data[0][:]
        sorter_class = cls.algorithm_class_mapping.get(subtopic)
        if sorter_class is None:
            raise ValueError(f"Unsupported sorting algorithm: {subtopic}")
        sorter = sorter_class(unsorted)
        sorted_list, states = sorter.sort_with_states()

        if queryable == QueryableTypes.OUTPUT.value:
            correct_answer = sorted_list
        elif queryable == QueryableTypes.STEP.value:
            correct_answer = sorter.get_state_at_iteration(variables_data[1])
        else:
            raise ValueError(f"Queryable {queryable} not found")

        distractor_options = []
        for option in options_data:
            distractor_options.append(sorter.get_state_at_iteration(option))

        all_options = [correct_answer] + distractor_options
        random.shuffle(all_options)

        all_options = [str(option) for option in all_options]
        correct_answer = str(correct_answer)

        return {
            "answer": correct_answer,
            "options": all_options
        }
