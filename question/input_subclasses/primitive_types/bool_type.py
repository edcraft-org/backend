from faker import Faker
from question.input_class import InputClass


class BoolInputClass(InputClass):
    @classmethod
    def generate_input(cls, chance_of_getting_true: int = 50) -> bool:
        fake = Faker()
        return fake.boolean(chance_of_getting_true=chance_of_getting_true)
