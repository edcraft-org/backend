from faker import Faker
from question.input_class import Input
from typing import Any, Dict

class BoolInput(Input):
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