from typing import Any, Dict, Generic, List, Optional, Type, TypeVar
from question_generation.input.input_class import Input
from question_generation.input.input_subclasses.primitive.int_type import IntInput
from question_generation.quantifiable.quantifiable_class import Quantifiable

T = TypeVar('T', bound=Quantifiable)

class Node(Input, Quantifiable, Generic[T]):
    def __init__(self, element_type: Optional[Type[T]] = IntInput, value=None, children=None):
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

        self.children = children if children is not None else []  # Internal nodes will have children

    def get_children(self) -> List['Node']:
        """
        Return the children of this node.
        """
        return self.children

    def is_terminal(self) -> bool:
        """
        Determine if the node is terminal (has no children).
        """
        return len(self.children) == 0

    def value(self) -> float:
        """
        Return the value of the node. This is only meaningful for terminal nodes.
        """
        if self.is_terminal() and self._value is not None:
            return self._value
        raise ValueError("Cannot retrieve value from a non-terminal node without a value.")

    def __str__(self) -> str:
        """
        String representation of the node. If terminal, shows its value; otherwise shows children count.
        """
        if self.is_terminal():
            return f"Terminal Node with value {self._value}"
        return f"Internal Node with {len(self.children)} children"

    def __repr__(self) -> str:
        return self.__str__()
