from abc import ABC, abstractmethod


class QueryableClass(ABC):
    @classmethod
    @abstractmethod
    def queryable(cls) -> str:
        pass
