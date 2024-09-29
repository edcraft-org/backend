import random
from typing import Any, Dict, List, Tuple
from question.question import Question
from question.data_types import DataStructureTypes
from algorithm.sort.insertion_sort import get_state_at_iteration, insertion_sort, insertion_sort_with_states, state_at_iteration
from faker import Faker

class InsertionSortQuestion(Question):
    # Define the structure as a class attribute
    topic = [
        {
            'queryable': 'State at Iteration',
            'variables': ['Input array', 'Iteration'],
            'outputType': 'Array',
        },
        {
            'queryable': 'Sorted Array',
            'variables': ['Input array'],
            'outputType': 'Array',
        },
    ]

    @classmethod
    def input_type(cls):
        return DataStructureTypes.LIST.value

    @classmethod
    def obtain_input(cls, queryable: str, options: int) -> Tuple[List[Any], List[Any]]:
        variables_data = []
        options_data = []
        fake = Faker()
        size = fake.random_int(min=5, max=10)
        min_value = 0
        max_value = 10
        iteration = -1

        inputList = [fake.random_int(min=min_value, max=max_value) for _ in range(size)]
        variables_data.append(inputList)
        if queryable == 'State at Iteration':
            iteration = fake.random_int(min=0, max=size - 1)
            variables_data.append(iteration)

        # Generate options that are not equal to the iteration using Faker
        possible_values = set(range(size))

        if iteration != -1:
            possible_values.remove(iteration)

        for _ in range(options - 1):
            option = fake.random_element(elements=list(possible_values))
            options_data.append(option)

        return variables_data, options_data

    @classmethod
    def process_method(cls, queryable: str, variables_data: List[Any], options_data: List[Any]) -> Dict[str, Any]:
        sorted_collection, states = insertion_sort_with_states(variables_data[0][:])

        if queryable == 'Sorted Array':
            correct_answer = sorted_collection
        elif queryable == 'State at Iteration':
            correct_answer = get_state_at_iteration(states, variables_data[1])
        else:
            raise ValueError(f"Queryable {queryable} not found in Insertion Sort topic")

        # Generate distractor options
        distractor_options = []

        for option in options_data:
            distractor_options.append(get_state_at_iteration(states, option))

        # Combine correct answer with distractor options and shuffle
        all_options = [correct_answer] + distractor_options
        random.shuffle(all_options)

        # Convert lists to strings
        all_options = [str(option) for option in all_options]
        correct_answer = str(correct_answer)

        return {
            "answer": correct_answer,
            "options": all_options
        }

    @classmethod
    def query_options(cls):
        return cls.topic

    @classmethod
    def output_type(cls, queryable):
        for item in cls.topic:
            if item['queryable'] == queryable:
                return item['outputType']
        raise ValueError(f"Queryable {queryable} not found in Insertion Sort topic")

    @classmethod
    def variables(cls, queryable):
        for item in cls.topic:
            if item['queryable'] == queryable:
                return item['variables']
        raise ValueError(f"Queryable {queryable} not found in Insertion Sort topic")
