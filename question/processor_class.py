
from abc import ABC
from typing import Any, Dict, List

from question.queryable_class import QueryableClass

class ProcessorClass(ABC):
    @classmethod
    def process_method(cls, queryable: QueryableClass, input: Any) -> Any:
        raise TypeError(f"Undefined subtype: {type(queryable)}")

    @classmethod
    def format_question_description(cls, queryable: QueryableClass, question_description: str, variables_data: List[Any]) -> str:
        queryable_variables = queryable.variables()
        formatted_description = question_description
        for index, variable_name in enumerate(queryable_variables):
            formatted_description = formatted_description.replace(f"{{{variable_name}}}", f"{variable_name}: {variables_data[index]}")

        return formatted_description
