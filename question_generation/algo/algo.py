from abc import ABC, abstractmethod

class Algo(ABC):
    def __init__(self, generate_graph: bool = True):
        super().__init__()
        self.generate_graph = generate_graph

    @abstractmethod
    def algo(self, *args, **kwargs):
        raise NotImplementedError("Method 'algo' must be implemented in subclass")
