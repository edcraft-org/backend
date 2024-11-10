from typing import Any


class Quantifiable:
    _value: Any

    def value(self) -> Any:
        return self._value