from faker import Faker
from question.input_class import Input
from typing import Any, Dict

class StringInput(Input):
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
