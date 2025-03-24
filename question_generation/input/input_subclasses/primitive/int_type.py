from typing import Any, Dict, List
from faker import Faker
from question_generation.input.input_class import Input
from question_generation.quantifiable.quantifiable_class import Quantifiable
from utils.constants import MIN_VALUE, MAX_INT_VALUE

fake = Faker()

class IntInput(int, Input, Quantifiable):
    _exposed_args = ['value']

    # Since int is immutable, initialization happens during object creation (__new__), not in __init__
    def __new__(cls, value: int = None, max: int = MAX_INT_VALUE, min: int = MIN_VALUE):
        if value is None:
            value = cls.generate_input(cls, max, min)
        instance = super().__new__(cls, value)
        instance._value = value
        instance._init_args = {
            'value': value,
        }
        return instance

    def generate_input(self, max: int = MAX_INT_VALUE, min: int = MIN_VALUE) -> int:
        return fake.random_int(min=min, max=max)

    def get_init_args(self) -> Dict[str, Any]:
        """Return initialization arguments."""
        return self._init_args
