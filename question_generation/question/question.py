from typing import Any, Dict


class Question:
    def format_question_description(self, question_description: str, variables: Dict[str, Any]) -> str:
        formatted_description = question_description
        for variable_key, variable_value in variables.items():
            formatted_description = formatted_description.replace(f"{{{variable_key}}}", f"{variable_key}: {variable_value}")
        return formatted_description
