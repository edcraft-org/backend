from typing import List

from question.queryable_class import QueryableClass

class StepQueryableClass(QueryableClass):
    @classmethod
    def queryable(cls) -> str:
        return "Step"
