from typing import Any, Type, get_args, get_origin


from question_generation.input.input_subclasses.primitive.bool_type import BoolInput
from question_generation.input.input_subclasses.primitive.int_type import IntInput
from question_generation.input.input_subclasses.primitive.str_type import StringInput
from utils.constants import MAX_VALUE

def generate_data_for_type(data_type: Type) -> Any:
    if data_type == int:
        return IntInput().generate_input()
    elif data_type == str:
        return StringInput().generate_input()
    elif data_type == bool:
        return BoolInput().generate_input()
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
