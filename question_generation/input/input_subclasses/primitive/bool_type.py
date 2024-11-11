from faker import Faker
from question_generation.input.input_class import Input
from typing import Any, Dict, List

from question_generation.quantifiable.quantifiable_class import Quantifiable

class BoolInput(Input, Quantifiable):
    def __init__(self, value: bool = None, options: Dict[str, Any] = {}):
        if value is None:
            self._value = self.generate_input(options)
        else:
            self._value = value

    def value(self) -> bool:
        return self._value

    def generate_input(self, options: Dict[str, Any] = {}) -> bool:
        """
        Generate input data for the algorithm.

        Args:
            options (Dict[str, Any]): Options for generating input, including:
                - chance_of_getting_true (int): The chance of getting True (0-100).

        Returns:
            bool: The generated input data.
        """
        chance_of_getting_true = options.get('chance_of_getting_true', 50)

        fake = Faker()
        return fake.boolean(chance_of_getting_true=chance_of_getting_true)

    def generate_options(self, answer: bool, options: Dict[str, Any] = {}) -> List[bool]:
        """
        Generate options for generating input data.

        Args:
            answer (bool): The answer for the input data.
            options (Dict[str, Any]): Options for generating input.

        Returns:
            List[bool]: The generated options.
        """
        return [True, False]