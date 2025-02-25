from typing import Any, Callable, Dict, List

def convert_keys(value: Dict[Any, List[Any]]) -> Dict[Any, List[Any]]:
    """
    Convert string keys back to integers if they represent digits.

    Args:
        value (Dict[Any, List[Any]]): The dictionary with potentially string keys.

    Returns:
        Dict[Any, List[Any]]: The dictionary with integer keys where applicable.
    """
    return {int(k) if isinstance(k, str) and k.isdigit() else k: v for k, v in value.items()}


def deserialize_function(func_str: str) -> Callable:
    """
    Deserialize a function from its string representation.

    Args:
        func_str (str): The string representation of the function.

    Returns:
        Callable: The deserialized function.
    """
    func_dict = {}
    global_namespace = {}

    lines = func_str.strip().split("\n")
    import_lines, func_lines = [], []

    for line in lines:
        if line.startswith(("import", "from")):
            import_lines.append(line)
        else:
            func_lines.append(line)

    try:
        exec("\n".join(import_lines), global_namespace)
        exec("\n".join(func_lines), global_namespace, func_dict)
    except Exception as e:
        raise ValueError(f"Error executing function: {e}")

    function_name = next(iter(func_dict), None)
    if function_name is None:
        raise ValueError("No valid function found in provided string.")

    return func_dict[function_name]


def deserialize_init_args(init_args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deserialize any string representations of functions in the init_args dictionary.

    Args:
        init_args (Dict[str, Any]): The initialization arguments.

    Returns:
        Dict[str, Any]: The deserialized initialization arguments.
    """
    deserialized_args = {}
    for key, value in init_args.items():
        if isinstance(value, str) and "def " in value:
            deserialized_args[key] = deserialize_function(value)
        else:
            deserialized_args[key] = value

    return deserialized_args

