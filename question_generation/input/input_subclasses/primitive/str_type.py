from faker import Faker
from question_generation.input.input_class import Input
from typing import Any, Dict, List

from question_generation.quantifiable.quantifiable_class import Quantifiable

fake = Faker()

class StringInput(str, Input, Quantifiable):
    def __new__(cls, value: str = None, options: Dict[str, Any] = {}):
        if value is None:
            value = cls.generate_input(cls, options)
        instance = super().__new__(cls, value)
        instance._value = value
        return instance

    def generate_input(self, options: Dict[str, Any] = {}) -> str:
        max_length = options.get('max_length', 10)
        return fake.text(max_nb_chars=max_length)
