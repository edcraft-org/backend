import copy
import importlib
import inspect
from functools import singledispatchmethod, wraps
from pathlib import Path
from typing import Any, Dict, List, Type, get_args, get_origin

from fastapi import HTTPException

from question.input_subclasses.primitive_types.bool_type import BoolInputClass
from question.input_subclasses.primitive_types.str_type import StringInputClass
from question.input_subclasses.primitive_types.int_type import IntInputClass
from question.processor_class import ProcessorClass
from question.queryable_class import QueryableClass
from utils.constants import MAX_VALUE


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
def get_class_from_module(module_name: str) -> Type[ProcessorClass]:
    """Get all classes inside the module."""
    module = importlib.import_module(module_name)
    for name, obj in inspect.getmembers(module, inspect.isclass):
        if obj.__module__ == module_name:
            return obj
    raise ValueError(f"No class found in module {module_name}")


@handle_exceptions
def autoload_classes(base_path: str, base_package: str) -> Dict[str, Dict[str, Type[ProcessorClass]]]:
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
def list_topics(autoloaded_classes: Dict[str, Dict[str, Type[ProcessorClass]]]) -> List[str]:
    """Return a list of all topics."""
    return list(autoloaded_classes.keys())


@handle_exceptions
def list_subtopics(autoloaded_classes: Dict[str, Dict[str, Type[ProcessorClass]]], topic: str) -> List[str]:
    """Return a list of all subtopics for a given topic."""
    if topic in autoloaded_classes:
        return list(autoloaded_classes[topic].keys())
    else:
        raise ValueError(f"Topic '{topic}' not found in autoloaded classes.")


@handle_exceptions
def get_subtopic_class(autoloaded_classes: Dict[str, Dict[str, Type[ProcessorClass]]], topic: str, subtopic: str) -> Type[ProcessorClass]:
    """Return class for a given subtopic."""
    if topic in autoloaded_classes and subtopic in autoloaded_classes[topic]:
        return autoloaded_classes[topic][subtopic]
    else:
        raise ValueError(f"Subtopic '{subtopic}' not found in autoloaded classes for topic '{topic}'.")


@handle_exceptions
def get_function_signatures(cls: ProcessorClass) -> Dict[Type, inspect.Signature]:
    signatures = {}
    for name, method in cls.__dict__.items():
        if isinstance(method, singledispatchmethod):
            dispatcher = method.dispatcher
            for registered_type, registered_method in dispatcher.registry.items():
                if registered_type is not object:
                    func = registered_method.__func__ if hasattr(registered_method, '__func__') else registered_method
                    signatures[registered_type] = inspect.signature(func)
    return signatures


@handle_exceptions
def list_queryable(autoloaded_classes: Dict[str, Dict[str, Type[ProcessorClass]]], topic: str, subtopic: str) -> List[str]:
    cls = get_subtopic_class(autoloaded_classes, topic, subtopic)
    signatures = get_function_signatures(cls)
    return [queryable_type.queryable() for queryable_type in signatures.keys()]


@handle_exceptions
def list_variable(autoloaded_classes: Dict[str, Dict[str, Type[ProcessorClass]]], topic: str, subtopic: str, queryable_type: str) -> List[str]:
    cls = get_subtopic_class(autoloaded_classes, topic, subtopic)
    signatures = get_function_signatures(cls)

    for queryable_cls in signatures.keys():
        if queryable_cls.queryable() == queryable_type:
            signature = signatures[queryable_cls]
            return [param_name for param_name in signature.parameters if param_name not in ['cls', 'queryable']]

    raise HTTPException(status_code=404, detail=f"Queryable type '{queryable_type}' not found.")


@handle_exceptions
def generate_data_for_type(data_type: Type) -> Any:
    if data_type == int:
        return IntInputClass().generate_input()
    elif data_type == str:
        return StringInputClass().generate_input()
    elif data_type == bool:
        return BoolInputClass().generate_input()
    elif hasattr(data_type, '__origin__'):
        origin = get_origin(data_type)
        args = get_args(data_type)

        if origin == list:
            element_type = args[0]
            return [generate_data_for_type(element_type) for _ in range(MAX_VALUE)]
        elif origin == tuple:
            return tuple(generate_data_for_type(arg) for arg in args)
        elif origin == set:
            element_type = args[0]
            return {generate_data_for_type(element_type) for _ in range(MAX_VALUE)}
        elif origin == dict:
            key_type, value_type = args
            return {generate_data_for_type(key_type): generate_data_for_type(value_type) for _ in range(MAX_VALUE)}
    else:
        raise ValueError(f"Unsupported data type: {data_type}")


@handle_exceptions
def generate_question(autoloaded_classes: Dict[str, Dict[str, Type[ProcessorClass]]], topic: str, subtopic: str, queryable_type: str, number_of_options: int, question_description: str) -> Dict[str, Any]:
    cls = get_subtopic_class(autoloaded_classes, topic, subtopic)
    signatures = get_function_signatures(cls)
    for queryable_class, signature in signatures.items():
        if queryable_class.queryable() == queryable_type:
            queryable_instance = queryable_class()
            generated_data = {}
            for param_name, param in signature.parameters.items():
                if param_name not in ['cls', 'queryable']:
                    generated_data[param_name] = generate_data_for_type(param.annotation)
            result = {}
            result["answer"] = str(cls.process_method(queryable_instance, **copy.deepcopy(generated_data)))
            result["question"] = cls.format_question_description(question_description, generated_data)
            options = []
            for _ in range(number_of_options):
                generated_options = copy.deepcopy(generated_data)
                for param_name, param in signature.parameters.items():
                    if param_name not in ['cls', 'queryable', 'input']:
                        generated_options[param_name] = generate_data_for_type(param.annotation)
                option = str(cls.process_method(queryable_instance, **generated_options))
                options.append(option)
            result["options"] = options
            return result
    raise HTTPException(status_code=404, detail=f"Queryable type '{queryable_type}' not found.")


@handle_exceptions
def autoload_queryable_classes(base_path: str, base_package: str) -> Dict[str, Type[QueryableClass]]:
    """Autoload all queryable classes from the queryable_subclasses directory."""
    queryable_classes = {}
    queryable_path = Path(base_path) / base_package / 'queryable_subclasses'
    python_files = [f.stem for f in queryable_path.glob('*.py') if f.name != '__init__.py']

    for file in python_files:
        module_name = f"{base_package}.queryable_subclasses.{file}"
        module = importlib.import_module(module_name)
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, QueryableClass) and obj is not QueryableClass:
                queryable_classes[name] = obj

    return queryable_classes