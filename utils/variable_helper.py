import inspect
import re
from typing import Any, Dict, List
from question_generation.queryable.queryable_class import Queryable
from utils.classes_helper import get_subclasses_name, get_subtopic_class
from utils.exceptions import handle_exceptions
from utils.types_helper import GeneratedQuestionClassType

def get_variable_annotations(cls: GeneratedQuestionClassType, queryable_type: str) -> Dict[str, List[Dict[str, Any]]]:
    """Get variable annotations for algo and query methods."""
    algo_signature = inspect.signature(cls().algo)
    algo_variables = [
        {"name": param_name, "type": param.annotation}
        for param_name, param in algo_signature.parameters.items()
        if param_name != 'self'
    ]

    queryable_methods = cls().query_all()
    query_variables = []
    for base, query_method in queryable_methods:
        if base.__name__ == queryable_type and issubclass(base, Queryable):
            signature = inspect.signature(query_method)
            query_variables.extend(
                {"name": param_name, "type": param.annotation}
                for param_name, param in signature.parameters.items()
                if param_name != 'self' and param.kind not in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD)
            )

    return {
        "algo_variables": algo_variables,
        "query_variables": query_variables
    }

def format_type(type_str: str) -> str:
    """Format the type string to a more readable format."""
    # Handle generic types
    generic_type_pattern = re.compile(r'([\w\.]+)\[([\w\., ]+)\]')
    match = generic_type_pattern.match(type_str)
    if match:
        base_type = match.group(1).split('.')[-1]
        arg_types = ', '.join([arg.split('.')[-1] for arg in match.group(2).split(', ')])
        return f'{base_type}[{arg_types}]'

    # Handle simple types
    simple_type_pattern = re.compile(r"<class '([\w\.]+)'>")
    match = simple_type_pattern.match(type_str)
    if match:
        return match.group(1).split('.')[-1]

    return type_str

@handle_exceptions
def list_variable(autoloaded_classes: Dict[str, Dict[str, GeneratedQuestionClassType]], topic: str, subtopic: str, queryable_type: str) -> List[Dict[str, str]]:
    cls = get_subtopic_class(autoloaded_classes, topic, subtopic)
    variable_annotations = get_variable_annotations(cls, queryable_type)
    # Convert types to strings
    algo_variables = [
      {
        "name": var["name"],
        "type": format_type(str(var["type"])),
        "subclasses": get_subclasses_name(var["type"]) if get_subclasses_name(var["type"]) else []
      }
      for var in variable_annotations["algo_variables"]
    ]
    query_variables = [
      {
        "name": var["name"],
        "type": format_type(str(var["type"])),
        "subclasses": []
      }
      for var in variable_annotations["query_variables"]
    ]

    return algo_variables + query_variables
