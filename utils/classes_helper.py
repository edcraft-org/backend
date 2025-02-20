import inspect
import importlib
from pathlib import Path
from typing import Any, Dict, List, Type

from question_generation.input.input_subclasses.custom.adversarial_problem.adversarial_env import AdversarialEnv
from question_generation.input.input_subclasses.custom.graph.adjacency_list import AdjacencyListInput
from utils.types_helper import GeneratedQuestionClassType
from utils.exceptions import handle_exceptions


@handle_exceptions
def get_class_from_module(module_name: str) -> Type:
    """Get all classes inside the module."""
    module = importlib.import_module(module_name)
    for name, obj in inspect.getmembers(module, inspect.isclass):
        if obj.__module__ == module_name:
            return obj
    raise ValueError(f"No class found in module {module_name}")

@handle_exceptions
def autoload_classes(base_path: str, base_package: str) -> Dict[str, Dict[str, Any]]:
    """Autoload classes from the specified folder."""
    autoloaded_classes = {}
    traverse_directory(base_path, base_package, autoloaded_classes)
    return autoloaded_classes

@handle_exceptions
def traverse_directory(current_path: str, current_package: str, autoloaded_classes: Dict[str, Dict[str, Any]]):
    """Recursively traverse the directory structure and collect classes."""
    for item in Path(current_path).iterdir():
        if item.is_dir() and not item.name.startswith('__'):
            if item.name not in autoloaded_classes:
                autoloaded_classes[item.name] = {}
            traverse_directory(str(item), f"{current_package}.{item.name}", autoloaded_classes[item.name])
        elif item.is_file() and item.suffix == '.py' and item.name != '__init__.py':
            module_name = f"{current_package}.{item.stem}"
            importlib.import_module(module_name)  # Dynamically import the module
            cls = get_class_from_module(module_name)
            autoloaded_classes[item.stem] = cls

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
