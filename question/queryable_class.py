from abc import ABC, abstractmethod
from typing import List

class QueryableClass(ABC):
    @classmethod
    @abstractmethod
    def queryable(cls) -> str:
        pass
