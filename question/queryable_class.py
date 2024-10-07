from abc import ABC, abstractmethod
from enum import Enum

class QueryableTypes(Enum):
    STEP = "Step"
    OUTPUT = "Output"

class VariableTypes(Enum):
    INPUT = "Input"
    STEP = "Step"


class QueryableClass(ABC):
    @classmethod
    def queryable_options(cls):
        return [
            {
                'queryable': QueryableTypes.STEP.value,
                'variables': [VariableTypes.INPUT.value, VariableTypes.STEP.value],
            },
            {
                'queryable': QueryableTypes.OUTPUT.value,
                'variables': [VariableTypes.INPUT.value],
            }
        ]