import inspect
from abc import ABC
from typing import Any, Dict

from question.queryable_class import Queryable
from utils.faker_helper import generate_data_for_type
class Processor(ABC):
    def process(self, cls: Queryable) -> Dict[str, Any]:
        if cls in self.__class__.__bases__:
            signature = inspect.signature(cls.query)
            generated_data = {
                param_name: generate_data_for_type(param.annotation)
                for param_name, param in signature.parameters.items()
                if param_name != 'self'
            }
            return {"answer": cls.query(self, **generated_data), "generated_data": generated_data}
        else:
            raise ValueError(f"{cls} is not a valid base class of {self.__class__.__name__}")

    def format_question_description(self, question_description: str, variables: Dict[str, Any]) -> str:
        formatted_description = question_description
        for variable_key, variable_value in variables.items():
            formatted_description = formatted_description.replace(f"{{{variable_key}}}", f"{variable_key}: {variable_value}")
        return formatted_description
