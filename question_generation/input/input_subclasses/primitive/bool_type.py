from faker import Faker
from question_generation.input.input_class import Input
from question_generation.quantifiable.quantifiable_class import Quantifiable
from typing import Any, Dict, List

fake = Faker()

class BoolInput(Input, Quantifiable):
    def __init__(self, value: bool = None, chance: int = 50):
        if value is None:
            self._value = self.generate_input(chance)
        else:
            self._value = value

    def __bool__(self):
        return self._value

    def __int__(self):
        return int(self._value)

    def generate_input(self, chance: int = 50) -> bool:
        return fake.boolean(chance_of_getting_true=chance)

