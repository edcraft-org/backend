from typing import Any, Dict, List

def convert_keys(value: Dict[Any, List[Any]]) -> Dict[Any, List[Any]]:
    """
    Convert string keys back to integers if they represent digits.

    Args:
        value (Dict[Any, List[Any]]): The dictionary with potentially string keys.

    Returns:
        Dict[Any, List[Any]]: The dictionary with integer keys where applicable.
    """
    return {int(k) if isinstance(k, str) and k.isdigit() else k: v for k, v in value.items()}
