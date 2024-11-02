import copy
import importlib
import inspect
from functools import wraps
from pathlib import Path
import random
from typing import Any, Dict, List, Type
from fastapi import HTTPException
from question.processor_class import Processor
from question.queryable_class import Queryable


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
def get_class_from_module(module_name: str) -> Type[Processor]:
    """Get all classes inside the module."""
    module = importlib.import_module(module_name)
    for name, obj in inspect.getmembers(module, inspect.isclass):
        if obj.__module__ == module_name:
            return obj
    raise ValueError(f"No class found in module {module_name}")


@handle_exceptions
def autoload_classes(base_path: str, base_package: str) -> Dict[str, Dict[str, Type[Processor]]]:
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
def list_topics(autoloaded_classes: Dict[str, Dict[str, Type[Processor]]]) -> List[str]:
    """Return a list of all topics."""
    return list(autoloaded_classes.keys())


@handle_exceptions
def list_subtopics(autoloaded_classes: Dict[str, Dict[str, Type[Processor]]], topic: str) -> List[str]:
    """Return a list of all subtopics for a given topic."""
    if topic in autoloaded_classes:
        return list(autoloaded_classes[topic].keys())
    else:
        raise ValueError(f"Topic '{topic}' not found in autoloaded classes.")


@handle_exceptions
def get_subtopic_class(autoloaded_classes: Dict[str, Dict[str, Type[Processor]]], topic: str, subtopic: str) -> Type[Processor]:
    """Return class for a given subtopic."""
    if topic in autoloaded_classes and subtopic in autoloaded_classes[topic]:
        return autoloaded_classes[topic][subtopic]
    else:
        raise ValueError(f"Subtopic '{subtopic}' not found in autoloaded classes for topic '{topic}'.")


@handle_exceptions
def list_queryable(autoloaded_classes: Dict[str, Dict[str, Type[Processor]]], topic: str, subtopic: str) -> List[str]:
    cls = get_subtopic_class(autoloaded_classes, topic, subtopic)
    queryable_classes = [base.__name__ for base in cls.__bases__ if issubclass(base, Queryable)]
    return queryable_classes


@handle_exceptions
def list_variable(autoloaded_classes: Dict[str, Dict[str, Type[Processor]]], topic: str, subtopic: str, queryable_type: str) -> List[str]:
    cls = get_subtopic_class(autoloaded_classes, topic, subtopic)
    for base in cls.__bases__:
        if base.__name__ == queryable_type and issubclass(base, Queryable):
            query_method = base.query
            signature = inspect.signature(query_method)
            return [param_name for param_name in signature.parameters if param_name != 'self']
    raise ValueError(f"Queryable type '{queryable_type}' not found in subtopic class '{cls.__name__}'.")


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
def generate_question(autoloaded_classes: Dict[str, Dict[str, Type[Processor]]], topic: str, subtopic: str, queryable_type: str, number_of_options: int, question_description: str) -> Dict[str, Any]:
    cls = get_subtopic_class(autoloaded_classes, topic, subtopic)

    queryable_cls = None
    for base in cls.__bases__:
        if base.__name__ == queryable_type and issubclass(base, Queryable):
            queryable_cls = base
            break

    if queryable_cls is None:
        raise ValueError(f"Queryable type '{queryable_type}' not found in subtopic class '{cls.__name__}'.")

    result = {}
    cls_instance = cls()
    process_result = cls_instance.process(queryable_cls)
    answer = process_result["answer"]
    generated_data = process_result["generated_data"]
    result['answer'] = str(answer)
    result['question'] = cls_instance.format_question_description(question_description, generated_data)

    options = []
    for _ in range(number_of_options - 1):
        option = shuffle_data(copy.deepcopy(answer))
        options.append(str(option))
    options.append(result['answer'])
    random.shuffle(options)
    result["options"] = options
    return result
