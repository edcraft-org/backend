from typing import Any
from functools import total_ordering

@total_ordering
class Quantifiable:
    _value: Any

    def value(self) -> Any:
        return self._value

    def __eq__(self, other):
        if isinstance(other, Quantifiable):
            return self._value == other._value
        return self._value == other

    def __lt__(self, other):
        if isinstance(other, Quantifiable):
            return self._value < other._value
        return self._value < other

    def __repr__(self):
        return str(self._value)
