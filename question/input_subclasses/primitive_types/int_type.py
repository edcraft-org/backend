from typing import Any, Dict
from faker import Faker
from question.input_class import Input
from utils.constants import MIN_VALUE, MAX_INT_VALUE


class IntInput(Input):
    def generate_input(self, options: Dict[str, Any] = {}) -> int:
        """
        Generate input data for the algorithm.

        Args:
            options (Dict[str, Any]): Additional options for generating input, including:
                - min_value (int): The minimum value for the input.
                - max_value (int): The maximum value for the input.

        Returns:
            int: The generated input data.
        """
        min_value = options.get('min_value', MIN_VALUE)
        max_value = options.get('max_value', MAX_INT_VALUE)

        fake = Faker()
        return fake.random_int(min=min_value, max=max_value)
