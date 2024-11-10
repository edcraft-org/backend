import copy
import importlib
import inspect
from functools import wraps
from pathlib import Path
import random
from typing import Any, Dict, List, Type, Union
from fastapi import HTTPException
from question_generation.algo.algo import Algo
from question_generation.queryable.queryable_class import Queryable
from question_generation.question.question import Question
from utils.faker_helper import generate_data_for_type

GeneratedQuestionClassType = Union[Type[Algo], Type[Question], Type[Queryable]]

def handle_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error in {func.__name__}: {str(e)}")
    return wrapper


@handle_exceptions
def get_topics(base_path: str) -> List[str]:
    """Get all topics (folder names) inside the base path."""
    return [p.name for p in Path(base_path).iterdir() if p.is_dir() and not p.name.startswith('__')]


@handle_exceptions
def get_subtopics(topic_path: str) -> List[str]:
    """Get all subtopics (file names) inside the topic path."""
    return [p.name for p in Path(topic_path).glob('*.py') if p.name != '__init__.py']


@handle_exceptions
def get_class_from_module(module_name: str) -> GeneratedQuestionClassType:
    """Get all classes inside the module."""
    module = importlib.import_module(module_name)
    for name, obj in inspect.getmembers(module, inspect.isclass):
        if obj.__module__ == module_name:
            return obj
    raise ValueError(f"No class found in module {module_name}")


@handle_exceptions
def autoload_classes(base_path: str, base_package: str) -> Dict[str, Dict[str, GeneratedQuestionClassType]]:
    """Autoload classes from the algorithm folder."""
    autoloaded_classes = {}
    topics = get_topics(base_path)

    for topic in topics:
        topic_path = Path(base_path) / topic
        subtopics = get_subtopics(str(topic_path))
        autoloaded_classes[topic] = {}

        for subtopic in subtopics:
            module_name = f"{base_package}.{topic}.{subtopic[:-3]}"  # Remove .py extension
            cls = get_class_from_module(module_name)
            autoloaded_classes[topic][subtopic[:-3]] = cls

    return autoloaded_classes


@handle_exceptions
def list_topics(autoloaded_classes: Dict[str, Dict[str, GeneratedQuestionClassType]]) -> List[str]:
    """Return a list of all topics."""
    return list(autoloaded_classes.keys())


@handle_exceptions
def list_subtopics(autoloaded_classes: Dict[str, Dict[str, GeneratedQuestionClassType]], topic: str) -> List[str]:
    """Return a list of all subtopics for a given topic."""
    if topic in autoloaded_classes:
        return list(autoloaded_classes[topic].keys())
    else:
        raise ValueError(f"Topic '{topic}' not found in autoloaded classes.")


@handle_exceptions
def get_subtopic_class(autoloaded_classes: Dict[str, Dict[str, GeneratedQuestionClassType]], topic: str, subtopic: str) -> GeneratedQuestionClassType:
    """Return class for a given subtopic."""
    if topic in autoloaded_classes and subtopic in autoloaded_classes[topic]:
        return autoloaded_classes[topic][subtopic]
    else:
        raise ValueError(f"Subtopic '{subtopic}' not found in autoloaded classes for topic '{topic}'.")


@handle_exceptions
def list_queryable(autoloaded_classes: Dict[str, Dict[str, GeneratedQuestionClassType]], topic: str, subtopic: str) -> List[str]:
    cls = get_subtopic_class(autoloaded_classes, topic, subtopic)
    queryable_classes = [base.__name__ for base in cls.__bases__ if issubclass(base, Queryable)]
    return queryable_classes

def get_variable_annotations(cls: GeneratedQuestionClassType, queryable_type: str) -> Dict[str, List[Dict[str, Any]]]:
    """Get variable annotations for algo and query methods."""
    # Get variables from the algo method
    algo_signature = inspect.signature(cls().algo)
    algo_variables = [
        {"name": param_name, "type": param.annotation}
        for param_name, param in algo_signature.parameters.items()
        if param_name != 'self'
    ]

    # Get variables from the query methods
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

@handle_exceptions
def list_variable(autoloaded_classes: Dict[str, Dict[str, GeneratedQuestionClassType]], topic: str, subtopic: str, queryable_type: str) -> List[Dict[str, str]]:
    cls = get_subtopic_class(autoloaded_classes, topic, subtopic)
    variable_annotations = get_variable_annotations(cls, queryable_type)

    # Convert types to strings
    algo_variables = [
        {"name": var["name"], "type": str(var["type"])}
        for var in variable_annotations["algo_variables"]
    ]
    query_variables = [
        {"name": var["name"], "type": str(var["type"])}
        for var in variable_annotations["query_variables"]
    ]

    return algo_variables + query_variables


def shuffle_data(data: Any) -> Any:
    """Shuffle the data based on its type."""
    if isinstance(data, list):
        random.shuffle(data)
        return data
    elif isinstance(data, tuple):
        temp_list = list(data)
        random.shuffle(temp_list)
        return tuple(temp_list)
    elif isinstance(data, dict):
        keys = list(data.keys())
        random.shuffle(keys)
        return {key: data[key] for key in keys}
    else:
        raise ValueError(f"Unsupported data type for shuffling: {type(data)}")


@handle_exceptions
def generate_question(autoloaded_classes: Dict[str, Dict[str, GeneratedQuestionClassType]], topic: str, subtopic: str, queryable_type: str, number_of_options: int, question_description: str) -> Dict[str, Any]:
    cls = get_subtopic_class(autoloaded_classes, topic, subtopic)
    cls_instance = cls()
    query_result = cls_instance.query_all()
    result = {}

    variable_annotations = get_variable_annotations(cls, queryable_type)
    algo_variables = variable_annotations["algo_variables"]
    query_variables = variable_annotations["query_variables"]

    algo_generated_data = {
        var["name"]: generate_data_for_type(var["type"])
        for var in algo_variables
    }
    cls_instance.algo(**algo_generated_data)

    for base, query_method in query_result:
        if base.__name__ == queryable_type and issubclass(base, Queryable):
            query_generated_data = {
                var["name"]: generate_data_for_type(var["type"])
                for var in query_variables
            }

            base_instance = base()
            for attr in dir(cls_instance):
                if not attr.startswith('__') and hasattr(base_instance, attr) and attr != 'variable':
                    setattr(base_instance, attr, getattr(cls_instance, attr))

            query_output = query_method(base_instance, **query_generated_data)
            result = {
                'answer': str(query_output),
                'question': cls_instance.format_question_description(question_description, {**algo_generated_data, **query_generated_data}),
                'options': []
            }
            options = []
            for _ in range(number_of_options - 1):
                option = shuffle_data(copy.deepcopy(query_output))
                options.append(str(option))
            options.append(result['answer'])
            random.shuffle(options)
            result["options"] = options
    return result
