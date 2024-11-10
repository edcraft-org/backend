from abc import ABC, abstractmethod
from typing import Any, Dict, List


class Input(ABC):
    def generate_input(self, options: Dict[str, Any] = {}) -> Any:
        """
        Generate input data for the algorithm.

        Args:
            options (Dict[str, Any]): Options for generating input.

        Returns:
            Any: The generated input data.
        """
        raise NotImplementedError("Method 'generate_input' is not implemented")

    def generate_options(self, answer: Any, options: Dict[str, Any] = {}) -> List[Any]:
        """
        Generate options for generating input data.

        Args:
            answer (Any): The answer for the input data.
            options (Dict[str, Any]): Options for generating input.

        Returns:
            List[Any]: The generated options.
        """
        raise NotImplementedError("Method 'generate_options' is not implemented")
