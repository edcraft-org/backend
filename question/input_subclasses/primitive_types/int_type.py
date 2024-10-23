from faker import Faker
from question.input_class import InputClass
from utils.constants import MIN_VALUE, MAX_INT_VALUE


class IntInputClass(InputClass):
    @classmethod
    def generate_input(cls, min_value: int = MIN_VALUE, max_value: int = MAX_INT_VALUE) -> int:
        fake = Faker()
        return fake.random_int(min=min_value, max=max_value)
