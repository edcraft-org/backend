from typing import Any, Type, get_args, get_origin


from question_generation.input.input_subclasses.composite.list_type import ListInput
from question_generation.input.input_subclasses.primitive.bool_type import BoolInput
from question_generation.input.input_subclasses.primitive.int_type import IntInput
from question_generation.input.input_subclasses.primitive.str_type import StringInput
from question_generation.quantifiable.quantifiable_class import Quantifiable
from utils.constants import MAX_VALUE

def generate_data_for_type(data_type: Type) -> Any:
    origin = get_origin(data_type)
    if origin is not None:
        # Handle generic types
        args = get_args(data_type)
        if origin == list:
            element_type = args[0]
            if issubclass(element_type, Quantifiable):
                return [element_type() for _ in range(MAX_VALUE)]
            else:
                return [generate_data_for_type(element_type) for _ in range(MAX_VALUE)]
        elif origin == ListInput:
            element_type = args[0]
            return ListInput()
        elif origin == tuple:
            return tuple(generate_data_for_type(arg) for arg in args)
        elif origin == set:
            element_type = args[0]
            return {generate_data_for_type(element_type) for _ in range(MAX_VALUE)}
        elif origin == dict:
            key_type, value_type = args
            return {generate_data_for_type(key_type): generate_data_for_type(value_type) for _ in range(MAX_VALUE)}
    else:
        # Handle non-generic types
        if isinstance(data_type, type) and issubclass(data_type, Quantifiable):
            return data_type()
        elif data_type == int:
            return IntInput().generate_input()
        elif data_type == str:
            return StringInput().generate_input()
        elif data_type == bool:
            return BoolInput().generate_input()
        else:
            raise ValueError(f"Unsupported data type: {data_type}")

# def shuffle_data(data: Any) -> Any:
#     """Shuffle the data based on its type."""
#     if isinstance(data, list):
#         random.shuffle(data)
#         return data
#     elif isinstance(data, tuple):
#         temp_list = list(data)
#         random.shuffle(temp_list)
#         return tuple(temp_list)
#     elif isinstance(data, dict):
#         keys = list(data.keys())
#         random.shuffle(keys)
#         return {key: data[key] for key in keys}
#     else:
#         raise ValueError(f"Unsupported data type for shuffling: {type(data)}")
