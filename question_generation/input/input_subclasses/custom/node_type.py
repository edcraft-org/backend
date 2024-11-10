class Node(Quantifyable):
    _label: str
    _children: list[Node]

    def value(self):
        return self._value


class Int(Quantifyable):
    def init(self, x):
        self._value = x