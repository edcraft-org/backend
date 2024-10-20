from faker import Faker
from question.input_class import InputClass


class StringInputClass(InputClass):
    @classmethod
    def generate_input(cls, max_length: int = 10) -> str:
        fake = Faker()
        return fake.text(max_nb_chars=max_length)
