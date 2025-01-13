from abc import ABC, abstractmethod
import copy
import inspect
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

    def get_init_args(self) -> Dict[str, Any]:
        """
        Get the arguments required to initialize an instance of a class.

        Args:
            instance (Any): The instance of the class.

        Returns:
            Dict[str, Any]: A dictionary containing the names and values of the initialization arguments.
        """
        signature = inspect.signature(self.__init__)
        init_args = {}
        for param in signature.parameters.values():
            if param.name == 'self':
                continue
            if hasattr(self, param.name):
                # init_args[param.name] = copy.deepcopy(getattr(self, param.name))
                value = copy.deepcopy(getattr(self, param.name))
                # Skip non-serializable objects and parameters without a value
                if isinstance(value, (type, inspect.Signature, inspect.Parameter)) or value is param.default:
                    continue
                init_args[param.name] = value
            # else:
            #     init_args[param.name] = param.default
        return init_args
