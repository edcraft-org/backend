import copy
import os
import importlib
import inspect
from functools import singledispatchmethod
from typing import Any, Dict, List, Type, get_args, get_origin

from fastapi import HTTPException

from question.input_subclasses.primitive_types.bool_type import BoolInputClass
from question.input_subclasses.primitive_types.str_type import StringInputClass
from question.input_subclasses.primitive_types.int_type import IntInputClass
from question.processor_class import ProcessorClass
from utils.constants import MAX_VALUE


def get_topics(base_path: str) -> List[str]:
    """Get all topics (folder names) inside the base path."""
    try:
        return [name for name in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, name)) and not name.startswith('__')]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting topics: {str(e)}")

def get_subtopics(topic_path: str) -> List[str]:
    """Get all subtopics (file names) inside the topic path."""
    try:
        return [name for name in os.listdir(topic_path) if name.endswith('.py') and name != '__init__.py']
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting subtopics: {str(e)}")

def get_class_from_module(module_name: str) -> ProcessorClass:
    """Get all classes inside the module."""
    try:
        module = importlib.import_module(module_name)
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if obj.__module__ == module_name:
                return obj
        raise ValueError(f"No class found in module {module_name}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting class from module: {str(e)}")

def autoload_classes(base_path: str, base_package: str) -> Dict[str, Dict[str, ProcessorClass]]:
    """Autoload classes from the algorithm folder."""
    try:
        autoloaded_classes = {}
        topics = get_topics(base_path)

        for topic in topics:
            topic_path = os.path.join(base_path, topic)
            subtopics = get_subtopics(topic_path)
            autoloaded_classes[topic] = {}

            for subtopic in subtopics:
                module_name = f"{base_package}.{topic}.{subtopic[:-3]}"  # Remove .py extension
                cls = get_class_from_module(module_name)
                autoloaded_classes[topic][subtopic[:-3]] = cls

        return autoloaded_classes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error autoloading classes: {str(e)}")

def list_topics(autoloaded_classes: Dict[str, Dict[str, List[Type]]]) -> List[str]:
    """Return a list of all topics."""
    try:
        return list(autoloaded_classes.keys())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing topics: {str(e)}")

def list_subtopics(autoloaded_classes: Dict[str, Dict[str, List[Type]]], topic: str) -> List[str]:
    """Return a list of all subtopics for a given topic."""
    try:
        if topic in autoloaded_classes:
            return list(autoloaded_classes[topic].keys())
        else:
            raise ValueError(f"Topic '{topic}' not found in autoloaded classes.")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing subtopics: {str(e)}")

def get_subtopic_class(autoloaded_classes: Dict[str, Dict[str, List[Type]]], topic: str, subtopic: str) -> ProcessorClass:
    """Return class for a given subtopic."""
    try:
        if topic in autoloaded_classes and subtopic in autoloaded_classes[topic]:
            return autoloaded_classes[topic][subtopic]
        else:
            raise ValueError(f"Subtopic '{subtopic}' not found in autoloaded classes for topic '{topic}'.")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting subtopic class: {str(e)}")

def get_function_signatures(cls: ProcessorClass) -> Dict[Type, inspect.Signature]:
    try:
        signatures = {}
        for name, method in cls.__dict__.items():
            if isinstance(method, singledispatchmethod):
                dispatcher = method.dispatcher
                for registered_type, registered_method in dispatcher.registry.items():
                    if registered_type is not object:
                        func = registered_method.__func__ if hasattr(registered_method, '__func__') else registered_method
                        signatures[registered_type] = inspect.signature(func)
        return signatures
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting function signatures: {str(e)}")

def list_queryable(autoloaded_classes: Dict[str, Dict[str, ProcessorClass]], topic: str, subtopic: str) -> List[str]:
    try:
        cls = get_subtopic_class(autoloaded_classes, topic, subtopic)
        signatures = get_function_signatures(cls)
        return [queryable_type.queryable() for queryable_type in signatures.keys()]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")

def list_variable(autoloaded_classes: Dict[str, Dict[str, ProcessorClass]], topic: str, subtopic: str, queryable_type: str) -> List[str]:
    try:
        cls = get_subtopic_class(autoloaded_classes, topic, subtopic)
        signatures = get_function_signatures(cls)

        for queryable_cls in signatures.keys():
            if queryable_cls.queryable() == queryable_type:
                return queryable_cls.variables()

        raise HTTPException(status_code=404, detail=f"Queryable type '{queryable_type}' not found.")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")

def generate_data_for_type(data_type: Type) -> Any:
    try:
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
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating data for type: {str(e)}")

def generate_question(autoloaded_classes: Dict[str, Dict[str, ProcessorClass]], topic: str, subtopic: str, queryable_type: str, number_of_options: int, question_description: str) -> Dict[str, Any]:
    try:
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
                result["question"] = cls.format_question_description(queryable_instance, question_description, list(generated_data.values()))
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
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating question: {str(e)}")