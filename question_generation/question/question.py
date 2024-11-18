from typing import Any, Dict

from question_generation.quantifiable.quantifiable_class import Quantifiable


class Question:
    def format_question_description(self, question_description: str, variables: Dict[str, Any]) -> str:
        formatted_description = question_description
        for variable_key, variable_value in variables.items():
            if isinstance(variable_value, Quantifiable):
                variable_value = variable_value.value()
            formatted_description = formatted_description.replace(f"{{{variable_key}}}", f"{variable_key}: {variable_value}")
        return formatted_description
