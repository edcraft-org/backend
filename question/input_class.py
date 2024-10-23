from abc import ABC, abstractmethod
from typing import Any


class InputClass(ABC):
    @classmethod
    @abstractmethod
    def generate_input(cls, **kwargs) -> Any:
        pass
