from question.question import Question
from question.data_types import DataStructureTypes
from typing import List, Tuple, Optional

class MergeSortQuestion(Question):
    # Define the structure as a class attribute
    topic = [
        {
            'queryable': 'Merge Sort',
            'variables': ['List of integers'],
            'outputType': 'Array',
        },
        {
            'queryable': 'State at Iteration',
            'variables': ['List of integers', 'Iteration'],
            'outputType': 'Array',
        },
        {
            'queryable': 'State at Depth',
            'variables': ['List of integers', 'Depth'],
            'outputType': 'Array',
        },
    ]

    @classmethod
    def input_type(cls):
        return DataStructureTypes.LIST.value

    @classmethod
    def obtain_input(cls, input_data):
        if not isinstance(input_data, list):
            raise ValueError("Input data must be a list")
        cls.input_data = input_data

    @classmethod
    def process_method(cls, queryable: str, *args):
        if queryable == 'Merge Sort':
            return cls.merge_sort(cls.input_data)
        elif queryable == 'State at Iteration':
            iteration = args[0]
            return cls.state_at_iteration(cls.input_data, iteration)
        elif queryable == 'State at Depth':
            depth = args[0]
            return cls.state_at_depth(cls.input_data, depth)
        else:
            raise ValueError(f"Queryable {queryable} not found in Merge Sort topic")

    @classmethod
    def query_options(cls):
        return cls.topic

    @classmethod
    def output_type(cls, queryable):
        for item in cls.topic:
            if item['queryable'] == queryable:
                return item['outputType']
        raise ValueError(f"Queryable {queryable} not found in Merge Sort topic")

    @classmethod
    def variables(cls, queryable):
        for item in cls.topic:
            if item['queryable'] == queryable:
                return item['variables']
        raise ValueError(f"Queryable {queryable} not found in Merge Sort topic")
