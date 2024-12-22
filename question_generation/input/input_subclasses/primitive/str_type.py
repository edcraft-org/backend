from faker import Faker
from question_generation.input.input_class import Input

from question_generation.quantifiable.quantifiable_class import Quantifiable

fake = Faker()

class StringInput(str, Input, Quantifiable):
    def __new__(cls, value: str = None, length: int = 10):
        if value is None:
            value = cls.generate_input(cls, length)
        instance = super().__new__(cls, value)
        instance._value = value
        return instance

    def generate_input(self, length: int = 10) -> str:
        return fake.text(max_nb_chars=length)
