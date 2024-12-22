import random
from typing import Any, Dict, Generic, List, Type, TypeVar
from question_generation.input.input_class import Input
from question_generation.input.input_subclasses.primitive.int_type import IntInput
from question_generation.quantifiable.quantifiable_class import Quantifiable

T = TypeVar('T', bound=Quantifiable)

class ListInput(list, Input, Quantifiable, Generic[T]):
    _exposed_args = ['length']

    def __init__(self, element_type: Type[T] = IntInput, value: List[T] = None, length: int = 10):
        self.element_type = element_type
        self.length = length
        if value is not None:
            self._value = value
        else:
            self._value = self.generate_input()
        super().__init__(self._value)

    def generate_input(self) -> List[Any]:
        return [self.element_type() for _ in range(self.length)]

    def generate_options(self) -> 'ListInput':
        shuffled_value = self._value[:]
        random.shuffle(shuffled_value)
        return self.__class__(element_type=self.element_type, value=shuffled_value, length=self.length)
