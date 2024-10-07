from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, List, Tuple
from faker import Faker

# from question.enums import DataStructureTypes

class DataStructureTypes(Enum):
    LIST_OF_INTEGERS = 'List of Integers'
    TUPLE_OF_STRINGS = 'Tuple of Strings'
    SET_OF_FLOATS = 'Set of Floats'
    DICTIONARY_OF_STRING_TO_INT = 'Dictionary of String to Int'
    ARRAY_OF_INTEGERS = 'Array of Integers'
    TREE = 'Tree'
    GRAPH = 'Graph'

class InputClass(ABC):
    @classmethod
    @abstractmethod
    def input_type(cls) -> DataStructureTypes:
        pass

    @classmethod
    def obtain_input(cls, numberOfOptions: int):
        if cls.input_type() == DataStructureTypes.LIST_OF_INTEGERS:
            return cls.generate_list_integers(numberOfOptions)

    @classmethod
    def generate_list_integers(cls, numberOfOptions: int) -> Tuple[List[Any], List[Any]]:
        variables_data = []
        options_data = []
        fake = Faker()
        size = fake.random_int(min=5, max=10)
        min_value = 0
        max_value = 10

        inputList = [fake.random_int(min=min_value, max=max_value) for _ in range(size)]
        variables_data.append(inputList)

        step = fake.random_int(min=0, max=size - 1)
        variables_data.append(step)

        possible_values = set(range(size))
        possible_values.remove(step)

        for _ in range(numberOfOptions - 1):
            option = fake.random_element(elements=list(possible_values))
            options_data.append(option)

        return variables_data, options_data






    # @classmethod
    # def validate_input(self):
    #     input_type = self.get_input_type()
    #     if input_type == DataStructureTypes.LIST_OF_INTEGERS:
    #         if not isinstance(self.input_data, list) or not all(isinstance(i, int) for i in self.input_data):
    #             raise TypeError(f"Expected input type {input_type.value}, got {type(self.input_data).__name__} with elements of type {type(self.input_data[0]).__name__ if self.input_data else 'unknown'}")
    #     elif input_type == DataStructureTypes.TUPLE_OF_STRINGS:
    #         if not isinstance(self.input_data, tuple) or not all(isinstance(i, str) for i in self.input_data):
    #             raise TypeError(f"Expected input type {input_type.value}, got {type(self.input_data).__name__} with elements of type {type(self.input_data[0]).__name__ if self.input_data else 'unknown'}")
    #     elif input_type == DataStructureTypes.SET_OF_FLOATS:
    #         if not isinstance(self.input_data, set) or not all(isinstance(i, float) for i in self.input_data):
    #             raise TypeError(f"Expected input type {input_type.value}, got {type(self.input_data).__name__} with elements of type {type(self.input_data[0]).__name__ if self.input_data else 'unknown'}")
    #     elif input_type == DataStructureTypes.DICTIONARY_OF_STRING_TO_INT:
    #         if not isinstance(self.input_data, dict) or not all(isinstance(k, str) and isinstance(v, int) for k, v in self.input_data.items()):
    #             raise TypeError(f"Expected input type {input_type.value}, got {type(self.input_data).__name__} with elements of type {type(next(iter(self.input_data.keys()))).__name__ if self.input_data else 'unknown'} to {type(next(iter(self.input_data.values()))).__name__ if self.input_data else 'unknown'}")
    #     elif input_type == DataStructureTypes.ARRAY_OF_INTEGERS:
    #         if not isinstance(self.input_data, list) or not all(isinstance(i, int) for i in self.input_data):
    #             raise TypeError(f"Expected input type {input_type.value}, got {type(self.input_data).__name__} with elements of type {type(self.input_data[0]).__name__ if self.input_data else 'unknown'}")
    #     # Add more type checks as needed for other data structure types
