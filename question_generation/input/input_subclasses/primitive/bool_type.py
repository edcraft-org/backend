from faker import Faker
from question_generation.input.input_class import Input
from question_generation.quantifiable.quantifiable_class import Quantifiable
from typing import Any, Dict, List

fake = Faker()

class BoolInput(Input, Quantifiable):
    def __init__(self, value: bool = None, options: Dict[str, Any] = {}):
        if value is None:
            self._value = self.generate_input(options)
        else:
            self._value = value

    def __bool__(self):
        return self._value

    def __int__(self):
        return int(self._value)

    def generate_input(self, options: Dict[str, Any] = {}) -> bool:
        chance_of_getting_true = options.get('chance_of_getting_true', 50)
        return fake.boolean(chance_of_getting_true=chance_of_getting_true)

