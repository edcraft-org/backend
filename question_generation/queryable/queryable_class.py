from typing import Any, Callable, List, Tuple

class Queryable:
    def __init__(self):
        self.variable: str = "variable"
        self.generate_input_function: Callable[[], Any] = None

    def query(self, *args, **kwargs) -> Any:
        return getattr(self, self.variable)

    def query_all(self) -> List[Tuple[type, Any, Callable[[], Any]]]:
        return [
            (cls, getattr(cls, 'query', None), getattr(cls, 'generate_input', None))
            for cls in self.__class__.__bases__
            if issubclass(cls, Queryable)
        ]