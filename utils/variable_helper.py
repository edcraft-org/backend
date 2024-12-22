import inspect
import re
from types import GenericAlias
from typing import Any, Dict, List, Type
from question_generation.queryable.queryable_class import Queryable
from utils.classes_helper import get_subclasses_name, get_subtopic_class
from utils.exceptions import handle_exceptions
from utils.types_helper import GeneratedQuestionClassType

def get_init_arguments(cls: Type) -> List[Dict[str, Any]]:
    """Get the initialization arguments for a given class."""
    init_signature = inspect.signature(cls.__init__)
    exposed_args = getattr(cls, '_exposed_args', [])
    init_variables = [
        {"name": param_name, "type": format_type(str(param.annotation))}
        for param_name, param in init_signature.parameters.items()
        if param_name != 'self' and param_name != 'cls' and param.annotation != inspect._empty and param_name in exposed_args
    ]
    return init_variables

def get_subclasses_info(cls: Type) -> List[Dict[str, Any]]:
    """Get the subclasses and their initialization arguments for a given class."""
    subclasses = cls.__subclasses__()
    subclasses_info = [
        {"name": subclass.__name__, "arguments": get_init_arguments(subclass)}
        for subclass in subclasses
    ]
    return subclasses_info

def get_variable_annotations(cls: GeneratedQuestionClassType, queryable_type: str) -> Dict[str, List[Dict[str, Any]]]:
    """Get variable annotations for algo and query methods."""
    algo_signature = inspect.signature(cls().algo)
    algo_variables = []

    for param_name, param in algo_signature.parameters.items():
        if param_name != 'self':
            var_info = {"name": param_name, "type": param.annotation}

            actual_class = param.annotation.__origin__ if isinstance(param.annotation, GenericAlias) else param.annotation

            if inspect.isclass(actual_class):
                var_info["arguments"] = get_init_arguments(actual_class)
                var_info["subclasses"] = get_subclasses_info(actual_class)

            algo_variables.append(var_info)

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
def list_variable(autoloaded_classes: Dict[str, Dict[str, GeneratedQuestionClassType]], topic: str, subtopic: str, queryable_type: str) -> List[Dict[str, Any]]:
    cls = get_subtopic_class(autoloaded_classes, topic, subtopic)
    variable_annotations = get_variable_annotations(cls, queryable_type)
    algo_variables = [
      {
        "name": var["name"],
        "type": format_type(str(var["type"])),
        "subclasses": [
            {
                "name": subclass["name"],
                "arguments": [
                    {
                        "name": arg["name"],
                        "type": format_type(str(arg["type"]))
                    }
                    for arg in subclass["arguments"]
                ]
            }
            for subclass in var.get("subclasses", [])
        ],
        "arguments": [
            {
                "name": arg["name"],
                "type": format_type(str(arg["type"]))
            }
            for arg in var.get("arguments", [])
        ]
      }
      for var in variable_annotations["algo_variables"]
    ]
    query_variables = [
      {
        "name": var["name"],
        "type": format_type(str(var["type"])),
        "subclasses": [],
        "arguments": []
      }
      for var in variable_annotations["query_variables"]
    ]

    return algo_variables + query_variables
