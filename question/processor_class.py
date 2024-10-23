
from abc import ABC
from typing import Any, Dict, List

from question.queryable_class import QueryableClass

class ProcessorClass(ABC):
    @classmethod
    def process_method(cls, queryable: QueryableClass, input: Any) -> Any:
        raise TypeError(f"Undefined subtype: {type(queryable)}")

    @classmethod
    def format_question_description(cls, question_description: str, variables: Dict[str, Any]) -> str:
        formatted_description = question_description
        for variable_key, variable_value in variables.items():
            formatted_description = formatted_description.replace(f"{{{variable_key}}}", f"{variable_key}: {variable_value}")

        return formatted_description
