from typing import Any, Dict, List
from faker import Faker
from question_generation.input.input_class import Input
from question_generation.quantifiable.quantifiable_class import Quantifiable
from utils.constants import MIN_VALUE, MAX_INT_VALUE

fake = Faker()

class IntInput(int, Input, Quantifiable):
    # Since int is immutable, initialization happens during object creation (__new__), not in __init__
    def __new__(cls, value: int = None, options: Dict[str, Any] = {}):
        if value is None:
            value = cls.generate_input(cls, options)
        instance = super().__new__(cls, value)
        instance._value = value
        return instance

    def generate_input(self, options: Dict[str, Any] = {}) -> int:
        min_value = options.get('min_value', MIN_VALUE)
        max_value = options.get('max_value', MAX_INT_VALUE)
        return fake.random_int(min=min_value, max=max_value)
