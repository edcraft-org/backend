import random
from typing import Any, Dict, Generic, List, Type, TypeVar
from question_generation.input.input_class import Input
from question_generation.input.input_subclasses.primitive.int_type import IntInput
from question_generation.quantifiable.quantifiable_class import Quantifiable
from utils.constants import MIN_VALUE, MAX_INT_VALUE

T = TypeVar('T', bound=Quantifiable)

class ListInput(Input, Quantifiable, Generic[T]):
    def __init__(self, element_type: Type[T] = IntInput, length: int = None, options: Dict[str, Any] = {}):
        self.element_type = element_type
        self.length = length if length is not None else options.get('length', 10)
        self._value = self.generate_input(options)

    def value(self) -> List[Any]:
        return self._value

    def generate_input(self, options: Dict[str, Any] = {}) -> List[Any]:
        """
        Generate input data for the algorithm.

        Args:
            options (Dict[str, Any]): Additional options for generating input, including:
                - length (int): The length of the list.

        Returns:
            List[Any]: The generated input data.
        """
        return [self.element_type().value() for _ in range(self.length)]

    def generate_options(self, answer: List[Any] = None , options: Dict[str, Any] = {}) -> List[List[Any]]:
        """
        Generate options for generating input data.

        Args:
            answer (List[Any]): The answer for the input data.
            options (Dict[str, Any]): Options for generating input, including:
                - num_options (int): The number of options to generate.
                - use_existing (bool): Whether to shuffle the existing list instead of creating a new list.

        Returns:
            List[List[Any]]: The generated options.
        """
        if answer is None:
            answer = self.generate_input()

        num_options = options.get('num_options', 4)
        use_existing = options.get('use_existing', True)
        length = options.get('length', self.length)

        generated_options = set()
        generated_options.add(tuple(answer))

        if use_existing:
            while len(generated_options) < num_options:
                shuffled_answer = answer[:]
                random.shuffle(shuffled_answer)
                generated_options.add(tuple(shuffled_answer))
        else:
            while len(generated_options) < num_options:
                option = [self.element_type().generate_input(options) for _ in range(length)]
                if option != answer:
                    generated_options.add(tuple(option))

        return [list(option) for option in generated_options]
