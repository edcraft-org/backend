from abc import ABC, abstractmethod
from typing import Any


class Queryable(ABC):
    @abstractmethod
    def query(self, *args, **kwargs) -> Any:
        raise NotImplementedError("Method 'query' must be implemented in subclass")

    @abstractmethod
    def algo(self, *args, **kwargs):
        raise NotImplementedError("Method 'algo' must be implemented in subclass")
