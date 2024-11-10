from typing import Any, List, Tuple

class Queryable:
    variable: str = "variable"

    def query(self, *args, **kwargs) -> Any:
        return getattr(self, self.variable)

    def query_all(self) -> List[Tuple[type, Any]]:
        return [(cls, getattr(cls, 'query', None)) for cls in self.__class__.__bases__ if issubclass(cls, Queryable)]
