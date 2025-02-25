from copy import deepcopy
from typing import Generic, List, Optional, Type, TypeVar
from uuid import uuid4
from question_generation.input.input_class import Input
from question_generation.input.input_subclasses.primitive.int_type import IntInput
from question_generation.quantifiable.quantifiable_class import Quantifiable

T = TypeVar('T', bound=Quantifiable)

class AdversarialElement(Input, Quantifiable, Generic[T]):
    internal = True
    def __init__(self, element_type: Optional[Type[T]] = IntInput, value=None, neighbours=None):
        """
        Initialize a node in the tree.
        :param element_type: Type of element (e.g., IntInput) that the node will store.
        :param value: Value for terminal nodes. Used when the node is terminal.
        :param children: List of child nodes for internal nodes.
        """
        self.element_type = element_type

        # Initialize value depending on whether it's terminal or internal
        if value is not None:
            self._value = value  # Terminal node with a predefined value
        elif self.element_type is not None:
            if self.element_type == IntInput:
                self._value = self.element_type(max = 100).value()
            else:
                self._value = self.element_type().value()  # Generate value based on element type
        else:
            self._value = None  # Default value is None, used for non-terminal nodes

        self.neighbours = neighbours if neighbours is not None else []  # Internal nodes will have children
        self.id = uuid4()

    def get_actions(self) -> List['AdversarialElement']:
        return self.neighbours

    def is_terminal(self) -> bool:
        return len(self.neighbours) == 0

    def value(self) -> float:
        """
        Return the value of the node.
        """
        if self._value is not None:
            return self._value
        raise ValueError("Cannot retrieve value.")

    def __deepcopy__(self, memo):
        new_instance = self.__class__(self.element_type, self._value)
        new_instance.neighbours = deepcopy(self.neighbours, memo)
        new_instance.id = self.id
        return new_instance

    def __str__(self) -> str:
        return f"Element with value {self._value}, {len(self.neighbours)} neighbours, id {self.id}"

    def __repr__(self) -> str:
        return self.__str__()
