from typing import Any, Dict, List
from faker import Faker
from question_generation.input.input_class import Input
from question_generation.quantifiable.quantifiable_class import Quantifiable
from utils.constants import MIN_VALUE, MAX_INT_VALUE

class IntInput(Input, Quantifiable):
    def __init__(self, value: int = None, options: Dict[str, Any] = {}):
        if value is None:
            self._value = self.generate_input(options)
        else:
            self._value = value

    def value(self) -> int:
        return self._value

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

    def generate_options(self, answer: int, options: Dict[str, Any] = {}) -> List[int]:
        """
        Generate options for generating input data.

        Args:
            answer (int): The answer for the input data.
            options (Dict[str, Any]): Options for generating input.

        Returns:
            List[int]: The generated options.
        """
        num_options = options.get('num_options', 4)
        min_value = options.get('min_value', MIN_VALUE)
        max_value = options.get('max_value', MAX_INT_VALUE)

        fake = Faker()
        generated_options = set()
        generated_options.add(answer)

        while len(generated_options) < num_options:
            option = fake.random_int(min=min_value, max=max_value)
            if option != answer:
                generated_options.add(option)

        return list(generated_options)