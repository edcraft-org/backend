from faker import Faker
from question_generation.input.input_class import Input
from typing import Any, Dict, List

from question_generation.quantifiable.quantifiable_class import Quantifiable

class StringInput(Input, Quantifiable):
    def __init__(self, value: str = None, options: Dict[str, Any] = {}):
        if value is None:
            self._value = self.generate_input(options)
        else:
            self._value = value

    def value(self) -> str:
        return self._value

    def generate_input(self, options: Dict[str, Any] = {}) -> str:
        """
        Generate input data for the algorithm.

        Args:
            options (Dict[str, Any]): Options for generating input, including:
                - max_length (int): The maximum length of the generated string.

        Returns:
            str: The generated input data.
        """
        max_length = options.get('max_length', 10)

        fake = Faker()
        return fake.text(max_nb_chars=max_length)

    def generate_options(self, answer: str, options: Dict[str, Any] = {}) -> List[str]:
        """
        Generate options for generating input data.

        Args:
            answer (str): The answer for the input data.
            options (Dict[str, Any]): Options for generating input.

        Returns:
            List[str]: The generated options.
        """
        num_options = options.get('num_options', 4)
        max_length = len(answer)

        fake = Faker()
        generated_options = set()
        generated_options.add(answer)

        while len(generated_options) < num_options:
            option = fake.text(max_nb_chars=max_length).strip()
            if option != answer:
                generated_options.add(option)

        return list(generated_options)