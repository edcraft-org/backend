
from abc import ABC, abstractmethod
from typing import Any, Dict, List

class ProcessorClass(ABC):
    @classmethod
    @abstractmethod
    def subtopic(cls):
        pass

    @classmethod
    @abstractmethod
    def process_method(cls, queryable: str, algorithm: str, variables_data: List[Any], options_data: List[Any]) -> Dict[str, Any]:
        pass

    @classmethod
    def format_question_description(cls, queryable_variables: List[str], question_description: str, variables_data: List[Any]) -> str:
        formatted_description = question_description
        for index, variable_name in enumerate(queryable_variables):
            formatted_description = formatted_description.replace(f"{{{variable_name}}}", f"{variable_name}: {variables_data[index]}")

        return formatted_description
