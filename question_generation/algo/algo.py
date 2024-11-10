from abc import ABC, abstractmethod

class Algo(ABC):
    @abstractmethod
    def algo(self, *args, **kwargs):
        raise NotImplementedError("Method 'algo' must be implemented in subclass")
