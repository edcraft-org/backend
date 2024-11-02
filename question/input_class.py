from abc import ABC, abstractmethod
from typing import Any, Dict


class Input(ABC):
    @abstractmethod
    def generate_input(self, options: Dict[str, Any] = {}) -> Any:
        """
        Generate input data for the algorithm.

        Args:
            options (Dict[str, Any]): Options for generating input.

        Returns:
            Any: The generated input data.
        """
        raise NotImplementedError("Method 'generate_input' is not implemented")
