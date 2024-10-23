from question.queryable_class import QueryableClass


class OutputQueryableClass(QueryableClass):
    @classmethod
    def queryable(cls) -> str:
        return "Output"
