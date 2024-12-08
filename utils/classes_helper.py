import inspect
import importlib
from pathlib import Path
from typing import Dict, List, Type

from question_generation.input.input_subclasses.custom.adversarial_problem.adversarial_problem import AdversarialProblem
from question_generation.input.input_subclasses.custom.traversable.adjacency_list import AdjacencyListInput
from question_generation.input.input_subclasses.custom.traversable.traversable import Traversable
from utils.path_helper import get_subtopics, get_topics
from utils.types_helper import GeneratedQuestionClassType
from utils.exceptions import handle_exceptions


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
            importlib.import_module(module_name)  # Dynamically import the module
            cls = get_class_from_module(module_name)
            autoloaded_classes[topic][subtopic[:-3]] = cls

    return autoloaded_classes

def get_all_subclasses(cls) -> List[Type]:
    """Recursively get all subclasses of a given class."""
    subclasses = set(cls.__subclasses__())
    for subclass in cls.__subclasses__():
        subclasses.update(get_all_subclasses(subclass))
    return list(subclasses)

def get_subclasses_name(cls: Type) -> List[str]:
    """
    Get the subclasses of the given type.
    """
    subclasses = get_all_subclasses(cls)
    return [subclass.__name__ for subclass in subclasses]

@handle_exceptions
def get_subtopic_class(autoloaded_classes: Dict[str, Dict[str, GeneratedQuestionClassType]], topic: str, subtopic: str) -> GeneratedQuestionClassType:
    """Return class for a given subtopic."""
    if topic in autoloaded_classes and subtopic in autoloaded_classes[topic]:
        return autoloaded_classes[topic][subtopic]
    else:
        raise ValueError(f"Subtopic '{subtopic}' not found in autoloaded classes for topic '{topic}'.")

def get_matching_class(subclasses, name):
    return next((cls for cls in subclasses if cls.__name__ == name), None)
