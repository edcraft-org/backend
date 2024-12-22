from abc import ABC, abstractmethod
from typing import Any, Dict, List


class Input(ABC):
    def generate_input(self) -> Any:
        """
        Generate input data for the algorithm.

        Returns:
            Any: The generated input data.
        """
        raise NotImplementedError("Method 'generate_input' is not implemented")

    def generate_options(self) -> List[Any]:
        """
        Generate options for generating input data.

        Returns:
            Any: The generated option.
        """

        return self.__class__()