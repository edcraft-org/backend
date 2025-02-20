from typing import Any, Dict, Type, get_args, get_origin

from question_generation.input.input_class import Input
from question_generation.input.input_subclasses.primitive.bool_type import BoolInput
from question_generation.input.input_subclasses.primitive.int_type import IntInput
from question_generation.input.input_subclasses.primitive.str_type import StringInput
from question_generation.quantifiable.quantifiable_class import Quantifiable
from utils.classes_helper import get_all_subclasses, get_matching_class
from utils.constants import MAX_VALUE



def generate_data_for_type(data_type: Type, element_type: str, init_args: Dict[str, Any] = {}) -> Any:
    if not data_type:
        return {}
    origin = get_origin(data_type)
    if origin is not None:
        return handle_generic_type(data_type, element_type, origin, init_args)
    else:
        return handle_non_generic_type(data_type, element_type, init_args)

def handle_generic_type(data_type: Type, element_type: str, origin: Type, init_args: Dict[str, Any]) -> Any:
    args = get_args(data_type)
    if not args:
        raise ValueError(f"Generic type {data_type} has no arguments")

    element = args[0]

    input_subclasses = get_all_subclasses(Input)
    matching_class = get_matching_class(input_subclasses, origin.__name__)
    if matching_class:
        if element_type:
            element = get_matching_class(get_all_subclasses(Quantifiable), element_type) or element
            return matching_class(element, **init_args)
        else:
            return matching_class(**init_args)

    return generate_collection_data(origin, args, element, element_type, init_args)

def handle_non_generic_type(data_type: Type, element_type: str, init_args: Dict[str, Any]) -> Any:
    if issubclass(data_type, Quantifiable):
        return get_quantifiable_instance(data_type, element_type, init_args)
    elif issubclass(data_type, Input):
        return data_type(**init_args)
    elif data_type == int:
        return IntInput().generate_input()
    elif data_type == str:
        return StringInput().generate_input()
    elif data_type == bool:
        return BoolInput().generate_input()
    else:
        raise ValueError(f"Unsupported data type: {data_type}")

def generate_collection_data(origin: Type, args: tuple, element: Type, element_type: str, init_args: Dict[str, Any]) -> Any:
    if origin == list:
        return [generate_data_for_type(element, element_type, init_args) for _ in range(MAX_VALUE)]
    elif origin == tuple:
        return tuple(generate_data_for_type(arg, element_type, init_args) for arg in args)
    elif origin == set:
        return {generate_data_for_type(element, element_type, init_args) for _ in range(MAX_VALUE)}
    elif origin == dict:
        key_type, value_type = args
        return {generate_data_for_type(key_type, element_type, init_args): generate_data_for_type(value_type, element_type, init_args) for _ in range(MAX_VALUE)}

def get_quantifiable_instance(data_type: Type, element_type: str, init_args: Dict[str, Any]) -> Any:
    if element_type:
        matching_class = get_matching_class(get_all_subclasses(Quantifiable), element_type)
        if matching_class:
            return matching_class(**init_args)
    return data_type(**init_args)
